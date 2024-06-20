import requests
import csv
import json
import re
from time import sleep
import os

"""
usage: python ruby.py

作った後は data.csv, data_with_ruby.csv の名前を
「シリーズ名.csv」や「シリーズ名_with_ruby.csv」などに変えることを推奨する。
"""

""" 設定 """
# カラムを、 index ではなくヘッダー名で判断する場合 True に
USE_HEADER_NAME_TO_COLUMN  = True

DATA_FILE_PATH = "data.csv"
RESULT_FILE_PATH = "data_with_ruby.csv"
SELF_RUBY_DATA_FILE_PATH = "ruby_data.csv"


DONT_NEED_RUBY_COLUMNS = ["カード画像", "担当者"]

# この値で join した状態でふりがなAPIに一斉送信する。
COLUMN_SEPARATOR = ":"
ROW_SEPARATOR = ";"
SELF_RUBY_DATA_SEPARATOR = "#"
API_CHUNK_ROW_NUM = 10 # 一度にAPIに送信する行数
# ここが大きくてリクエストサイズが4KBを超えるとエラーになることがある。）
# {'error': {'code': -32602, 'message': 'Invalid params'}, 'id': '1234-1', 'jsonrpc': '2.0'}


target_url = "https://jlp.yahooapis.jp/FuriganaService/V2/furigana"

####
# 外部流出厳禁
APP_ID= "dj00aiZpPWFib1VDTjQxUWxPaiZzPWNvbnN1bWVyc2VjcmV0Jng9NzE-"
# 外部流出厳禁
####


def kanji_furigana_pair_to_kanji_ruby_pair(pair):
    """漢字と振り仮名のペアを、漢字と「<ruby> つきの HTML風テキスト」のペアに変換する。
    |が含まれている（途中にひらがながある）場合は、|で区切り、漢字にのみ振り仮名を振ったテキストを返す。

    Args:
        pair (dict): {"surface": "漢字", "furigana": "かんじ"} のようなオブジェクト

    Returns:
        str: <ruby> つきの HTML風テキスト
    """
    if "|" in pair["surface"]:
        pairs = pair["surface"].split("|")
        furiganas = pair["furigana"].split("|")
        return {
            "surface": "".join(pairs),
            "replacement":  "".join([f'<ruby>{pairs[i]}<rt>{furiganas[i]}</rt></ruby>' if pairs[i] != furiganas[i] else f'{pairs[i]}' for i in range(len(pairs))])
        }
    return {
        "surface": pair["surface"],
        "replacement": f'<ruby>{pair["surface"]}<rt>{pair["furigana"]}</rt></ruby>'
    }


def replace_kanji_with_ruby_local(before_text: str, kanji_furigana_pairs):
    """漢字入りのテキストの一部の漢字をローカルから読み込んだ振り仮名とのペアデータによって <ruby> 付きの html風テキスト に置換する。

    Args:
        - before_text (str): 置換前のテキスト
        - kanji_furigana_pairs (list[dict]): {"surface": "漢字", "furigana": "かんじ"} のようなオブジェクトの配列

    Returns:
        str: 置換後のテキスト
    """
    texts = [before_text]
    # 各漢字振り仮名ペアに対して置換
    kanji_ruby_pairs = list(map(kanji_furigana_pair_to_kanji_ruby_pair, kanji_furigana_pairs))
    for pair in kanji_ruby_pairs:
        temp_texts = []
        for text in texts:
            if "<ruby>" in text:
                temp_texts.append(text)
                continue
            pattern = re.escape(pair['surface'])
            replacement = f"{SELF_RUBY_DATA_SEPARATOR}{re.escape(pair['replacement'])}{SELF_RUBY_DATA_SEPARATOR}"
            text = re.sub(pattern, replacement, text)
            temp_texts += text.split(SELF_RUBY_DATA_SEPARATOR)
        texts = temp_texts
        # print(texts)
        # pattern = r'(?<!<ruby>)' + re.escape(pair['surface']) + r'(?!</ruby>)'
        # replacement = f"<ruby>{pair['surface']}<rt>{pair['furigana']}</rt></ruby>"
        # before_text = re.sub(pattern, replacement, before_text)

    return "".join(texts)


