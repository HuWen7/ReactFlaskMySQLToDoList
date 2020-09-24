from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from constant import MYSQL_URL

engine = create_engine(MYSQL_URL)
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))