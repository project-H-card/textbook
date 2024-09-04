import sys
import os


def main():
    if len(sys.argv) < 2:
        print("usage: python png2webp_cui.py <dir_path>")
        return
    directory_path = sys.argv[1]
    
    # ディレクトリ内のファイルをリストアップ
    for filename in os.listdir(directory_path):
        # フルパスを取得
        old_file_path = os.path.join(directory_path, filename)
        
        # ファイルかどうかを確認
        if os.path.isfile(old_file_path):
            # 新しいファイル名を作成（最初の7文字を除く）
            new_filename = filename[7:]
            new_file_path = os.path.join(directory_path, new_filename)
            
            # ファイルをリネーム
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {old_file_path} -> {new_file_path}')



main()

