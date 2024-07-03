import sys
import os
import glob
from PIL import Image



# 画像処理関数
def process_image(file_path, leave=False):
    processed_image_path =  file_path.replace(".png", ".webp")
    Image.open(file_path).convert('RGBA').save(processed_image_path)
    
    if not leave:
        os.remove(file_path)

    print('処理完了:', processed_image_path)



def main():
    if len(sys.argv) < 2:
        print("usage: python png2webp_cui.py <dir_path> [leave]")
        return
    relative_path = sys.argv[1]
    
    # png 画像を残すか
    leave = False
    if len(sys.argv) == 3 and sys.argv[2] == "leave":
        leave = True
    
    cwd = os.getcwd()
    abs_path = os.path.join(cwd, relative_path)
    print(abs_path)
    
    files = glob.glob(abs_path + "/*.png")
    for file in files:
        print(file)
        process_image(file, leave)



main()

