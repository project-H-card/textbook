# 教材自動制作システム

# 基本機能
画像と `data.csv` を元に、 `template/template.html` を変換し、 `pages/{人物名}/index.html` を作る。

# 前提
1. Python を実行できる環境にする（Python3）
2. vscode 拡張機能の `Live Server` などを入れて、localのサーバーを起動できるようにする

# 使い方
1. `data.csv` にカードデータを決められたフォーマットで入れ、 `python ruby.py` によりルビつきのデータを `data_with_ruby.csv` に作成
   1. 基本的にスプシをCSVにエクスポートし名前を変える。
   2. 初めてやる時は `pip install -r requirements.txt` で必要なライブラリをインストールする。
2. ルビが間違っていれば、 `ruby_data.csv` に記入してから再度やれば直る。
3. canvaで作成した画像は `images/textbook/` 以下の適切な `{人物名}.png` か `{効果名}.png` でフォルダに入れること
    - `largeIllust/` 左ページの大きな画像を `{人物名}.png` で入れる
    - `aboutPersonCircle/` 右ページ右上の人物の画像を `{人物名}.png` で入れる
    - `miniCircle/` 左ページのクイズのアイコンの画像を `{人物名}.png` で入れる
    - `skill/` 右ページの効果の解説の画像を `{効果名}.png` で入れる
4. `python template_to_pages.py`  で `pages/{人物名}/index.html` のファイルがたくさんできる。
    - 同時に `pages/index.html` にライブサーバー用のこれらのページのリンク一覧ができる。 