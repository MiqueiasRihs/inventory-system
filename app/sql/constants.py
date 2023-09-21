from sqlalchemy import text
from sqlalchemy.orm import Session

from .database import SessionLocal

from .utils import calculate_stock_availability


def get_stock_availability_inventory(db: Session, product_id: int, strategy):
    query = text("""
        SELECT
            i.id,
            i.quantity AS inventory_quantity,
            SUM(ri.quantity) AS reservation_quantity,
            fi.quantity AS future_reservation_quantity,
            TO_CHAR(fi.available_date, 'DD/MM/YYYY') AS inventory_available_date
        FROM inventory i
        LEFT JOIN reservation_inventory ri 
            ON i.id = ri.inventory_id
                AND ri.status = 'Ativo'
                AND ri.expiration_date > now()
        LEFT JOIN future_inventory fi
            ON fi.id = i.id
        WHERE 1=1
            AND i.id = :product_id
        GROUP BY i.id, fi.id;
    """)
        
    result = db.execute(query, {"product_id": product_id})
    result_dict = {}
    for row in result.fetchall():
        result_dict = {
            "id": row[0],
            "inventory_quantity": row[1],
            "reservation_quantity": row[2],
            "future_reservation_quantity": row[3],
            "inventory_available_date": row[4]
        }
        
    return calculate_stock_availability(result_dict, strategy)