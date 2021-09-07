import logging
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackMessage:
    def __init__(
        self, token: str, channel_id: str,
        logger: logging.getLogger
    ) -> None:
        self.client = WebClient(token=token)
        self.logger = logger
        self.channel_id = channel_id

    def post_message(self, text: str):
        try:
            # Call the chat.postMessage method using the WebClient
            result = self.client.chat_postMessage(
                channel=self.channel_id,
                text=text
            )
            self.logger.info(result)

        except SlackApiError as e:
            self.logger.error(f"Error posting message: {e}")


if __name__ == "__main__":
    from read_settings import SMART_KEY_BOX_SETTINGS
    logger = logging.getLogger(__name__)
    sm = SlackMessage(
        SMART_KEY_BOX_SETTINGS["SLACK"]["SLACK_BOT_TOKEN"],
        SMART_KEY_BOX_SETTINGS["SLACK"]["CHANNEL_ID"],
        logger,
    )
    sm.post_message(text="Hello world")
