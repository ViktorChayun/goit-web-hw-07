import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


ENVIRONMENT = 'DEV'

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

user = config.get(ENVIRONMENT, 'USER')
password = config.get(ENVIRONMENT, 'PASS')
db = config.get(ENVIRONMENT, 'DB')
host = config.get(ENVIRONMENT, 'HOST')
port = config.get(ENVIRONMENT, 'PORT')

URI = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(URI, echo=True, pool_size=5, max_overflow=0)
DBSession = sessionmaker(bind=engine)
session = DBSession()