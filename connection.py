import os
import getpass
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DIRNAME = os.path.dirname(__file__)


def _create_config_file():
    import shutil

    path = os.path.join(DIRNAME, 'connection_config.json')
    src_path = os.path.join(DIRNAME, 'connection_config_default.json')

    shutil.copy2(src_path, path)


def _load_config():
    try:
        path = os.path.join(DIRNAME, 'connection_config.json')
        with open(path) as f:
            d = json.load(f)
    except FileNotFoundError:
        _create_config_file()
        return _load_config()

    host = d['host']
    port = d['port']
    database = d['database']
    return host, port, database


HOST, PORT, DATABASE = _load_config()


def create_session(*, user=getpass.getuser(), password=None, echo=False):
    if password is None:
        getpass.getpass('Enter password for user "{}"'.format(user))

    engine = create_engine(
        'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(user, password, HOST, PORT, DATABASE), echo=echo
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_local_session(*, user=getpass.getuser(), echo=False):
    engine = create_engine(
        'postgresql+psycopg2://{}@{}:{}/{}'.format(user, 'localhost', PORT, DATABASE), echo=echo
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def get_password_from_pgpass_win(user=getpass.getuser()):
    path = os.path.expandvars(r'%APPDATA%\postgresql\pgpass.conf')
    if not os.path.isfile(path):
        raise FileNotFoundError('File "{}" does not exists!'.format(path))

    with open(path) as f:
        data = f.read().strip().split('\n')

    data = (row.strip() for row in data if row != '' and not row.startswith('#'))

    target_user = user
    for row in data:
        try:
            items = row.split(':')
            host, port, db, user, passw = items
            match = (
                    (host == HOST or host == '*') and
                    (db == DATABASE or db == '*') and
                    (port == '*' or int(port) == PORT) and
                    (user == target_user or user == '*')
            )
            if match:
                return passw
        except Exception:
            pass
    raise RuntimeError('There is no configuration in "pgpass.conf" which match parameters!')
