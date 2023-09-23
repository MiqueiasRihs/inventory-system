INVENTORY_SIMPLE_DATA = [
    {
        "id": 1,
        "quantity": 10,
        "name": "Camisa"
    },
    {
        "id": 2,
        "quantity": 120,
    },
    {
        "id": 3,
        "quantity": 230,
    },
    {
        "id": 4,
        "quantity": 50,
    }
]

INVENTORY_FUTURE_DATA = [
    {
        "id": 2,
        "quantity": 10,
        "available_date": "21/09/2023"
    },
    {
        "id": 4,
        "quantity": 60,
        "available_date": "20/10/2023"
    }
]

INVENTORY_RESERVATION_DATA = [
    {
        "id": 3,
        "quantity": 50,
        "expiration_date": "23/11/2023",
        "status": "Ativo"
    }
]


def create_inventory_data(client):
    response = client.post("/estoque/estoque-fisico", json=INVENTORY_SIMPLE_DATA)
    return response

def create_future_inventory_data(client):
    response = client.post("/estoque/estoque-futuro", json=INVENTORY_FUTURE_DATA)
    return response

def create_inventory_reservation_data(client):
    response = client.post("/estoque/reserva", json=INVENTORY_RESERVATION_DATA)
    return response

        