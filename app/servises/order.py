from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.schemas.order import Order, OrderCreate
from app.models.product import Product


def get_order(db:Session, order_id:int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_user_orders(db:Session, user_id:int):
    return db.query(Order).filter(user_id == Order.user_id).all()


def to_order_schema(db_order:Order, db:Session):
    items = []
    for item in db_order.items:
        items.append(
            OrderItem(
                id = item.id,
                product_id = item.product_id,
                quantity = item.quantity,
                price = item.price
            )
        )
    return Order(id=db_order.id,
                 user_id = db_order.user_id,
                 created_ad = db_order.created_at,
                 status = db_order.status,
                 total_price = db_order.total_price,
                 items = items
                 )


def  create_order(db:Session, order:OrderCreate, user_id:int):
    db_order = Order(user_id = user_id)
    db.add(db_order)
    db.flush()
    
    total_price = 0
    order_items = []

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise ValueError(f"Продукт с данным {item.product_id} не найден")
        
        price = product.price*item.quantity
        total_price+=price
        db_item = OrderItem(order_id = db_order.id, 
                            product_id = item.product_id,
                            quantity = item.quantity,
                            price = price)
        db.add(db_item)
        order_items.append(db_item)

    db_order.total_price = total_price
    db.commit()
    db.refresh(db_order)
    return to_order_schema(db_order, db)

