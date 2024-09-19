# src/ 以下の 画像で、pages.csvファイルで2列目の名前と一致した画像を1列目のファイル名に変更し、name_changed/ 以下に保存する。

# import glob
import os
import shutil

# 画像ファイルの保存先ディレクトリ
src_directory = 'page_number/src/'
dst_directory = 'page_number/name_changed/'

# 保存先ディレクトリが存在しない場合は作成
if not os.path.exists(dst_directory):
    os.makedirs(dst_directory)


with open('page_number/pages.csv', 'r', encoding='utf-8') as f:
    pages = [line.strip().split(',') for line in f]

# csvファイルの内容に基づいて名前変更を行う
for page in pages[1:]:
    original_name = page[1].strip() + ".png"  # 2列目がオリジナルのファイル名
    new_name = page[0].strip().replace(".eps", ".png")  # 1列目が新しいファイル名

    # 拡張子を含むファイル名を組み立てる
    original_path = os.path.join(src_directory, original_name)
    new_path = os.path.join(dst_directory, new_name)

    # ファイルが存在する場合のみ処理
    if os.path.exists(original_path):
        # 画像ファイルを新しい名前に変更してコピー
        shutil.copyfile(original_path, new_path)
        print(f'{original_name} -> {new_name}')
    else:
        print(f'{original_name} が見つかりませんでした。')