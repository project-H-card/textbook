from PIL import Image

# GIF画像を開く
gif_image = Image.open('assets/images/textbook/emblem/丸に三つ引き.gif').convert('RGBA')

# 画像のピクセルデータを取得
pixels = gif_image.load()

# GIF画像の幅と高さを取得
width, height = gif_image.size

# 白い部分を黒に、他の部分を透明にする処理
for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        # 白い部分 (RGB = 255, 255, 255) を黒 (0, 0, 0) に変換
        if (r, g, b) == (255, 255, 255):
            pixels[x, y] = (0, 0, 0, a)
        else:
            pixels[x, y] = (0, 0, 0, 0)

# WebP形式で保存
gif_image.save('assets/images/textbook/emblem/丸に三つ引き.webp', 'WEBP')

print("画像が変換され、丸に三つ引き.webpとして保存されました。")
