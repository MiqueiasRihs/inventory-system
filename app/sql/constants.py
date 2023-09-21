from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import SessionLocal  # Importe sua sessão de banco de dados aqui


def inventory_reservation_difference(db: Session, product_id: int):
    query = text("""
        SELECT
            i.id,
            i.quantity AS inventory_quantity,
            CASE
                WHEN SUM(ri.quantity) IS NULL THEN 0
                ELSE SUM(ri.quantity)
            END AS reservation_quantity,
            CASE 
                WHEN (i.quantity - SUM(ri.quantity)) < 0 THEN 0
                WHEN SUM(ri.quantity) IS NULL THEN i.quantity
                ELSE (i.quantity - SUM(ri.quantity))
            END AS difference
        FROM inventory i
        LEFT JOIN reservation_inventory ri 
            ON i.id = ri.inventory_id
                AND ri.status = 'Ativo'
                AND ri.expiration_date > now()
        WHERE 1=1
            AND i.id = :product_id
        GROUP BY i.id;
    """)

        
    result = db.execute(query, {"product_id": product_id})
    result_dict = {}
    for row in result.fetchall():
        result_dict = {
            "id": row[0],
            "inventory_quantity": row[1],
            "reservation_quantity": row[2],
            "difference": row[3]
        }

    return result_dict
