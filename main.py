import discord

token = "MTA0NDI3MDMwMjI3MzczNjcwNA.Gotgim.n8HEX34t1aTGY7Sd_Gn_tcRa-DxDZoJXHeFcSQ"


class WardB0t(discord.Client):
    async def on_ready(self):
        print("Bot online !")

    async def on_message(self, message):
        print("user:", message.author)
        print("content:", message.content)


intents = discord.Intents.default()
intents.message_content = True

bot = WardB0t(intents=intents)
bot.run(token)
