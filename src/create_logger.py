from pathlib import Path
import logging
from logging import getLogger, StreamHandler, FileHandler, Formatter, Logger


def create_logger(logger_name: str, log_filename: Path) -> Logger:
    # ref: https://qiita.com/mimitaro/items/9fa7e054d60290d13bfc
    # --------------------------------
    # 1.loggerの設定
    # --------------------------------
    # loggerオブジェクトの宣言
    logger = getLogger(logger_name)

    # loggerのログレベル設定(ハンドラに渡すエラーメッセージのレベル)
    logger.setLevel(logging.DEBUG)

    # --------------------------------
    # 2.handlerの設定
    # --------------------------------
    # ログ出力フォーマット設定
    handler_format = Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # ---- 2-1.標準出力のhandler ----
    # handlerの生成
    stream_handler = StreamHandler()

    # handlerのログレベル設定(ハンドラが出力するエラーメッセージのレベル)
    stream_handler.setLevel(logging.DEBUG)

    # ログ出力フォーマット設定
    stream_handler.setFormatter(handler_format)

    # ---- 2-2.テキスト出力のhandler ----
    # handlerの生成
    file_handler = FileHandler(log_filename, 'a')

    # handlerのログレベル設定(ハンドラが出力するエラーメッセージのレベル)
    file_handler.setLevel(logging.DEBUG)

    # ログ出力フォーマット設定
    file_handler.setFormatter(handler_format)

    # --------------------------------
    # 3.loggerにhandlerをセット
    # --------------------------------
    # 標準出力のhandlerをセット
    logger.addHandler(stream_handler)
    # テキスト出力のhandlerをセット
    logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    logger = create_logger("sample", "temp_sample.log")
    # --------------------------------
    # ログ出力テスト
    # --------------------------------
    logger.debug("Hello World!")
