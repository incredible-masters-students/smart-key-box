import statistics
from time import sleep

from get_button_status import ButtonStatus
from post_message import SlackMessage
from slack_bot_token import SLACK_BOT_TOKEN, CHANNEL_ID


class KeyAndRpi:
    def __init__(self, do_send_slack_msg: bool = True) -> None:
        self.bs = ButtonStatus()
        self.sm = SlackMessage(SLACK_BOT_TOKEN, CHANNEL_ID)
        self.do_send_slack_msg = do_send_slack_msg

    def main(self) -> None:
        i = 0
        max_i = 10
        has_key = True
        count_pressed = [0 for _ in range(max_i)]
        sleep_sec = 0.1
        threshold_rate = 0.8  # has_keyを切り替えるしきい値

        while True:
            if self.bs.get_button_status():
                count_pressed[i] = 1
            else:
                count_pressed[i] = 0

            if has_key is True and \
                    statistics.mean(count_pressed) < (1 - threshold_rate):
                has_key = False
                self.send_slack_message(has_key)
            elif has_key is False and \
                    statistics.mean(count_pressed) > threshold_rate:
                has_key = True
                self.send_slack_message(has_key)

            i += 1
            if i == max_i:
                i = 0
            # print(i)
            # print(count_pressed)

            sleep(sleep_sec)

    def send_slack_message(self, has_key: bool) -> None:
        name = "Alice"  # Get Bluetooth Info
        if has_key is True:
            removed_or_placed = "placed"
        else:
            removed_or_placed = "removed"
        msg = f"{name} {removed_or_placed} the key."

        if self.do_send_slack_msg:
            self.sm.post_message(msg)
        else:
            print(msg)


if __name__ == "__main__":
    kar = KeyAndRpi(do_send_slack_msg=False)
    kar.main()
