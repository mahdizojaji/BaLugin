from balebot import handlers, updater, filters
from balebot.models import base_models
from balebot.bot import Bot
from os import listdir, path, mkdir
from importlib import import_module
from termcolor import cprint as print
from configparser import ConfigParser, ExtendedInterpolation

rp = path.dirname(path.realpath(__file__))

# Bale Bot Authorization Token
updater = updater.Updater(
    token="194346805:1a9ca159b73492ae986a85ba24b67682356ee006",

)
# Define dispatcher
dispatcher = updater.dispatcher

def hi(a):
    pass

def _process_msgs(bot: Bot, update: base_models.FatSeqUpdate):
    for plugin in plugins_dir_list():
        plugin_import = import_module('plugins.{}'.format(plugin))
        func = plugin_import.returns.get('func')
        func(bot, update)


def plugins_dir_list():
    return [plug.rstrip('.py').strip() for plug in listdir(path.join(rp, 'plugins')) if
            plug.endswith(('.py', '.pyc')) and plug.endswith('.py')]


def create_config():
    """Create config file and Then write plugins status on config.
        on path: BaLugin/data/config.ini
        """
    print('\t>> Creating Config...', 'cyan')
    config = ConfigParser(interpolation=ExtendedInterpolation())  # Create instance of ConfigParser Class.
    config.add_section('Plugins')  # Add 'Plugins' Section To Write Plugins Status On This Section.
    for i in plugins_dir_list():
        config['Plugins'][i] = 'enabled'  # Enable All Plugins Of plugins directory.
    with open(path.join(rp, 'data', 'config.ini'), 'w') as file:
        config.write(file)  # write all changes to config.ini as finally
    print('end create config def')


def update_config_plugins():
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(path.join(rp, 'data', 'config.ini'))
    config.set('Plugins', 'plugins', 'enabled')
    for plug in config['Plugins']:
        if plug not in plugins_dir_list():
            config.remove_option('Plugins', plug)
    for plug in plugins_dir_list():
        if plug not in config['Plugins']:
            config['Plugins'][plug] = 'enabled'
    with open(path.join(rp, 'data', 'config.ini'), 'w') as file:
        config.write(file)


def check_config():
    print('\nChecking Config...', 'green')
    config = ConfigParser(interpolation=ExtendedInterpolation())
    if not path.isdir(path.join(rp, 'data')):
        print('not data folder')
        mkdir(path.join(rp, 'data'))
        print('created data folder')
    if not path.exists(path.join(rp, 'data', 'config.ini')):
        print('not config found')
        create_config()
    print('update config plugins')
    update_config_plugins()
    config.read(path.join(rp, 'data', 'config.ini'))
    if 'Plugins' not in config.sections():
        print('#! ["Plugins"] not in config sections. !#', 'red')
    print('Done!', 'magenta')


def main():
    check_config()
    dispatcher.add_handler(
        handlers.MessageHandler(
            filters.DefaultFilter(),
            _process_msgs
        )
    )
    # Run the bot!
    updater.run()


if __name__ == '__main__':
    main()
