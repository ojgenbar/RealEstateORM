import os
import getpass
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DIRNAME = os.path.dirname(__file__)


def _load_config():
    path = os.path.join(DIRNAME, 'connection_config.json')
    with open(path) as f:
        d = json.load(f)
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
