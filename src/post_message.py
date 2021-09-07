import logging
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackMessage:
    def __init__(self, token: str, channel_id: str) -> None:
        self.client = WebClient(token=token)
        self.logger = logging.getLogger(__name__)
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
    from slack_bot_token import SLACK_BOT_TOKEN, CHANNEL_ID
    sm = SlackMessage(SLACK_BOT_TOKEN, CHANNEL_ID)
    sm.post_message(text="Hello world")
