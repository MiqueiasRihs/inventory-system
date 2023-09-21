from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import pytest

from ..sql.database import Base
from ..main import app, get_db

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@postgres-db:5432/mydatabasetest"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# Testes para a rota /estoque/estoque-fisico
def test_register_product(test_db):
    response = client.post("/estoque/estoque-fisico", json=[
        {"id": 1, "quantity": 10},
        {"id": 2, "quantity": 20}
    ])
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_update_product_inventory(test_db):
    response = client.put("/estoque/estoque-fisico/1", json={"quantity": 15})
    assert response.status_code == 200
    assert response.json()["quantity"] == 15

# Testes para a rota /estoque/estoque-futuro
def test_register_future_inventory(test_db):
    response = client.post("/estoque/estoque-futuro", json=[
        {"id": 1, "quantity": 50},
        {"id": 2, "quantity": 30}
    ])
    assert response.status_code == 200
    assert len(response.json()) == 2

# Testes para a rota /estoque/reserva
def test_inventory_reservation(test_db):
    response = client.post("/estoque/reserva", json=[
        {"id": 1, "quantity": 5},
        {"id": 2, "quantity": 25}
    ])
    assert response.status_code == 200
    assert len(response.json()) == 2

# Testes para a rota /estoque/consulta/{strategy}
def test_consult_inventory_estoque_fisico(test_db):
    response = client.post("/estoque/consulta/estoque-fisico", json=[
        {"id": 1, "quantity": 10},
        {"id": 2, "quantity": 15}
    ])
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert all("stock_availability" in item for item in response.json())

def test_consult_inventory_estoque_futuro(test_db):
    response = client.post("/estoque/consulta/estoque-futuro", json=[
        {"id": 1, "quantity": 10},
        {"id": 2, "quantity": 15}
    ])
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert all("inventory_available_date" in item for item in response.json())
