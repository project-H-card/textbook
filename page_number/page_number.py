import os
import glob
from PIL import Image, ImageDraw, ImageFont

# 画像が格納されているディレクトリ
src_dir = 'page_number/name_changed/'
output_dir = 'page_number/output/'  # 出力先のディレクトリ

# Robotoフォントのパス（システムにインストールされている場合はそのパスを指定）
font_path = "assets/fonts/Roboto-Bold.ttf"

margin_x_rate = 6 / (364+6*2) # B4の横幅364mmに対して6mmの余白
margin_y_rate = 6 / (257+6*2) # B4の縦幅257mmに対して6mmの余白

# ページ番号の設定
def add_page_numbers(image_path, page_number, font, output_path):
    # 画像を開く
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # ページ番号を配置するテキスト
    text1 = str(page_number*2-2).zfill(3)
    text2 = str(page_number*2-1).zfill(3)

    # テキストのサイズと配置位置を指定
    text_size = 40 / 3381 * width  # 文字のサイズを指定
    font = ImageFont.truetype(font, text_size)

    # 左下と右下の座標を計算
    margin_x = width * margin_x_rate * 1.3  # 画像端からの横方向の余白
    margin_y = height * margin_y_rate * 1.3  # 画像端からの縦方向の余白
    left_position = (margin_x, height - text_size - margin_y)
    right_position = (width - margin_x - draw.textbbox((0, 0), text2, font=font)[2], height - text_size - margin_y)

    # テキストを左下と右下に描画
    fill = "white"
    if page_number == 2 or page_number == 53:
        fill = "black"
    draw.text(left_position, text1, font=font, fill=fill)  # 左下
    draw.text(right_position, text2, font=font, fill=fill)  # 右下

    # 画像を保存
    print(output_path)
    img.save(output_path)

# 画像ファイルをループして処理
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
files = glob.glob(f"{src_dir}/*.png")
files.sort()
files = list(map(lambda file: file.split("/")[-1], files))
print(files)
# exit()


for i in range(len(files)):
    filename: str = files[i]
    if filename.lower().endswith(('.png')):
        input_image_path = os.path.join(src_dir, filename)
        output_image_path = os.path.join(output_dir, filename)

        # ページ番号を追加
        add_page_numbers(input_image_path, i + 1, font_path, output_image_path)

print("すべての画像にページ番号を追加しました。")
