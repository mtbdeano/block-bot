import os
import discord
import logging
from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger


def setup_logging(log_level):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    json_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    json_handler.setFormatter(formatter)
    logger.addHandler(json_handler)


class BlockBotClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(__name__)

    async def on_ready(self):
        self.log.info('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        self.log.info('Message from {0.author}: {0.content}'.format(message))


if __name__ == "__main__":
    setup_logging(logging.INFO)
    load_dotenv()

    client = BlockBotClient()

    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)
