import flask_migrate
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None
__engine = None

def global_init(db_file):
    global __factory, __engine

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    __engine = sa.create_engine(conn_str, echo=False)

    __factory = orm.sessionmaker(bind=__engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(__engine)


def create_session() -> Session:
    global __factory
    return __factory()

def migrate(app, engine = __engine):
    __migrate = flask_migrate.Migrate(app ,engine)