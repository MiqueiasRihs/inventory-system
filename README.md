# SolFácil Inventory Management API 

Our API plays a important role in our new venture: SolFácil's expansion into the market of solar system and solar product sales through our very own E-commerce platform. To ensure precise control over the products available on our platform, we've developed this inventory management API. With it, we streamline communication and integration between our E-commerce system and our product inventory, ensuring an efficient flow of information for our customers and internal teams.

**Technologies Used:**

- **FastAPI:** Our API is powered by FastAPI, a modern and fast web framework for building APIs with Python. It offers automatic interactive documentation and validation, making development a breeze.

- **Docker:** We've containerized our application using Docker, which allows for easy deployment and ensures consistent environments across different setups.

- **PostgreSQL:** For robust data storage, we rely on PostgreSQL, a powerful open-source relational database management system.

By combining these technologies, we've created a dependable inventory management solution that's easy to set up and ensures your API is always in sync with your database.

## How to Run

To run this API using Docker Compose, follow these steps:

1. Clone this repository.
2. Navigate to the project directory.
3. Run the following command to build and start the containers:

```bash
docker-compose up
```

4. The API will be accessible at `http://localhost:8000`.

## API Endpoints

### 1. Register Physical Products

**Endpoint:** `/estoque/estoque-fisico`  
**Method:** `POST`  
**Description:** Register one or more physical inventory products.  
**Request Body:**   

```json
[
    {
        "id": 1,
        "name": "Product 1",
        "quantity": 10
    },
    {
        "id": 2,
        "name": "Product 2",
        "quantity": 20
    }
]
```

**Response:** 
- **Status Code:** 200 (OK)

```json
[
    {
        "id": 1,
        "name": "Product 1",
        "quantity": 10
    },
    {
        "id": 2,
        "name": "Product 2",
        "quantity": 20
    }
]
```

### 2. Update Physical Product Inventory

**Endpoint:** `/estoque/estoque-fisico/{product_id}`  
**Method:** `PUT`  
**Description:** Update the inventory quantity of a specific physical product by its ID.  
**Request Parameters:** 

- `product_id` (int)
  
**Request Body:**   

```json
{
    "quantity": 30
}
```

**Response:** 
- **Status Code:** 200 (OK)

```json
{
    "id": 1,
    "name": "Product 1",
    "quantity": 30
}
```

### 3. Register Future Inventory

**Endpoint:** `/estoque/estoque-futuro`  
**Method:** `POST`  
**Description:** Register future inventory for one or more products.  
**Request Body:**   

```json
[
    {
        "id": 1,
        "name": "Product 1",
        "quantity": 50
    },
    {
        "id": 2,
        "name": "Product 2",
        "quantity": 60
    }
]
```

**Response:** 
- **Status Code:** 200 (OK)

```json
[
    {
        "id": 1,
        "name": "Product 1",
        "quantity": 50
    },
    {
        "id": 2,
        "name": "Product 2",
        "quantity": 60
    }
]
```

### 4. Update Future Inventory

**Endpoint:** `/estoque/estoque-futuro/{product_id}`  
**Method:** `POST`    
**Description:** Update the future inventory of a specific physical product by its ID.  
**Request Parameters:** 

- `product_id` (int)
  
**Request Body:**   

```json
{
    "quantity": 50,
    "available_date": "2025-09-19",
}
```

**Response:** 
- **Status Code:** 200 (OK)

```json
{
    "id": 1,
    "quantity": 50,
    "available_date": "2025-09-19",
    "name": null
}
```

### 5. Inventory Reservation

**Endpoint:** `/estoque/reserva`  
**Method:** `POST`  
**Description:** Make inventory reservations for one or more products.  
**Request Body:**   

```json
[
    {
        "id": 1,
        "quantity": 5
    },
    {
        "id": 2,
        "quantity": 10
    }
]
```

**Response:** 
- **Status Code:** 200 (OK)

```json
[
    {
        "id": 1,
        "quantity": 5
    },
    {
        "id": 2,
        "quantity": 10
    }
]
```

### 6. Inventory Consultation

**Endpoint:** `/estoque/consulta/{strategy}`  
**Method:** `POST`  
**Description:** Consult inventory based on different strategies.  
**Request Parameters:**

- `strategy` (string)
    - `estoque-fisico`
    - `estoque-futuro`
  
**Request Body:**   

```json
[
    {
        "id": 1,
        "quantity": 100
    },
    {
        "id": 2,
        "quantity": 10
    }
]
```

**Response:** 
- **Status Code:** 200 (OK)

```json
[
    {
        "id": 1,
        "quantity": 100,
        "stock_availability": 50,
        "available": false
    },
    {
        "id": 2,
        "quantity": 10,
        "stock_availability": 60,
        "available": true,
        "inventory_available_date": "2024-01-20"
    }
]
```

## Tests
 The tests are automatically executed as soon as the container starts, but to run the tests the command is: 
 ```bash
'python -m pytest'.
 ```

## Database

This API uses a PostgreSQL database for storing inventory data. You can configure the

 database connection in the `database.py` file.

## Dependencies

This project uses FastAPI for building the API, SQLAlchemy for database operations, and Docker Compose for managing the development environment.

## Additional Notes

 - Ensure that you have docker installed.
 - You can access the API documentation by visiting http://localhost:8000/docs when the API is running.