import discord
from discord import app_commands
from discord.ext import commands


class ModuleSingleCommands(commands.Cog):
    def __init__(self, bot):
        self.oisol = bot

    @app_commands.command(name='refresh_nicknames', description='refresh each member name depending on its highest role')
    async def refresh_nicknames(self, interaction: discord.Interaction):
        await interaction.response.defer()
        guild_members = list(interaction.guild.members)
        for guild_member in guild_members:
            if len(guild_member.display_name) > 24:
                continue
            if guild_member.get_role(1125790881111359494):
                if guild_member.display_name[:8] != '[FCF] ⁂ ':
                    await guild_member.edit(nick=f'[FCF] ⁂ {guild_member.display_name}')
                continue
            if guild_member.get_role(1125790881111359493):
                if guild_member.display_name[:8] != '[FCF] ⁑ ':
                    await guild_member.edit(nick=f'[FCF] ⁑ {guild_member.display_name}')
                continue
            if guild_member.get_role(1125790881094570053):
                if guild_member.display_name[:8] != '[FCF] ∗ ':
                    await guild_member.edit(nick=f'[FCF] ∗ {guild_member.display_name}')
                continue
            if guild_member.get_role(1147568458532409474):
                if guild_member.display_name[:8] != '[FCF] ✪ ':
                    await guild_member.edit(nick=f'[FCF] ✪ {guild_member.display_name}')
                continue
            if guild_member.get_role(1125790881094570046):
                if guild_member.display_name[:8] != '[FCF] ⦿ ':
                    await guild_member.edit(nick=f'[FCF] ⦿ {guild_member.display_name}')
                continue
            if guild_member.get_role(1125790881094570045):
                if guild_member.display_name[:2] != '⦾ ':
                    await guild_member.edit(nick=f'⦾ {guild_member.display_name}')
                continue
        await interaction.followup.send('> Les pseudos des membres ont bien été mis à jour', ephemeral=True)
