import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from app.config.settings import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


class DBConnection:
    def __init__(self) -> None:
        self.engine = None
        self._session = None

    def init_app(self) -> None:
        self.engine = create_engine(
            url="postgresql://{user}:{password}@{host}:{port}/{name}".format(
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                name=settings.DB_NAME,
            ),
            pool_size=settings.SQLALCHEMY_POOL_SIZE,
        )
        self._session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )

    def startup(self):
        logger.info(f"db.startup - {self.engine.url.render_as_string()}")
        self.engine.connect()

    def shutdown(self):
        self._session.close_all()
        self.engine.dispose()
        logger.info(f"db.shutdown - {self.engine.url.render_as_string()}")

    def get_session(self) -> Session:
        session = self._session()
        try:
            yield session
        finally:
            session.close()

    @property
    def session(self):
        return self.get_session
