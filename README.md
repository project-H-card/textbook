# 教材自動制作システム
# 関ヶ原のプリントパック用の説明

## ページのpng画像の作成について
ページ種類ごとにやり方がちょっとずつ違う。
1. `xxx_templates/` と `xxx_data/` が別に合ってそこからHTML内の`{}`を変換して `xxx_pages/`を作るタイプ
   1. `xxx_main.py` でルビ振りとページ作成を行う（コマンドライン引数で `ruby` または `page` を入れるとどちらかだけやる）
2. `xxx/` の中に `data/` と `pages/` があり js で自動で作成。
   1. `xxx_ruby.py` でルビを振り、そのデータを元にjsでページのHTMLができる。

css は人物ページように作った `_common.css` とページごとのcssを作成

## 入稿システムについて
`page_number/` と `submit/` が関係する。
### page_number
まず、 `change_name.py` を使って、`src/` 以下の 画像で、`pages.csv` ファイルで2列目の名前と一致した画像を1列目のファイル名に変更し、 `name_changed/` 以下に保存する。これにより、画像を入稿用のai（eps）ファイルと一致させる。

その後、 `page_number.py` を使って、各ページの左下にページ番号を振る。色や入れ方が冊子によって変わる可能性があるので注意。

### submit
まず、`eps2ai.jsx` を使い、`eps/` 以下のテンプレートのepsをaiに変換する。（ `ai/` に移すが、自動では移らないので自分で動かす）

次に、`printPack.jsx` を使い、`ai/` 以下のファイルと、同名の `png/` 以下のファイルを使って `.ai` の入稿データを完成させる。（なぜか実数値でずらさないと左上が合わせないので注意）

その後、 `ai2pdf.jsx` を使い、 `ai/` 以下の完成ファイルをPDFに変換。（これも手動で `pdf/` に移動する）

最後に、この `pdf/` を zip にして完成。あとは提出するだけ


# 以下、東西決戦のアプリ用の説明

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