def generate_ruby_HTML_text(data: list):
    """yahoo API の仕様に従い、オブジェクトを <ruby> つきの HTML風テキスト に変換する。

    Args:
        data (array): yahoo api のレスポンスの result の word

    Returns:
        str: <ruby> つきの HTML風テキスト
    """
    ruby_text = ""
    for word in data:
        if "subword" in word:
            subword = word["subword"]
            ruby_text += generate_ruby_HTML_text(subword)
        elif "furigana" in word:
            furigana = word["furigana"]
            surface = word["surface"]
            if furigana == surface:
                ruby_text += surface
            else:
                ruby_text += f'<ruby>{surface}<rt>{furigana}</rt></ruby>'
        else:
            surface = word["surface"]
            ruby_text += surface
    return ruby_text


def extract_and_replace_ruby(text):
    # <ruby>タグで囲まれた部分を抽出
    ruby_parts = re.findall(r'<ruby>.*?</ruby>', text)
    # <ruby>タグで囲まれた部分を一時的な記号に置換
    temp_text = re.sub(r'<ruby>.*?</ruby>', '#', text)

    return temp_text, ruby_parts


def restore_ruby(text, ruby_parts):
    # 各プレースホルダーを対応する<ruby>タグで囲まれたテキストに置き換え
    for part in ruby_parts:
        text = text.replace('#', part, 1)
    return text


def create_kanji_furigana_pairs_by_local_file():
    """jsonまたはcsvから、{"surface": "漢字", "furigana": "かんじ"} のようなオブジェクトの配列を作成する。}"""
    
    if not os.path.exists(SELF_RUBY_DATA_FILE_PATH):
        print(f"\033[31m{SELF_RUBY_DATA_FILE_PATH} が存在しません。\033[0m")
        exit()

    if(SELF_RUBY_DATA_FILE_PATH.endswith(".json")):
        with open(SELF_RUBY_DATA_FILE_PATH) as f:
            kanji_furigana_pairs = json.loads(f.read())["data"]
        return kanji_furigana_pairs

    elif(SELF_RUBY_DATA_FILE_PATH.endswith(".csv")):
        with open(SELF_RUBY_DATA_FILE_PATH) as f:
            reader = csv.reader(f)
            header = next(reader)
            data = list(reader)
        return [{"surface": row[0], "furigana": row[1]} for row in data if row and len(row) >= 2 and row[0] and row[1]]

    return []


def request_furigana(sentence: str):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": f"Yahoo AppID: {APP_ID}",
    }
    
    # 参考： https://developer.yahoo.co.jp/webapi/jlp/furigana/v2/furigana.html
    # yahoo のルビのjsonの形式は、 `templates/yahoo_ruby.json` を参照。
    req_data = {
        "id": "1234-1",
        "jsonrpc": "2.0",
        "method": "jlp.furiganaservice.furigana",
        "params": {
            "q": sentence,
            "grade": 1 # 0（無指定）だと漢数字に振られない上にカタカナにまで振られた。
        }
    }
    
    response = requests.post(target_url, data=json.dumps(req_data), headers=headers)
    res_json = response.json()
    
    if(res_json.get("error")):
        rows = sentence.split(ROW_SEPARATOR)
        for row in rows:
            req_data["params"]["q"] = row
            response = requests.post(target_url, data=json.dumps(req_data), headers=headers)
            res_json = response.json()
            if(res_json.get("error")):
                print(f"\033[31mエラーが発生しました。{res_json['error']}\n以下の中に異体字などが含まれていないかを確認してください。\033[0m")
                print("------")
                print(f"\033[33m{row}\033[0m")
                print("------")
                exit()
        print(f"\033[31mエラーが発生しました。{res_json['error']}\n以下の中に異体字などが含まれていないか、また文字数が2000文字以上のような大きい値でないかを確認してください。\033[0m")
        print("------")
        print(f"\033[33m{sentence}\033[0m")
        print("------")
        exit()

    data = res_json["result"]["word"]
    print(data[:10])
    return data


