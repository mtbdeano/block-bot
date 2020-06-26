import os
import discord
import logging
import json
from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger
from mcstatus import MinecraftServer


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
        self.uri = os.getenv("MINECRAFT_URI")
        first_char = self.uri.strip()[0]
        if first_char == '{' or first_char == '[':  # it's a json blob
            self.servers = json.loads(self.uri)
            if not isinstance(self.servers, list):
                self.servers = list(self.servers)  # force a list of one item
        else:
            self.servers = [{
                "server": self.uri.split(':')[0],
                "port": int(self.uri.split(':')[1]),
                "name": "Original Gansta"
                }]
        for s in self.servers:
            self.log.info(f'I will check {s["name"]} == {s["server"]}:{s["port"]}')
        self.eyes = None

    def lazy_init(self):
        if self.eyes is None:
            self.eyes = discord.utils.get(self.emojis, name='eyes') or '\N{EYES}'
            self.robot = discord.utils.get(self.emojis, name='robot') or "\U0001F916"  # robot!
            self.thumbsup = discord.utils.get(self.emojis, name='thumbsup') or '\N{THUMBS UP SIGN}'
            self.thumbsdown = discord.utils.get(self.emojis, name='thumbsdown') or '\N{THUMBS DOWN SIGN}'

    async def on_ready(self):
        self.log.info('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        self.lazy_init()
        self.log.debug(f'Message from {message.author}: {message.clean_content}')
        for mention in message.mentions:
            if mention == self.user:
                self.log.debug("its for us!")
                await self.process(message)

    async def status(self, message):
        # 'status' is supported by all Minecraft servers that are version 1.7 or higher.
        for server in self.servers:
            try:
                async with message.channel.typing():
                    await message.add_reaction(self.eyes)
                    self.log.debug(f'pinging {server["server"]}:{server["port"]}')
                    status = MinecraftServer.lookup(f'{server["server"]}:{server["port"]}')
                    smsg = f'The server {server["name"]} is up and has {status.players.online} players and replied in {status.latency} ms'
                    self.log.info(smsg)
                    await message.add_reaction(self.thumbsup)
            except Exception as err:
                self.log.error(err)
                await message.add_reaction(self.thumbsdown)
                await message.channel.send(f'nope, doesn\'t look like the {server["name"]} is up! {err}')

    async def identify(self, message):
        if message.author != self.user:
            # 'status' is supported by all Minecraft servers that are version 1.7 or higher.
            try:
                async with message.channel.typing():
                    await message.add_reaction(self.eyes)
                    mtbdeano = discord.utils.find(lambda m: m.name == 'mtbdeano', message.channel.guild.members)
                    smsg = "<@{}>, sigh, yes, I am a robot ... or am I <@{}> in disguise?".format(
                        message.author.id, mtbdeano.id)
                    self.log.info(smsg)
                    await message.add_reaction(self.robot)
                    await message.channel.send(smsg)
            except Exception as err:
                self.log.error(err)
                await message.add_reaction(self.thumbsdown)
                await message.channel.send(f'weird i can\'t identify myself! {err}')

    async def process(self, message):
        if '?' in message.clean_content and 'server' in message.clean_content.lower():
            # assume we are asking about the server, check connectivity
            self.log.debug("found a status question")
            await self.status(message)
        if 'robot' in message.clean_content.lower():
            await self.identify(message)


if __name__ == "__main__":
    setup_logging(logging.INFO)
    load_dotenv()

    client = BlockBotClient()

    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is not None and len(TOKEN) > 0:
        client.run(TOKEN)
