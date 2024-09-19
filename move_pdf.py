import os
import glob
import shutil

src_dir = 'submit/ai'
output_dir = 'submit/pdf'

def move_pdf():
    # 保存先ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    files = glob.glob(f"{src_dir}/*.pdf")
    files = list(map(lambda file: file.split("/")[-1], files))
    
    for i in range(len(files)):
        filename: str = files[i]
        if filename.lower().endswith(('.pdf')):
            input_image_path = os.path.join(src_dir, filename)
            output_image_path = os.path.join(output_dir, filename)
            shutil.move(input_image_path, output_image_path)
            print(f'{input_image_path} -> {output_image_path}')
            
move_pdf()