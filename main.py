import statistics
from time import sleep

from gpiozero import Button

from post_message import SlackMessage
from slack_bot_token import SLACK_BOT_TOKEN, CHANNEL_ID


def main(do_send_slack_msg: bool) -> None:
    sleep_sec = 0.1
    threshold_rate = 0.8  # has_keyを切り替えるしきい値
    max_i = 10

    slack_message = SlackMessage(SLACK_BOT_TOKEN, CHANNEL_ID)
    keyracks_list = [
        KeyRack(keyrack_gpio=2, keyrack_name="keyrack_2", max_i=max_i)
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
            message = keyrack.create_slack_message(
                person_name=person_name,
            )
            if do_send_slack_msg:
                slack_message.post_message(message)
            else:
                print(message)

        i += 1
        if i == max_i:
            i = 0
        # print(i)
        # print(count_pressed)

        sleep(sleep_sec)


class KeyRack:
    def __init__(
        self, keyrack_gpio: int,
        keyrack_name: str,
        max_i: int
    ) -> None:
        self.keyrack_button = Button(keyrack_gpio)
        self.keyrack_name = keyrack_name

        self.count_pressed = [0 for _ in range(max_i)]
        self.has_key = True

    def create_slack_message(self, person_name: str) -> str:
        if self.has_key is True:
            removed_or_placed = "placed"
        else:
            removed_or_placed = "removed"
        message = (
            f"{person_name} {removed_or_placed} the key: "
            f"{self.keyrack_name}."
        )
        return message


if __name__ == "__main__":
    main(do_send_slack_msg=False)
