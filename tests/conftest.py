from httpx import AsyncClient
import pytest_asyncio
from sqlalchemy import delete

from app.api.user.models import AuthUser
from app.config.connection import db
from app.main import app

fixture_root_email = "matstagram@test.com"
fixture_root_password = "1234"


client = AsyncClient(app=app, base_url="http://test.nolbal.com")


@pytest_asyncio.fixture(scope="function")
async def session():
    async with db._session() as session:
        try:
            yield session
        finally:
            await session.close()
    await db._session.remove()
    await db.engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def create_root_user(session):
    response = await client.post(
        url="/api/auth/signup",
        json={
            "user_email": fixture_root_email,
            "password": fixture_root_password,
            "password_check": fixture_root_password,
        },
    )
    assert response.status_code == 200
    yield response.json()
    await session.execute(
        delete(AuthUser).where(AuthUser.user_email == fixture_root_email)
    )
    await session.commit()
