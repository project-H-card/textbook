from ruby import ruby

def main():
    DATA_FILE_PATH = "gegw_qa/data/data.csv"
    RESULT_FILE_PATH = "gegw_qa/data/data_with_ruby.csv"
    SELF_RUBY_DATA_FILE_PATH = "gegw_qa/data/ruby_data.csv"


    DONT_NEED_RUBY_COLUMNS = [
        "番号", "ページ", "回答キャラ", "東西"
    ]

    ruby(DATA_FILE_PATH, RESULT_FILE_PATH, SELF_RUBY_DATA_FILE_PATH, DONT_NEED_RUBY_COLUMNS)

if __name__ == "__main__":
    main()