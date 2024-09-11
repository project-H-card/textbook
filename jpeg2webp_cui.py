import sys
import os
import glob
from PIL import Image



# 画像処理関数
def process_image(file_path):
    processed_image_path =  file_path.replace(".jpeg", ".webp").replace(".jpg", ".webp")
    Image.open(file_path).convert('RGBA').save(processed_image_path)

    print('処理完了:', processed_image_path)



def main():
    if len(sys.argv) < 2:
        print("usage: python jpeg2webp_cui.py <dir_path>")
        return
    relative_path = sys.argv[1]
    cwd = os.getcwd()
    abs_path = os.path.join(cwd, relative_path)
    print(abs_path)
    
    files = glob.glob(abs_path + "/*.jpeg") + glob.glob(abs_path + "/*.jpg")
    for file in files:
        print(file)
        process_image(file)



main()