def add_ruby(sentence):
    """文章に対して、 <ruby> をつけた HTML風テキスト にして返す。

    Args:
        sentence (str): ルビ付与前の文章

    Returns:
        str: ルビ付与後の文章
    """

    
    kanji_furigana_pairs = create_kanji_furigana_pairs_by_local_file()
    self_ruby_replaced_sentence = replace_kanji_with_ruby_local(sentence, kanji_furigana_pairs)
    print(self_ruby_replaced_sentence[:100])
    separated_parts_str, ruby_parts = extract_and_replace_ruby(self_ruby_replaced_sentence)
    
    # separated_part_str を ROW_SEPARATOR で split して API_CHUNK_ROW_NUM 個ずつに分割し、それぞれを ROW_SEPARATOR で再度joinしてリストにする。
    separated_parts_str_rows = separated_parts_str.split(ROW_SEPARATOR)
    separated_parts_chunks = [ROW_SEPARATOR.join(separated_parts_str_rows[i:i+API_CHUNK_ROW_NUM]) for i in range(0, len(separated_parts_str_rows), API_CHUNK_ROW_NUM)]
    
    ruby_texts = []
    
    for separated_parts in separated_parts_chunks:
        data = request_furigana(separated_parts)
        ruby_texts.append(generate_ruby_HTML_text(data))
        sleep(0.5)
    
    return restore_ruby(ROW_SEPARATOR.join(ruby_texts), ruby_parts)



def remove_columns_after_empty_array(array):
    """csvから読みとったデータのうち、空行以降を切り取る。

    Args:
        array (list): 切り取り前の配列

    Returns:
        list: 切り取り後の配列
    """
    # 空の配列を見つける
    empty_index = None
    for i, column in enumerate(array):
        column_strs = "".join(column)
        if not column or not column_strs or len(column_strs) < 10:  # 空の配列を見つけた場合
            empty_index = i
            break

    # 空の配列が見つかった場合、それ以降の列を削除
    if empty_index is not None:
        return array[:empty_index]
    else:
        return array



def main():
    if not os.path.exists(DATA_FILE_PATH):
        print(f"\033[31m{DATA_FILE_PATH} が存在しません。\033[0m")
        return
    with open(DATA_FILE_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        
        data = list(reader)
    data = remove_columns_after_empty_array(data)
    
    dont_need_ruby_columns_num = list(map(lambda column: header.index(column), DONT_NEED_RUBY_COLUMNS))
    # print(dont_need_ruby_columns_num)

    # data から ルビがいらない列を削除
    ruby_rows = []
    for row in data:
        ruby_rows.append([row[i] for i in range(len(row)) if i not in dont_need_ruby_columns_num])
    
    all_text = "".join(list(map(lambda row: "".join(row) , ruby_rows)))
    if (ROW_SEPARATOR in all_text) or (COLUMN_SEPARATOR in all_text) or (SELF_RUBY_DATA_SEPARATOR in all_text):
        print(f"\033[31m変換前のテキストがセパレータ（「{ROW_SEPARATOR}」または「{COLUMN_SEPARATOR}」または「{SELF_RUBY_DATA_SEPARATOR}」）を含みます。セパレータかファイル内容を変えてください。\033[0m")
        return
    ruby_rows_str = ROW_SEPARATOR.join(list(map(lambda row: COLUMN_SEPARATOR.join(row) , ruby_rows)))
    
    # print(ruby_rows_str)
    
    ruby_result_str = add_ruby(ruby_rows_str)
    # ruby_result_str = ruby_rows_str
    
    ruby_result = [row.split(COLUMN_SEPARATOR) for row in ruby_result_str.split(ROW_SEPARATOR)]
    
    # print(ruby_result)
    
    
    result = data
    for i in range(len(result)):
        for j in range(len(result[i])):
            if j not in dont_need_ruby_columns_num:
                result[i][j] = ruby_result[i][j]
        
    # print(result)

    
    with open(RESULT_FILE_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(result)
    
if __name__ == "__main__":
    main()
