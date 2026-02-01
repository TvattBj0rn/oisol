import discord
from discord import app_commands

from src.utils.localization import USER_LOCALE_LOCALIZATION_DICT, USER_LOCALE_LOCALIZATION_ENGLISH


class OisolTranslator(app_commands.Translator):
    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContext,
    ) -> str | None:

        if (string_id := USER_LOCALE_LOCALIZATION_ENGLISH.get(str(string))) is None:
            return None

        match locale:
            case discord.Locale.french:
                return USER_LOCALE_LOCALIZATION_DICT['french'].get(string_id)
            # case discord.Locale.spain_spanish | discord.Locale.latin_american_spanish:
            #     return USER_LOCALE_LOCALIZATION_DICT['spanish'].get(string_id)
            case discord.Locale.brazil_portuguese:
                return USER_LOCALE_LOCALIZATION_DICT['portuguese'].get(string_id)
        return None
