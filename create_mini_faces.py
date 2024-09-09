from PIL import Image
import os

# 画像フォルダパス
image_folder = 'assets/images/textbook/common/mini/gegw/'

# 画像の並び順リスト
image_files = [
    # シュン1〜8
    'シュン1.webp', 'シュン2.webp', 'シュン3.webp', 'シュン4.webp', 'シュン5.webp', 'シュン6.webp', 'シュン7.webp', 'シュン8.webp',
    # ハマボウ1〜8
    'ハマボウ1.webp', 'ハマボウ2.webp', 'ハマボウ3.webp', 'ハマボウ4.webp', 'ハマボウ5.webp', 'ハマボウ6.webp', 'ハマボウ7.webp', 'ハマボウ8.webp',
    # シオリン1〜8
    'シオリン1.webp', 'シオリン2.webp', 'シオリン3.webp', 'シオリン4.webp', 'シオリン5.webp', 'シオリン6.webp', 'シオリン7.webp', 'シオリン8.webp',
    # ジェンキンス、サリー、スクナ、サトリ（4つの名前の画像）
    'ジェンキンス1.webp', 'ジェンキンス2.webp', 'サリー1.webp', 'サリー2.webp', 'スクナ1.webp', 'スクナ2.webp', 'サトリ1.webp'
]

# 出力画像の1つあたりのサイズ（256×256px）
image_size = 256

# 出力画像（横8列×縦4行の合計サイズ）を作成
output_image = Image.new('RGB', (image_size * 8, image_size * 4))

# 画像を順に処理して貼り付ける
for idx, filename in enumerate(image_files):
    img_path = os.path.join(image_folder, filename)
    if os.path.exists(img_path):
        img = Image.open(img_path)
        img = img.resize((image_size, image_size))
        
        # x座標とy座標を計算して画像を貼り付ける
        x = (idx % 8) * image_size  # 横方向の位置
        y = (idx // 8) * image_size  # 縦方向の位置
        
        output_image.paste(img, (x, y))

# 新しい画像として保存
output_image.save('mini_faces.jpg')
output_image.show()  # 画像を表示（オプション）
