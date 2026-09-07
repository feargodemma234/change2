def get_products():
    return [
        {"id": 1, "name": "Wireless Headphones", "price": 45000, "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400", "category": "Electronics"},
        {"id": 2, "name": "Smart Watch", "price": 78000, "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400", "category": "Electronics"},
        {"id": 3, "name": "Delivery Service", "price": 2500, "image": "https://images.unsplash.com/photo-1586528113085-9100e3e2b122?w=400", "category": "Delivery"},
        {"id": 4, "name": "Laptop Bag", "price": 22000, "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400", "category": "Fashion"},
        {"id": 5, "name": "T-Shirt", "price": 8000, "image": "https://images.unsplash.com/photo-1521572163474-3910d44e4b82?w=400", "category": "Fashion"},
        {"id": 6, "name": "Phone Case", "price": 3500, "image": "https://images.unsplash.com/photo-1601597111158-2fceff292cdc?w=400", "category": "Electronics"},
    ]

def get_orders():
    # Dummy orders for testing
    return [
        {"id": "ORD001", "date": "2026-09-05", "total": 45000, "status": "Delivered", "items": 2},
        {"id": "ORD002", "date": "2026-09-06", "total": 80500, "status": "Processing", "items": 3},
    ]

def get_order_by_id(order_id):
    orders = get_orders()
    for order in orders:
        if order['id'] == order_id:
            return order
    return None