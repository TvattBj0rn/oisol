USER_LOCALE_LOCALIZATION_ENGLISH = {
    'Translate': 'translate_command',

    'Command to display the current list of recruit with the date the got the recruit role': 'register_display_desc',

    'Create a new stockpile interface': 'stockpile_interface_create_desc',
    'Join an existing stockpile interface shared between multiple servers': 'stockpile_interface_join_desc',
    'Update up to 5 stockpiles codes from a list': 'refresh_code_desc',
    'Clear a specific interface': 'stockpile_clear_desc',
    'Clear a given interface, and its network if connected to other interfaces': 'stockpile_clear_desc_2',
    'Create a new stockpile on a given interface/network': 'stockpile_create_desc',
    'Create multiple stockpiles at once on a given interface/network': 'stockpile_bulk_create_desc',
    'Delete an existing stockpile on a given interface/network': 'stockpile_delete_desc',
    'Delete multiple existing stockpiles on a given interface/network': 'stockpile_bulk_delete_desc',

    'Create a new todolist interface, with possibility to limit usage to specific roles/users': 'todolist_generate_desc',

    'Command to add missing config, with possibility to reset the existing configuration': 'oisol_repair_desc',
    'Display the current server configuration': 'config_show_desc',
    'Set the recruit discord role, icons for recruits & promoted recruits': 'config_register_desc',
    'Set the language the bot uses for the server': 'config_language_desc',
    'Set the name of the group using the bot': 'config_name_desc',
    'Set the tag of the regiment group using the bot': 'config_tag_desc',
    'Set the shard of the group (default is Able)': 'config_shard_desc',
    'Set the faction of the group using the bot, this will impact the color of the stockpile interface': 'config_faction_desc',

    'Get a wiki infobox': 'wiki_desc',
    'List each required ammunition to destroy a given vehicle / structure': 'health_desc',
    'Production cost of a given entry, with all possibilities': 'production_desc',
}


