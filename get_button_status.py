from gpiozero import Button


class ButtonStatus:
    def __init__(self, button_gpio: int = 2) -> None:
        self.button = Button(button_gpio)

    def get_button_status(self) -> bool:
        return self.button.is_pressed


if __name__ == "__main__":
    from time import sleep
    bs = ButtonStatus()
    for i in range(10):
        print(bs.get_button_status())
        sleep(1)
