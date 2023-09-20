from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import SessionLocal  # Importe sua sessão de banco de dados aqui


def inventory_reservation_difference(db: Session, product_id: int):
    query = text("""
        SELECT
            i.id,
            i.quantity AS inventory_quantity,
            sum(ri.quantity) AS reservation_quantity,
            (i.quantity - sum(ri.quantity)) AS difference
        FROM reservation_inventory ri
        LEFT JOIN inventory i 
            ON i.id = ri.inventory_id
        WHERE 1=1
            AND i.id = :product_id
            AND ri.status = 'Ativo'
            AND ri.expiration_date > now()
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
