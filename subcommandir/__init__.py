import inspect
from pathlib import Path
import pkgutil
from importlib import import_module

from django.core.management import BaseCommand as MostBaseCommand, CommandError, get_commands


class BaseCommand(MostBaseCommand):
    subcommand_dir: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.subcommand_dir:
            raise CommandError('Invalid subcommand_dir field')

        self.command_name = self.__class__.__module__.rsplit('.', maxsplit=1)[-1]
        try:
            self.app_name = get_commands()[self.command_name]
        except KeyError:
            raise CommandError(f'Unknown command: {self.command_name}')

        subcommand_path = Path(inspect.getfile(self.__class__)).resolve().parent / self.subcommand_dir
        self.subcommands = self.find_commands(str(subcommand_path))
        self.argv = []

    def run_from_argv(self, argv):
        self.argv = argv

        super(BaseCommand, self).run_from_argv(argv)

    def load_command_class(self, app_name, name):
        module = import_module('%s.management.commands.%s.%s' % (app_name, self.subcommand_dir, name))
        command = module.Command(stdout=self.stdout, stderr=self.stderr)
        command.requires_system_checks = False
        return command

    def find_commands(self, command_dir):
        return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
                if not is_pkg and not name.startswith('_')]

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='subcommand', title='subcommand', description='Subcommand')
        subparsers.required = True
        for subcommand in [self.argv[2]] if self._called_from_command_line else self.subcommands:
            command = self.load_command_class(self.app_name, subcommand)
            if len(self.argv): command._called_from_command_line = True
            subparser = subparsers.add_parser(subcommand, help=command.__class__.help)
            command.add_arguments(subparser)
            command_parser = command.create_parser(
                self.argv and self.argv[0] or '', self.argv and self.argv[1] or self.command_name)
            subparser._actions = command_parser._actions

    def handle(self, *args, **options):
        subcommand = options.pop('subcommand')
        if subcommand not in self.subcommands:
            raise CommandError('Invalid argument for subcommand')

        command = self.load_command_class(self.app_name, subcommand)
        if self._called_from_command_line:
            return command.run_from_argv([self.argv[0]] + self.argv[2:])
        return command.execute(*args, **options)
