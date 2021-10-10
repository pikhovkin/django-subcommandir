# django-subcommandir

[![GitHub Actions](https://github.com/pikhovkin/django-subcommandir/workflows/build/badge.svg)](https://github.com/pikhovkin/django-subcommandir/actions)
[![PyPI](https://img.shields.io/pypi/v/django-subcommandir.svg)](https://pypi.org/project/django-subcommandir/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-subcommandir.svg)
[![framework - Django](https://img.shields.io/badge/framework-Django-0C3C26.svg)](https://www.djangoproject.com/)
![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-subcommandir.svg)
[![PyPI - License](https://img.shields.io/pypi/l/django-subcommandir)](./LICENSE)

Django subcommands in subdirectories

### Installation

```bash
$ pip install django-subcommandir
```

### Example of usage

```bash
my_app
├── ...
├── management
│   ├── commands
│   │   ├── __init__.py
│   │   ├── load
│   │   │   ├── __init__.py
│   │   │   ├── month_report.py
│   │   │   └── year_report.py
│   │   ├── my_app_load.py
│   ├── __init__.py
```

```python
# .../management/commands/my_app_load.py
from subcommandir import BaseCommand

class Command(BaseCommand):
    subcommand_dir = 'load'
```
```python
# .../management/commands/load/month_report.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--start', ...)
        ...

    def handle(self, *args, **options):
        ...
```

Command calls:
```bash
$ python manage.py my_app_load year_report
$ python manage.py my_app_load month_report --start="2021-01" --end="2021-02"
```
or
```python
from django.core.management import call_command

def load_year_report():
    call_command('my_app_load', 'year_report')
    
def load_month_report():
    call_command('my_app_load', 'month_report', start=...)
```

## License

MIT
