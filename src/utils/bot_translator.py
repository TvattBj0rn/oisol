import discord
from discord import app_commands


class OisolTranslator(app_commands.Translator):
    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContext,
    ) -> str | None:
        sentence = str(string)
        match locale:
            case discord.Locale.french:
                return self.__french_translation(sentence)
        return None

    @staticmethod
    def __french_translation(message: str) -> str | None:
        if message == 'Traduire':
            return 'Traduire'
        elif message == '__General config__':
            return '__Configuration Globale__'
        return None