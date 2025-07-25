class StockpileCore:
    @staticmethod
    def validate_stockpile_code(code: str) -> str | None:
        # Case where a user entered an invalid sized code
        if len(code) != 6:
            return '> The code must be a 6-digits code'

        # Case where a user entered a code without digits only
        if not code.isdigit():
            return '> The code contains non digit characters'

        return None

    @staticmethod
    def validate_stockpile_localisation(localisation: str) -> str | None:
        # Case where a user did not select a provided localisation
        if ' | ' not in localisation or localisation.startswith(' | '):
            return '> The localisation you entered is incorrect, displayed localisations are clickable'
        return None


    @staticmethod
    def validate_stockpile_ids(ids_list: list[str]) -> str | None:
        # Case where the user did not select the interface from the provided options
        if len(ids_list) != 4 or not all(ids.isdigit() for ids in ids_list[0:-1]):
            return '> The provided interface name is not correct'
        return None

