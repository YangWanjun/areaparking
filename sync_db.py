# coding: utf-8
import os
import sys
import getpass
import MySQLdb
import django
from django.core.management import call_command

# from contract import migrations as contract_migrations
# from employee import migrations as employee_migrations
# from format import migrations as format_migrations
# from master import migrations as master_migrations
# from parkinglot import migrations as parkinglot_migrations
# from turnover import migrations as turnover_migrations
# from whiteboard import migrations as whiteboard_migrations


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "areaparking.settings")
django.setup()

if sys.platform == 'win32' and getpass.getuser() == 'EB097':
    user = 'root'
    password = 'root'
    host = 'localhost'
else:
    user = 'root'
    password = 'root'
    host = 'localhost'


def main():
    del_migration_records()
    del_migration_files()
    migrate()


def migrate():
    call_command('migrate', '--fake')
    call_command('makemigrations', 'contract')
    call_command('makemigrations', 'employee')
    call_command('makemigrations', 'format')
    call_command('makemigrations', 'master')
    call_command('makemigrations', 'parkinglot')
    # call_command('makemigrations', 'turnover')
    call_command('makemigrations', 'whiteboard')
    call_command('migrate', '--fake')


def del_migration_records():
    con = MySQLdb.connect(user=user, passwd=password, db='areaparking', host=host)
    cursor = con.cursor()
    try:
        cnt = cursor.execute("delete from django_migrations")
        print('EXEC: delete from django_migrations. %s rows deleted' % cnt)
        con.commit()
    except Exception as e:
        con.roolback()
        raise e
    finally:
        cursor.close()
        con.close()


def del_migration_files():
    root_path = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(root_path):
        for filename in files:
            if filename in ('__init__.py', '__init__.pyc'):
                continue
            if os.path.basename(root) == 'migrations':
                path = os.path.join(root, filename)
                os.remove(path)
                print('DEL: %s' % path)


if __name__ == '__main__':
    main()
