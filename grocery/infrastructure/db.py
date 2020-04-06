from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()


# We could also create a Session abstraction here if we didn't want to leak sqlalchemy dep
# all over the app
class DbSession:
    def __init__(self):
        engine = create_engine("postgresql://dev:secretpassw0rd@localhost:5432")
        self.session = sessionmaker(bind=engine)()

    def query(self, *args, **kwargs):
        return self.session.query(*args, **kwargs)

    def save(self, *args, **kwargs):
        return self.session.add(*args, **kwargs)

    def commit(self):
        try:
            return self.session.commit()
        except IntegrityError as e:
            raise ResourceConflictError(e)

    def rollback(self):
        return self.session.rollback()


class PersistenceError(RuntimeError):
    pass


class ResourceNotFoundError(PersistenceError):
    pass


class ResourceConflictError(PersistenceError):
    pass


def get_session() -> Session:
    return DbSession()


@contextmanager
def session():
    sess = get_session()
    try:
        yield sess
    except Exception as e:
        sess.rollback()
        raise e
    else:
        sess.commit()


def create_tables():
    Base.metadata.create_all(engine)
