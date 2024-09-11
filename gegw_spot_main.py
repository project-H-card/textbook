import sys

from ruby import ruby
from template_to_pages import template_to_pages

def main(only_ruby=False, only_page=False):
    if not only_page:
        DATA_FILE_PATH = "gegw_spot_data/data.csv"
        RESULT_FILE_PATH = "gegw_spot_data/data_with_ruby.csv"
        SELF_RUBY_DATA_FILE_PATH = "gegw_spot_data/ruby_data.csv"


        DONT_NEED_RUBY_COLUMNS = [
            "紹介キャラ名", "紹介キャラ画像",
            "紹介キャラ名右", "紹介キャラ画像右",
        ]

        ruby(DATA_FILE_PATH, RESULT_FILE_PATH, SELF_RUBY_DATA_FILE_PATH, DONT_NEED_RUBY_COLUMNS)

    if only_ruby:
        return


    FIELDS = [
        "紹介キャラ名", "紹介キャラ画像",
        "紹介キャラ名右", "紹介キャラ画像右",
        "場所名", "場所詳細", "紹介キャラ異名", "紹介内容",
        "場所名右", "場所詳細右", "紹介キャラ異名右", "紹介内容右",
    ]

    DATA_WITH_RUBY_FILE_PATH = "gegw_spot_data/data_with_ruby.csv"
    TEMPLATE_FILE_PATH = "gegw_spot_templates/template.html"
    INDEX_TEMPLATE_FILE_PATH = "gegw_spot_templates/index_template.html"
    PAGES_DIV_TEMPLATE_FILE_PATH = "gegw_spot_templates/pages_div_template.html"
    ALL_TEMPLATE_FILE_PATH = "gegw_spot_templates/all_template.html"
    RESULT_DIR = "gegw_spot_pages/"

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