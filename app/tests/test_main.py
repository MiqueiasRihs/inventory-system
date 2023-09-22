from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest

from sql.database import Base
from app.main import app, get_db

from app.config import settings

from .utils import create_inventory_data, create_future_inventory_data, create_inventory_reservation_data, \
    INVENTORY_SIMPLE_DATA, INVENTORY_FUTURE_DATA, INVENTORY_RESERVATION_DATA

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@postgres-db:5432/solfaciltest"

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

import pdb; pdb.set_trace();

def test_register_product(test_db):
    response = client.post("/estoque/estoque-fisico", json=INVENTORY_SIMPLE_DATA[:1])
    
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'quantity': 10, 'name': 'Camisa'}]
    

def test_register_duplicated_product(test_db):
    create_inventory_data(client)
    response = client.post("/estoque/estoque-fisico", json=INVENTORY_SIMPLE_DATA[:1])
    
    assert response.status_code == 400
    assert response.json() == {'detail': 'O produto com ID 1 já existe, tente atualizá-lo'}
    

def test_register_product_invalid_data(test_db):
    response = client.post("/estoque/estoque-fisico", json=[{
        "id": 1,
        "quantity": -100
    }])
    
    assert response.status_code == 422

def test_update_product_inventory(test_db):
    create_inventory_data(client)
    
    response = client.put("/estoque/estoque-fisico/1", json={"quantity": 15})

    assert response.status_code == 200
    assert response.json() == {'id': 1, 'quantity': 15, 'name': 'Camisa'}
    

def test_update_nonexistent_product_inventory(test_db):
    response = client.put("/estoque/estoque-fisico/1", json={"quantity": 15})
    
    assert response.status_code == 400
    assert response.json() == {'detail': 'Este produto não existe, tente cria-lo antes'}
    

def test_update_product_inventory_negative_quantity(test_db):
    create_inventory_data(client)
    
    response = client.put("/estoque/estoque-fisico/1", json={"quantity": -10})
    assert response.status_code == 422
    

def test_update_product_inventory_null_quantity(test_db):
    create_inventory_data(client)
    
    response = client.put("/estoque/estoque-fisico/1", json={"quantity": None})
    assert response.status_code == 422

def test_register_future_inventory(test_db):
    create_inventory_data(client)
    
    response = client.post("/estoque/estoque-futuro", json=INVENTORY_FUTURE_DATA)
    
    assert response.status_code == 200
    assert response.json() == [
        {'id': 2, 'quantity': 10, 'available_date': '2023-09-21', 'name': None},
        {'id': 4, 'quantity': 60, 'available_date': '2023-10-20', 'name': None}
    ]
    

def test_register_future_inventory_invalid_date(test_db):
    create_inventory_data(client)
    
    response = client.post("/estoque/estoque-futuro", json=[{
        "id": 2,
        "quantity": 10,
        "available_date": "221/19/2023"
    }])
    
    assert response.status_code == 422
    

def test_register_future_inventory_invalid_quantity(test_db):
    create_inventory_data(client)
    
    response = client.post("/estoque/estoque-futuro", json=[{
        "id": 2,
        "quantity": -10,
        "available_date": "21/09/2023"
    }])
    
    assert response.status_code == 422
    

def test_register_future_inventory_null_quantity(test_db):
    create_inventory_data(client)
    
    response = client.post("/estoque/estoque-futuro", json=[{
        "id": 2,
        "available_date": "21/09/2023"
    }])
    
    assert response.status_code == 422


def test_inventory_reservation(test_db):
    create_inventory_data(client)
    
    response = client.post("/estoque/reserva", json=INVENTORY_RESERVATION_DATA)
    
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'status': 'Ativo', 'quantity': 50, 'expiration_date': '2023-10-23', 'inventory_id': 3}
    ]


def test_nonexistent_inventory_reservation(test_db):
    response = client.post("/estoque/reserva", json=INVENTORY_RESERVATION_DATA)
    
    assert response.status_code == 400
    assert response.json() == {'detail': 'Não é possivel realizar a reserva pois o produto com ID 3 não existe'}


