import statistics
from time import sleep

from gpiozero import Button, LED

from post_message import SlackMessage
from read_settings import SMART_KEY_BOX_SETTINGS, PROJ_DIR
from create_logger import create_logger


def main(do_send_slack_msg: bool) -> None:
    sleep_sec = 0.1
    threshold_rate = 0.8  # has_keyを切り替えるしきい値
    max_i = 10

    LOG_FILENAME = PROJ_DIR / "smart_key_box.log"
    logger = create_logger("main.py", LOG_FILENAME)

    slack_message = SlackMessage(
        SMART_KEY_BOX_SETTINGS["SLACK"]["SLACK_BOT_TOKEN"],
        SMART_KEY_BOX_SETTINGS["SLACK"]["CHANNEL_ID"],
        logger.getChild("post_message.py"),
    )
    keyracks_list = [
        KeyRack(
            keyrack_gpio=27, led_gpio=17,
            keyrack_name="keyrack_27", max_i=max_i
        ),
        KeyRack(
            keyrack_gpio=23, led_gpio=22,
            keyrack_name="keyrack_23", max_i=max_i
        ),
    ]

    i = 0
    while True:
        for keyrack in keyracks_list:
            if keyrack.keyrack_button.is_pressed:
                keyrack.count_pressed[i] = 1
            else:
                keyrack.count_pressed[i] = 0

        for keyrack in keyracks_list:
            # count_pressedの平均値を取得する．
            avg_count_pressed = statistics.mean(keyrack.count_pressed)

            # 鍵が外されたと判定した場合，has_keyをFalseにする．
            if keyrack.has_key is True and \
                    avg_count_pressed < (1 - threshold_rate):
                keyrack.has_key = False

            # 鍵が付けられたと判定した場合，has_keyをTrueにする．
            elif keyrack.has_key is False and \
                    avg_count_pressed > threshold_rate:
                keyrack.has_key = True

            # has_keyが変わらない場合，continueする．
            else:
                continue

            # has_keyが変わった場合は，
            # Bluetooth情報の受信とSlackへの送信を行う．
            person_name = "Alice"  # Get bluetooth information

            # messageを生成し，LEDを点灯 or 消灯させる
            if keyrack.has_key is True:
                removed_or_placed = "placed"
                keyrack.led.on()
            else:
                removed_or_placed = "removed"
                keyrack.led.off()
            message = (
                f"{person_name} {removed_or_placed} the key: "
                f"{keyrack.keyrack_name}."
            )

            # Slackへの投稿とlogの記録を行う
            if do_send_slack_msg:
                slack_message.post_message(message)
            logger.info(message)

        i += 1
        if i == max_i:
            i = 0
        # print(i)
        # print(count_pressed)

        sleep(sleep_sec)


class KeyRack:
    def __init__(
        self, keyrack_gpio: int, led_gpio: int,
        keyrack_name: str,
        max_i: int
    ) -> None:
        self.keyrack_button = Button(keyrack_gpio)
        self.led = LED(led_gpio)
        self.keyrack_name = keyrack_name

        self.count_pressed = [0 for _ in range(max_i)]
        self.has_key = True


if __name__ == "__main__":
    main(do_send_slack_msg=False)
