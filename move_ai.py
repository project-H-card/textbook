import os
import glob
import shutil

src_dir = 'submit/eps'
output_dir = 'submit/ai'

def move_ai():
    # 保存先ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    files = glob.glob(f"{src_dir}/*.ai")
    files = list(map(lambda file: file.split("/")[-1], files))
    
    for i in range(len(files)):
        filename: str = files[i]
        if filename.lower().endswith(('.ai')):
            input_image_path = os.path.join(src_dir, filename)
            output_image_path = os.path.join(output_dir, filename)
            shutil.move(input_image_path, output_image_path)
            print(f'{input_image_path} -> {output_image_path}')
            
move_ai()