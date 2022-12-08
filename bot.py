#!/usr/bin/python3
import discord
from discord.ext import commands
import toml

config = toml.loads(open('config.toml', 'r').read())
token = config['token']


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=discord.Intents.all(),
            application_id=config['app_id']
        )

    async def on_ready(self):
        print(f"{self.user} has connected successfully.")

    async def setup_hook(self):
        await self.load_extension(f"cogs.chatgpt")
        await bot.tree.sync(guild=discord.Object(id=config['guild']))


bot = Bot()
bot.run(token)
