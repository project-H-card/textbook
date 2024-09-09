from PIL import Image
import os

# 画像があるディレクトリのパス
image_dir = "assets/images/textbook/common/mini/gegw"
# 保存先ディレクトリ
output_dir = image_dir


# 切り抜きの範囲 と 対象画像ファイル名のリスト
# crop_box = (161, 267, 167+344, 267+344)
# image_files = ["ハマボウ (5).png", "ハマボウ (6).png", "ハマボウ (7).png", "ハマボウ (8).png"]


crop_box = (499, 282, 499+512, 282+512)
image_files = ["ジェンキンス (1).png", "ジェンキンス (2).png"]


# 保存先ディレクトリが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 各画像の処理
for image_file in image_files:
    # 画像を開く
    image_path = os.path.join(image_dir, image_file)
    image = Image.open(image_path)
    
    # 画像を指定された範囲で切り抜く
    cropped_image = image.crop(crop_box)
    
    # ファイル名から括弧とスペースを削除
    new_filename = image_file.replace(" ", "").replace("(", "").replace(")", "")
    
    # 新しいファイル名で保存
    save_path = os.path.join(output_dir, new_filename)
    cropped_image.save(save_path)

    print(f"Processed and saved: {new_filename}")
