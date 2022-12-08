import discord
from discord import app_commands
from discord.ext import commands
import time
import toml
import requests
import uuid
import json

frontend_api = "https://chat.openai.com/api"
backend_api = "https://chat.openai.com/backend-api"
session = toml.loads(open('config.toml', 'r').read())['session']
userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
config = toml.loads(open('config.toml', 'r').read())
accessToken = ""


def send_message(message, parentMessage, interaction: discord.Interaction, startTime) -> discord.Embed():
    global accessToken

    if session == "":
        print("Please enter a valid session")
        return "Not a valid session"
    if accessToken == "":
        accessToken = refresh_access_token()

    uuid1 = str(uuid.uuid4())

    data = {
        'action': 'next',
        'messages': [
            {
                'id': uuid1,
                'role': 'user',
                'content': {
                    'content_type': 'text',
                    'parts': [message]
                }
            }
        ],
        'model': 'text-davinci-002-render',
        'parent_message_id': parentMessage
    }

    headers = {
        'Authorization': f'Bearer {accessToken}',
        'Content-Type': 'application/json',
        'user-agent': userAgent
    }

    url = f"{backend_api}/conversation"

    print(f"Sending '{message}'")

    r = requests.post(url, json=data, headers=headers)

    data = "{" + r.text.split("data: {")[len(r.text.split("data: {")) - 1].split('data: [DONE]')[0]

    jsonData = json.loads(data)

    print(f"Received response in {round((time.time() - startTime) * 10) / 10}s")

    embed = discord.Embed()

    embed.title = message
    embed.colour = 16777214
    embed.set_author(name=f"OpenAI - {interaction.user.name}",
                     icon_url="https://static-00.iconduck.com/assets.00/openai-icon-505x512-pr6amibw.png")
    embed.set_footer(
        text=f"\nGenerated response in {round((time.time() - startTime) * 10) / 10}s\n\nid: {jsonData['message']['id']}\nconversation_id: {jsonData['conversation_id']}")

    fullText = ""

    for part in jsonData['message']['content']['parts']:
        fullText += part
    embed.description = fullText[0:4096]
    for field in [fullText[i+4096:i+5120] for i in range(4096, len(fullText), 1024)]:
        embed.add_field(name="", value=field, inline=False)

    return embed


def refresh_access_token():
    headers = {
        'cookie': f'__Secure-next-auth.session-token={session}',
        'user-agent': userAgent
    }

    r = requests.get("https://chat.openai.com/api/auth/session", headers=headers)

    return r.text.split('"accessToken":"')[1].split('"}')[0]


class ChatGPT(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="chatgpt", description="Requests your message from the ChatGPT Servers")
    async def chat_gpt(self, interaction: discord.Interaction, message: str):
        startTime = time.time()

        await interaction.response.send_message("Loading...")

        embed = send_message(message, str(uuid.uuid4()), interaction, startTime)

        await interaction.edit_original_response(content="", embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        ChatGPT(bot),
        guilds=[discord.Object(id=config['guild'])]
    )