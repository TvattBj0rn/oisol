import discord

## For debug purposes only
def view_ascii_embed(embed: discord.Embed):
    print(embed.title)
    if embed.description:
        print(embed.description)
    for field in embed.fields:
        print(field.name)
        print(field.value)
    if embed.footer:
        print(embed.footer)