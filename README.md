# ChatGPTBot

## Configuration

Create a file in the bot.py directory named `config.toml`
Open it with a text editor and add the following lines:
```
session = ""

token = ""
app_id = ""
guild = ""
```
  
To get your session, go to `https://chat.openai.com/chat` and open Inspect Element
> Open the `Application` tab (You may need to press the >> Icon to find it)

> Open the Cookies tab under Storage

> Click on `https://chat.openai.com`

> Copy the `Value` field of the cookie called `__Secure-next-auth.session-token`

> Paste the value into the `session` quotes inside your `config.toml`

To get your token, create a discord bot on `https://discord.com/developers/applications`
> Open the `Bot` tab and press `Add Bot`

> Customize the bot's name and profile picture to your liking

> Press the `Reset Token` button and copy the token

> Paste the value into the `token` quotes inside your `config.toml`

To get your application id, go to the `General Information` tab of the Discord Developer Portal
> Press the `Copy` button under `Application ID`

> Paste the value into the `app_id` quotes inside your `config.toml`

To get your guild id, open Discord
> Open your Discord settings

> Go into the `Advanced` tab under `App Settings`

> Ensure `Developer Mode` is on

> Right click on the server you wish to have the bot in

> Press `Copy ID` at the bottom of the pop-up

> Paste the value into the `guild` quotes inside your `config.toml`
