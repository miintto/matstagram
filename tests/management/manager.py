from fastapi.testclient import TestClient
import pytest

from app.config.router import router
from app.common.models import Base
from app.config.connection import db
from app.main import app

client = TestClient(app)


class TestManager:
    def create_table(self):
        Base.metadata.create_all(bind=db.engine)

    def drop_table(self):
        Base.metadata.drop_all(bind=db.engine)

    def create_root_user(self):
        response = client.post(
            url="/api/auth/signup",
            json={
                "user_email": "matstagram@test.com",
                "password": "1234",
                "password_check": "1234",
            },
        )
        if response.status_code != 201:
            raise ValueError(f"생성 실패: {response.text}")

    def setUpTestCase(self):
        self.create_table()
        self.create_root_user()

    def tearDownTestCase(self):
        self.drop_table()

    def run(self):
        db.init_app()
        self.setUpTestCase()
        pytest.main()
        self.tearDownTestCase()
