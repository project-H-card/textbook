import os
from PIL import Image

# ディレクトリのパス
directory = './temp'
output_directory = './assets/images/textbook/aboutPersonCircle'

# ディレクトリ内の全てのファイルを処理
for filename in os.listdir(directory):
    if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
        file_path = os.path.join(directory, filename)
        output_file_path = os.path.join(output_directory, filename)

        with Image.open(file_path) as img:
            width, height = img.size

            # 新しい高さは幅と同じ
            new_height = width

            if height > new_height:
                # 中心で切り取る
                left = 0
                top = (height - new_height) / 2
                right = width
                bottom = top + new_height

                img_cropped = img.crop((left, top, right, bottom))
                img_cropped.save(output_file_path)

print("画像の切り取りが完了しました。")