def test_inventory_reservation_more_than_inventory_quantity(test_db):
    create_inventory_data(client)
    
    response = client.post("/estoque/reserva", json=[{
        "id": 3,
        "quantity": 300,
        "expiration_date": "23/09/2023",
        "status": "Ativo"
    }])
    
    assert response.status_code == 400
    assert response.json() == {'detail': 'Não é possivel reservar pois não existe estoque suficiente para o produto com ID 3, o estoque atual é 230'}


def test_inventory_reservation_invalid_date(test_db):
    create_inventory_data(client)
    
    response = client.post("/estoque/reserva", json=[{
        "id": 3,
        "quantity": 10,
        "expiration_date": "223/109/2023",
        "status": "Ativo"
    }])
    
    assert response.status_code == 422


def test_inventory_reservation_invalid_quantity(test_db):
    create_inventory_data(client)
    
    response = client.post("/estoque/reserva", json=[{
        "id": 3,
        "quantity": -65,
        "expiration_date": "23/09/2023",
        "status": "Ativo"
    }])
    
    assert response.status_code == 422


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


def test_consult_inventory_estoque_fisico_nonexistent_products(test_db):
    response = client.post("/estoque/consulta/estoque-fisico", json=[
        {"id": 10, "quantity": 5},
        {"id": 11, "quantity": 10}
    ])

    assert response.status_code == 200
    assert response.json() == [
        {'id': 10, 'quantity': 5, 'stock_availability': 0, 'available': False},
        {'id': 11, 'quantity': 10, 'stock_availability': 0, 'available': False}
    ]


def test_consult_inventory_estoque_fisico_without_reserve(test_db):
    create_inventory_data(client)
    
    response = client.post("/estoque/consulta/estoque-fisico", json=[
        {"id": 1, "quantity": 10}
    ])

    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'quantity': 10, 'stock_availability': 10, 'available': True}]


def test_consult_inventory_estoque_fisico_with_reserve(test_db):
    create_inventory_data(client)
    create_inventory_reservation_data(client)
    
    response = client.post("/estoque/consulta/estoque-fisico", json=[
        {"id": 3, "quantity": 200}
    ])

    assert response.status_code == 200
    assert response.json() == [{'id': 3, 'quantity': 200, 'stock_availability': 180, 'available': False}]


def test_consult_inventory_estoque_fisico_with_no_stock(test_db):
    response = client.post("/estoque/consulta/estoque-fisico", json=[
        {"id": 100, "quantity": 200}
    ])
    
    assert response.status_code == 200
    assert response.json() == [{'id': 100, 'quantity': 200, 'stock_availability': 0, 'available': False}]


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


def test_consult_inventory_estoque_futuro_nonexistent_products(test_db):
    response = client.post("/estoque/consulta/estoque-futuro", json=[
        {"id": 10, "quantity": 5},
        {"id": 11, "quantity": 10}
    ])
    
    print(response.json())
    
    assert response.status_code == 200
    assert response.json() == [
        {'id': 10, 'quantity': 5, 'stock_availability': 0, 'available': False, 'inventory_available_date': None},
        {'id': 11, 'quantity': 10, 'stock_availability': 0, 'available': False, 'inventory_available_date': None}
    ]


def test_consult_inventory_estoque_futuro_without_future_stock(test_db):
    create_inventory_data(client)
    create_inventory_reservation_data(client)
    
    response = client.post("/estoque/consulta/estoque-futuro", json=[
        {"id": 1, "quantity": 10}
    ])
    
    assert response.status_code == 200
    assert response.json() == [{
        'id': 1, 'quantity': 10, 'stock_availability': 10, 'available': True, 'inventory_available_date': None
    }]


def test_consult_inventory_estoque_futuro_with_future_stock(test_db):
    create_inventory_data(client)
    create_future_inventory_data(client)
    
    response = client.post("/estoque/consulta/estoque-futuro", json=[
        {"id": 4, "quantity": 50}
    ])
    
    assert response.status_code == 200
    assert response.json() == [{
        'id': 4, 'quantity': 50, 'stock_availability': 110, 'available': True, 'inventory_available_date': '20/10/2023'
    }]


def test_consult_inventory_estoque_futuro_with_no_stock(test_db):
    response = client.post("/estoque/consulta/estoque-futuro", json=[
        {"id": 100, "quantity": 200}
    ])
    
    assert response.status_code == 200
    assert response.json() == [{
        'id': 100, 'quantity': 200, 'stock_availability': 0, 'available': False, 'inventory_available_date': None
    }]