import statistics
from time import sleep
from argparse import ArgumentParser

from gpiozero import Button, LED

from post_message import SlackMessage
from read_settings import SMART_KEY_BOX_SETTINGS, PROJ_DIR
from create_logger import create_logger
from get_bluetooth_info import SmartphoneBluetoothInformation


def main() -> None:
    # 引数を解析し，Slackにて送信するか決定する
    parser = ArgumentParser(description="Smart Key Box")
    parser.add_argument(
        "--do-post-slack-message", "-p",
        action="store_true",
        help="Post messege to Slack or do not it for debug",
    )
    args = parser.parse_args()
    do_post_slack_message = args.do_post_slack_message

    # 定数・変数の初期化を行う
    SLEEP_SEC = 0.1
    THRESHOLD_RATE = 0.8  # has_keyを切り替えるしきい値
    MAX_I = 10

    LOG_FILENAME = PROJ_DIR / "smart_key_box.log"
    logger = create_logger("main.py", LOG_FILENAME)

    sp_ble_info = SmartphoneBluetoothInformation(
        logger=logger.getChild("get_bluetooth_info.py")
    )
    slack_message = SlackMessage(
        SMART_KEY_BOX_SETTINGS["SLACK"]["SLACK_BOT_TOKEN"],
        SMART_KEY_BOX_SETTINGS["SLACK"]["CHANNEL_ID"],
        logger.getChild("post_message.py"),
    )
    keyracks_list = [
        KeyRack(
            keyrack_gpio=26, led_gpio=23,
            keyrack_name="keyrack_left", max_i=MAX_I
        ),
        KeyRack(
            keyrack_gpio=16, led_gpio=22,
            keyrack_name="keyrack_center", max_i=MAX_I
        ),
        KeyRack(
            keyrack_gpio=6, led_gpio=27,
            keyrack_name="keyrack_right", max_i=MAX_I
        ),
    ]

    # ループを実行する
    i = 0
    while True:
        for keyrack in keyracks_list:
            if keyrack.keyrack_button.is_pressed:
                keyrack.count_pressed[i] = 1
            else:
                keyrack.count_pressed[i] = 0

        changed_keyrack_list = []
        for keyrack in keyracks_list:
            # count_pressedの平均値を取得する．
            avg_count_pressed = statistics.mean(keyrack.count_pressed)

            # 鍵が外されたと判定した場合，has_keyをFalseにする．
            if keyrack.has_key is True and \
                    avg_count_pressed < (1 - THRESHOLD_RATE):
                keyrack.has_key = False

            # 鍵が付けられたと判定した場合，has_keyをTrueにする．
            elif keyrack.has_key is False and \
                    avg_count_pressed > THRESHOLD_RATE:
                keyrack.has_key = True

            # has_keyが変わらない場合，continueする．
            else:
                continue

            # messageを生成し，LEDを点滅させる
            if keyrack.has_key is True:
                removed_or_placed = "placed"
                keyrack.led.blink(on_time=0.1, off_time=0.1, n=2)
            else:
                removed_or_placed = "removed"
                keyrack.led.blink(on_time=0.1, off_time=0.1, n=1)
            changed_keyrack_list.append({
                "removed_or_placed": removed_or_placed,
                "name": keyrack.keyrack_name,
            })

        if len(changed_keyrack_list) != 0:
            persons_name = ""
            persons_around_rpi =\
                sp_ble_info.get_bluetooth_info()
            if len(persons_around_rpi) != 0:
                for person_name in persons_around_rpi:
                    persons_name += f"{person_name}, "
                persons_name = persons_name[0:-2]
            else:
                persons_name = "Unkown person"

            message = ""
            for changed_keyrack in changed_keyrack_list:
                # has_keyが変わった場合は，
                # Bluetooth情報の受信とSlackへの送信を行う．
                message += (
                    f"{persons_name} {changed_keyrack['removed_or_placed']}"
                    " the key: "
                    f"{changed_keyrack['name']}. "
                )

            # Slackへの投稿とlogの記録を行う
            if do_post_slack_message:
                slack_message.post_message(message)
            logger.info(message)

        # iを更新する
        i += 1
        if i == MAX_I:
            i = 0

        sleep(SLEEP_SEC)


class KeyRack:
    def __init__(
        self, keyrack_gpio: int, led_gpio: int,
        keyrack_name: str,
        max_i: int
    ) -> None:
        # ボタンとLEDを生成する
        self.keyrack_button = Button(keyrack_gpio)
        self.led = LED(led_gpio)

        # キーラック名を生成する
        self.keyrack_name = keyrack_name

        # キーラックの初期状態を判定する
        temp_has_key = False
        if self.keyrack_button.is_pressed:
            temp_has_key = True

        # カウント用のリストとキーラックの状態の変数を生成する
        self.count_pressed = [int(temp_has_key) for _ in range(max_i)]
        self.has_key = temp_has_key


if __name__ == "__main__":
    main()
