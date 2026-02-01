import discord
from discord import app_commands

from src.utils.localization import USER_LOCALE_LOCALIZATION_DICT


class OisolTranslator(app_commands.Translator):
    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContext,
    ) -> str | None:
        sentence = str(string)
        print(sentence)
        match locale:
            case discord.Locale.french:
                return USER_LOCALE_LOCALIZATION_DICT['french'][sentence]
            case discord.Locale.spain_spanish | discord.Locale.latin_american_spanish:
                return USER_LOCALE_LOCALIZATION_DICT['spanish'][sentence]
            case discord.Locale.brazil_portuguese:
                return USER_LOCALE_LOCALIZATION_DICT['portuguese'][sentence]
        return sentence