USER_LOCALE_LOCALIZATION_DICT = {
    'french': {
        ## USER LOCALE
        # Module Translation
        'translate_command': 'Traduire',
        # Module Register
        'register_display_desc': "Affiche la liste des recrues et leur date d'obtention du rôle recrue",
        # Module Stockpiles
        'stockpile_interface_create_desc': 'Créer une nouvelle interface de stocks',
        'stockpile_interface_join_desc': "Rejoindre un réseau d'interfaces multi serveur",
        'refresh_code_desc': "Modifier jusqu'à 5 stockpiles",
        'stockpile_clear_desc': 'Nettoyer une interface',
        'stockpile_clear_desc_2': "Nettoyer une interface (et son réseau si connectée à d'autres interfaces)",
        'stockpile_create_desc': 'Créer un nouveau stock sur un(e) interface/réseau',
        'stockpile_bulk_create_desc': 'Créer plusieurs stocks sur un(e) interface/réseau',
        'stockpile_delete_desc': 'Supprimer un stock sur un(e) interface/réseau',
        'stockpile_bulk_delete_desc': 'Supprimer plusieurs stocks sur un(e) interface/réseau',
        # Module Todolist
        'todolist_generate_desc': 'Créer un nouvelle interface de tâches, avec limitation de rôles/utilisateurs possible',
        # Module Config
        'oisol_repair_desc': 'Compléter la configuration avec des éléments manquants, avec possibilité de reinitialiser la config',
        'config_show_desc': 'Afficher la configuration actuelle sur ce serveur',
        'config_register_desc': 'Définir le rôle recrue & les symboles recrues et recrues promues',
        'config_language_desc': 'Définir le langage que le bot utilise pour le serveur',
        'config_name_desc': 'Définir le nom de la guilde',
        'config_tag_desc': 'Definir le tag de la guilde',
        'config_shard_desc': 'Définir le serveur Foxhole de la guilde (Able par défaut)',
        'config_faction_desc': "Définir la faction de la guilde (cela impactera la couleur de l'interface de stocks)",
        # Module Wiki
        'wiki_desc': 'Afficher une infobox wiki',
        'health_desc': 'Afficher la liste des munitions pouvant détruire un véhicule/structure et leurs nombre',
        'production_desc': "Coûts de production d'une entrée wiki",
    },
    'portuguese': {
        ## USER LOCALE
        # Module Translation
        'translate_command': 'Traduzir',
        # Module Register
        'register_display_desc': 'Comando que exibe a lista atual do cargo recruta com a data em que receberam esse cargo',
        # Module Stockpiles
        'stockpile_interface_create_desc': 'Cria uma nova interface de stockpiles',
        'stockpile_interface_join_desc': 'Entra em uma interface de stockpiles existente compartilhada entre vários servidores',
        'refresh_code_desc': 'Atualiza até 5 códigos de stockpiles a partir de uma lista',
        'stockpile_clear_desc': 'Limpa uma interface específica',
        'stockpile_clear_desc_2': 'Limpa uma interface e sua rede de conexões, caso esteja conectada a outras interfaces',
        'stockpile_create_desc': 'Cria um novo stockpile em uma interface/rede específica',
        'stockpile_bulk_create_desc': 'Cria vários stockpiles de uma vez em uma interface/rede específica',
        'stockpile_delete_desc': 'Exclui um stockpile existente em uma interface/rede específica',
        'stockpile_bulk_delete_desc': 'Exclui vários stockpiles existentes em uma interface/rede específica',
        # Module Todolist
        'todolist_generate_desc': 'Cria uma nova interface de lista de tarefas com opção de limitar o uso a cargos/usuários específicos',
        # Module Config
        'oisol_repair_desc': 'Comando que adiciona configurações faltantes com possibilidade de redefinir a configuração existente',
        'config_show_desc': 'Exibe a configuração atual do servidor',
        'config_register_desc as well as the option to update or not the symbol on promotion': 'Define o cargo de recruta no Discord, os ícones para recrutas e recrutas promovidos, e a opção de atualizar (ou não) o símbolo na promoção',
        'config_language_desc': 'Define o idioma que o bot usa no servidor',
        'config_name_desc': 'Define o nome do regimento/grupo que está usando o bot',
        'config_tag_desc': 'Define a tag do regimento/grupo que está usando o bot',
        'config_shard_desc, this can impact the results of the stockpiles creation & health commands (shard dependant)': 'Define o shard do regimento/grupo (padrão: Able). Isso pode impactar os resultados dos comandos de criação de stockpiles e de status/saúde (dependem do shard)',
        'config_faction_desc': 'Define a facção do regimento/grupo que usa o bot. Isso afeta apenas a cor da interface de stockpiles',
        # Module Wiki
        'wiki_desc': 'Obtém uma infobox da wiki',
        'health_desc': 'Lista toda a munição necessária para destruir um veículo/estrutura específico',
        'production_desc': 'Exibe o custo de produção de um item específico, com todas as possibilidades',
    },
    'spanish': {
        ## USER LOCALE
        # Module Translation
        'translate_command': 'Traducir',
        # Module Register
        'register_display_desc': 'Comando para mostrar la lista actual de reclutas con la fecha en la que obtuvieron el rol de recluta',
        # Module Stockpiles
        'stockpile_interface_create_desc': 'Crear una nueva interfaz de existencias',
        'stockpile_interface_join_desc': 'Unirse a una interfaz de almacenamiento existente compartida entre varios servidores',
        'refresh_code_desc': 'Actualizar hasta 5 códigos de existencias de una lista',
        'stockpile_clear_desc': 'Borrar una interfaz específica',
        'stockpile_clear_desc_2': 'Borrar una interfaz determinada y su red si está conectada a otras interfaces',
        'stockpile_create_desc': 'Crear una nueva reserva en una interfaz/red determinada',
        'stockpile_bulk_create_desc': 'Crear múltiples reservas a la vez en una interfaz/red determinada',
        'stockpile_delete_desc': 'Eliminar una reserva existente en una interfaz/red determinada',
        'stockpile_bulk_delete_desc': 'Eliminar múltiples reservas existentes en una interfaz/red determinada',
        # Module Todolist
        'todolist_generate_desc': 'Nueva interfaz de tareas con acceso limitado por roles o usuarios.',
        # Module Config
        'oisol_repair_desc': 'Agregar configuración faltante, con posibilidad de restablecer la configuración existente',
        'config_show_desc': 'Mostrar la configuración actual del servidor',
        'config_register_desc as well as the option to update or not the symbol on promotion': 'Establese el rol de Discord del recluta, los íconos para los reclutas y los reclutas promovidos, así como la opción de actualizar o no el símbolo en la promoción.',
        'config_language_desc': 'Establese el idioma que utiliza el bot para el servidor',
        'config_name_desc': 'Establese el nombre del grupo usando el bot',
        'config_tag_desc': 'Establese la etiqueta del grupo del regimiento usando el bot',
        'config_shard_desc, this can impact the results of the stockpiles creation & health commands (shard dependant)': 'Establese el servidor del grupo (el valor predeterminado es Able), esto puede afectar los resultados de la creación de reservas y los comandos de estado (depende del servidor)',
        'config_faction_desc': 'Establese la facción que el bot usara , esto solo afectará el color de la interfaz.',
        # Module Wiki
        'wiki_desc': 'Obtener un cuadro de información wiki',
        'health_desc': 'Enumera cada munición necesaria para destruir un vehículo o estructura determinados.',
        'production_desc': 'Coste de producción de una entrada determinada, con todas las posibilidades',
    },
}
