from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest

from sql.database import Base
from app.main import app, get_db

from .utils import create_inventory_data, create_future_inventory_data, create_inventory_reservation_data, \
    INVENTORY_SIMPLE_DATA, INVENTORY_FUTURE_DATA, INVENTORY_RESERVATION_DATA

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@postgres-db:5432/solarfaciltest"

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


def test_register_product(test_db):
    response = client.post("/estoque/estoque-fisico", json=INVENTORY_SIMPLE_DATA[:1])
    
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'quantity': 10, 'name': None}]

def test_update_product_inventory(test_db):
    create_inventory_data(client)
    
    response = client.put("/estoque/estoque-fisico/1", json={"quantity": 15})

    assert response.status_code == 200
    assert response.json() == {'id': 1, 'quantity': 15, 'name': None}

def test_register_future_inventory(test_db):
    create_inventory_data(client)
    
    response = client.post("/estoque/estoque-futuro", json=INVENTORY_FUTURE_DATA)
    
    print(response.json())
    
    assert response.status_code == 200
    assert response.json() == [
        {'id': 2, 'quantity': 10, 'available_date': '2023-09-21', 'name': None},
        {'id': 4, 'quantity': 60, 'available_date': '2023-10-20', 'name': None}
    ]

def test_inventory_reservation(test_db):
    create_inventory_data(client)
    
    response = client.post("/estoque/reserva", json=INVENTORY_RESERVATION_DATA)
    
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'status': 'Ativo', 'quantity': 50, 'expiration_date': '2023-09-23', 'inventory_id': 3}]

def test_consult_inventory_estoque_fisico(test_db):
    create_inventory_data(client)
    create_future_inventory_data(client)
    create_inventory_reservation_data(client)

    response = client.post("/estoque/consulta/estoque-fisico", json=[
        {"id": 1, "quantity": 11},
        {"id": 3, "quantity": 120}
    ])
    
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'quantity': 11, 'stock_availability': 10, 'available': False},
        {'id': 3, 'quantity': 120, 'stock_availability': 180, 'available': True}
    ]

def test_consult_inventory_estoque_futuro(test_db):
    create_inventory_data(client)
    create_future_inventory_data(client)
    create_inventory_reservation_data(client)
    
    response = client.post("/estoque/consulta/estoque-futuro", json=[
        {"id": 1, "quantity": 11},
        {"id": 4, "quantity": 110}
    ])
    
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'quantity': 11, 'stock_availability': 10, 'available': False, 'inventory_available_date': None},
        {'id': 4, 'quantity': 110, 'stock_availability': 110, 'available': True, 'inventory_available_date': '20/10/2023'}
    ]
