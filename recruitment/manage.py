#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

def main():
    """Run administrative tasks."""
    # load_dotenv('./.env')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recruitment.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # if len(sys.argv) > 1:
    #     execute_from_command_line(sys.argv)
    # else:
    #     execute_from_command_line(['manage.py','runserver'])

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
