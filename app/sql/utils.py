def calculate_stock_availability(result, strategy):
    stock_availability, difference, available_date = 0, 0, None 
    
    if result:
        inventory_quantity = result['inventory_quantity'] if result['inventory_quantity'] else 0
        reservation_quantity = result['reservation_quantity'] if result['reservation_quantity'] else 0
        future_quantity = result['future_reservation_quantity'] if result['future_reservation_quantity'] else 0

        # Calculate stock availability based on the selected strategy
        if strategy == "estoque-fisico":
            stock_availability = inventory_quantity - reservation_quantity

        elif strategy == "estoque-futuro":
            stock_availability = (inventory_quantity + future_quantity) - reservation_quantity

        available_date = result.get("inventory_available_date")
        
        difference = inventory_quantity - reservation_quantity
        
    stock_availability = {
        "stock_availability": stock_availability,
        "available_date": available_date,
        "current_difference": difference,
    }

    return stock_availability
