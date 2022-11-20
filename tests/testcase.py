import os

from fastapi.testclient import TestClient
from app.common.models import Base

os.environ.setdefault("APP_ENV", "test")


class BaseTestCase:
    @classmethod
    def setup_class(cls):
        from app.config.connection import db
        from app.main import app

        assert app.extra.get("env") == "test"

        cls.db = db
        cls.client = TestClient(app)
        cls()._create_table()

    @classmethod
    def teardown_class(cls):
        cls()._drop_table()

    def _create_table(self):
        Base.metadata.create_all(bind=self.db.engine)

    def _drop_table(self):
        Base.metadata.drop_all(bind=self.db.engine)

    def _create_root_user(self):
        response = self.client.post(
            url="/api/auth/signup",
            json={
                "user_email": "matstagram@test.com",
                "password": "1234",
                "password_check": "1234",
            },
        )
        if response.status_code != 201:
            raise ValueError(f"생성 실패: {response.text}")
