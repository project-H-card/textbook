from ruby import ruby

def main():
    DATA_FILE_PATH = "gegw_war/data/data.csv"
    RESULT_FILE_PATH = "gegw_war/data/data_with_ruby.csv"
    SELF_RUBY_DATA_FILE_PATH = "gegw_war/data/ruby_data.csv"


    DONT_NEED_RUBY_COLUMNS = [
        "種類", "キャラクター", "画像"
    ]

    ruby(DATA_FILE_PATH, RESULT_FILE_PATH, SELF_RUBY_DATA_FILE_PATH, DONT_NEED_RUBY_COLUMNS)

if __name__ == "__main__":
    main()