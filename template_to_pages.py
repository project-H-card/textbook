import os
import csv
import re

fields = [
    "異名",
    "名前",
    "時代",
    "身分",
    "生没年",
    "効果名1",
    "効果解説1",
    "効果名2",
    "効果解説2",
    "コラム",
    "どんな人？",
    "豆知識",
    "クイズ",
    "イラスト説明1のタイトル",
    "イラスト説明1",
    "イラスト説明2のタイトル",
    "イラスト説明2",
    "カード画像"
]

DATA_WITH_RUBY_FILE_PATH = "data_with_ruby.csv"
TEMPLATE_FILE_PATH = "templates/template.html"
INDEX_TEMPLATE_FILE_PATH = "templates/template.html"
RESULT_DIR = "pages/"


def remove_ruby_tags(text):
    """<rt>タグの中身と<ruby>タグを削除する。（<ruby>の中身の漢字は残す）"""
    return re.sub(r'<rt>.*?</rt>|<ruby>|</ruby>', '', text)

def create_index_page(names_without_ruby):
    # pages/index.html を生成（各ページへのリンクをひたすら並べる）
    with open(INDEX_TEMPLATE_FILE_PATH, "r", encoding="utf-8") as template_f:
        template = template_f.read()
        links = ""
        for name in names_without_ruby:
            links += f'<li><a href="{name}/index.html">{name}</a></li>\n'
        template = template.replace("{links}", links)
        with open(os.path.join(RESULT_DIR, "index.html"), "w", encoding="utf-8") as result_f:
            result_f.write(template)


# DATA_WITH_RUBY_FILE_PATH のデータを元に、TEMPLATE_FILE_PATH のテンプレートを使って、RESULT_DIR にページを生成する。
# 生成されるページは、data_with_ruby.csv の各行のデータを使って、テンプレートの中の {フィールド名} に対応する部分を置換する。
# 生成されるページは、RESULT_DIR の中に、data_with_ruby.csv の各行のデータの "名前" フィールドの値をディレクトリ名に置き換え、その中に "index.html" として保存される。
def main():
    with open(DATA_WITH_RUBY_FILE_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["名前"]
            name_without_ruby = remove_ruby_tags(name)
            dir_path = os.path.join(RESULT_DIR, name_without_ruby)
            os.makedirs(dir_path, exist_ok=True)
            with open(TEMPLATE_FILE_PATH, "r", encoding="utf-8") as template_f:
                template = template_f.read()
                for field in fields:
                    template = template.replace("{" + field + "}", row[field])
                    template = template.replace("{" + field + "ルビなし}", remove_ruby_tags(row[field]))
                with open(os.path.join(dir_path, "index.html"), "w", encoding="utf-8") as result_f:
                    result_f.write(template)
                    
        
        
                    


