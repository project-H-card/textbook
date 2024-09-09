import sys

from ruby import ruby
from template_to_pages import template_to_pages

def main(only_ruby=False, only_page=False):
    if not only_page:
        DATA_FILE_PATH = "gegw_data/data.csv"
        RESULT_FILE_PATH = "gegw_data/data_with_ruby.csv"
        SELF_RUBY_DATA_FILE_PATH = "gegw_data/ruby_data.csv"


        DONT_NEED_RUBY_COLUMNS = [
            "教材順", "カード順", "イラスト説明1キャラ", "イラスト説明2キャラ", "どうしてQキャラ", 
            "関ヶ原ではQキャラ", "関ヶ原の後Qキャラ", "カード画像", 
            "パラメータ1（知恵）", "パラメータ2（忠義）", "パラメータ3（勇気）", "パラメータ4（武力）", "パラメータ5（魅力）", "パラメータ6の名前", "パラメータ6の値",
            "レーダーチャート解説キャラ", "文字数"
        ]

        ruby(DATA_FILE_PATH, RESULT_FILE_PATH, SELF_RUBY_DATA_FILE_PATH, DONT_NEED_RUBY_COLUMNS)

    if only_ruby:
        return


    FIELDS = [
        "異名", "名前", "時代", "身分", "生没年", "開戦前の石高", "開戦後の石高", "兵力",
        "イラスト説明1キャラ", "イラスト説明1のタイトル", "イラスト説明1",
        "イラスト説明2キャラ", "イラスト説明2のタイトル", "イラスト説明2", 
        "効果名1", "効果名2", "どうしてQ", "どうしてQキャラ", "どうしてA",
        "関ヶ原ではQ", "関ヶ原ではQキャラ", "関ヶ原ではA", "関ヶ原の後Q",
        "関ヶ原の後Qキャラ", "関ヶ原の後A", "クイズ", "コメント", "カード画像", "東西",
        "パラメータ1（知恵）", "パラメータ2（忠義）", "パラメータ3（勇気）", "パラメータ4（武力）", "パラメータ5（魅力）",
        "パラメータ6の名前", "パラメータ6の値", "レーダーチャート解説キャラ", "レーダーチャート解説", "家紋名"
    ]

    DATA_WITH_RUBY_FILE_PATH = "gegw_data/data_with_ruby.csv"
    TEMPLATE_FILE_PATH = "gegw_templates/template.html"
    INDEX_TEMPLATE_FILE_PATH = "gegw_templates/index_template.html"
    PAGES_DIV_TEMPLATE_FILE_PATH = "gegw_templates/pages_div_template.html"
    ALL_TEMPLATE_FILE_PATH = "gegw_templates/all_template.html"
    RESULT_DIR = "gegw_pages/"

    template_to_pages(
        FIELDS, DATA_WITH_RUBY_FILE_PATH, TEMPLATE_FILE_PATH, 
        INDEX_TEMPLATE_FILE_PATH, PAGES_DIV_TEMPLATE_FILE_PATH, 
        ALL_TEMPLATE_FILE_PATH, RESULT_DIR)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    elif sys.argv[1] == "ruby":
        main(only_ruby=True)
    elif sys.argv[1] == "page":
        main(only_page=True)