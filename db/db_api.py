import os

from sqlalchemy import create_engine, Engine, exists, select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from db.models import Base, Service


class BotDB:
    def __init__(self):
        self.engine = self.get_db_engine()

    def is_service_exists(self, service_name: str, tg_id: int) -> None:
        with Session(self.engine) as session:
            return session.scalar(exists(Service)
                                  .where(Service.name == service_name, Service.tg_id == tg_id)
                                  .select())

    def delete_service(self, service_name: str, tg_id: int) -> bool:
        with Session(self.engine) as session:
            session.execute(delete(Service).where(Service.tg_id == tg_id, Service.name == service_name))
            session.commit()
            return True

    def get_service_login_password(self, service_name: str, tg_id: int) -> tuple[str, str]:
        with Session(self.engine) as session:
            service = session.scalar(select(Service).where(Service.tg_id == tg_id, Service.name == service_name))
            if service:
                return service.login, service.password
            return "", ""

    def save_service(self, service_data: list[str], tg_id: int) -> None:
        with Session(self.engine) as session:
            session.add(Service(tg_id=tg_id, name=service_data[0], login=service_data[1], password=service_data[2]))
            session.commit()

    def overwrite_service(self, service_data: list[str], tg_id: int) -> None:
        with Session(self.engine) as session:
            session.execute(update(Service)
                            .where(Service.tg_id == tg_id, Service.name == service_data[0])
                            .values(login=service_data[1], password=service_data[2]))
            session.commit()

    @staticmethod
    def get_db_engine() -> Engine:
        if os.getenv('DATABASE_URL'):
            engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
        else:
            engine = create_engine(
                f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}'
                f'@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}',
                echo=True)
        if not database_exists(engine.url):
            create_database(engine.url)

        Base.metadata.create_all(engine)
        return engine
