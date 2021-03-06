import configparser
import logging
import click
from framework.Core import Core
from framework.PluginLoader import PluginLoader

# Bootstrap the application
core = Core()

# Read settings
config = configparser.ConfigParser()
config.read('Settingfile')
debug = config['general'].getboolean('debug')


# Register commands and plugins
@click.group()
@click.pass_context
def framework(ctx, connection):
    pass


@click.group(cls=PluginLoader)
@click.pass_context
def plugins(ctx):
    pass


@framework.command(name='connection:list')
@click.pass_context
def list_connections(ctx):
    """ Lists all connections. """

    core.connection_manager.print_connections()


@framework.command(name='connection:show')
@click.argument('name')
def show_connection(name):
    """ Show a connection for a given name. """

    print(core.connection_manager.get_connection(name))
    

@framework.command(name='connection:hash')
@click.argument('name')
def hash_connection(name):
    """ Returns a hash for a given connection name. """

    print(core.database_identifier.get_hash(name))


@framework.command(name='connection:guess')
@click.argument('name')
def guess_connection(name):
    """ Tries to find a matching plugin by using a similarity hash for a given connection name. """

    core.database_identifier.print_guesses(name)


@framework.command(name='plugin:list')
def list_plugins():
    """ Lists all plugins. """

    core.plugin_manager.print_plugins()


@framework.command(name='plugin:show')
@click.argument('name')
def show_plugin(name):
    """ Show a plugin with a given name. """

    print(core.plugin_manager.get_plugin(name))


@click.command(cls=click.CommandCollection, sources=[framework, plugins])
@click.option('--connection', help='Name of connection')
@click.option('--export', help='Format of output file')
@click.option('--output', help='Path of output file')
@click.pass_context
def cli(ctx, connection, export, output):
    core.init(connection, export, output)


# Run the application
try:
    cli(obj={})
    exit(0)
except Exception as exception:
    if debug:
        logging.exception(exception)
    else:
        print("Error: " + exception.__str__())
        print("(Enable debug in Settingfile for more info)")
    exit(1)
