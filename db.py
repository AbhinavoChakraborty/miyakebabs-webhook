import psycopg2
from contextlib import contextmanager

DB_URL = "postgresql://postgres:HsUVWoYItgsIBHbsytYivLCCnaEFwNjp@interchange.proxy.rlwy.net:56909/railway"

@contextmanager
def get_connection():
    conn = psycopg2.connect(DB_URL)
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def insert_data(payload):
    with get_connection() as conn:
        cur = conn.cursor()

        # Insert outlet
        cur.execute("""
            INSERT INTO outlets (outlet_id, outlet_name, location, contact_info)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (outlet_id) DO NOTHING
        """, (
            payload.outlet.outlet_id,
            payload.outlet.outlet_name,
            payload.outlet.location,
            payload.outlet.contact_info
        ))

        # Insert customer
        cur.execute("""
            INSERT INTO customers (customer_id, name, phone_number, email, created_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (customer_id) DO NOTHING
        """, (
            payload.customer.customer_id,
            payload.customer.name,
            payload.customer.phone_number,
            payload.customer.email,
            payload.customer.created_at
        ))

        # Insert order
        cur.execute("""
            INSERT INTO orders (
                order_id, outlet_id, customer_id, order_date, total_amount,
                payment_mode, status, order_type, payment_type, created_on, order_from
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            payload.order.order_id,
            payload.order.outlet_id,
            payload.order.customer_id,
            payload.order.order_date,
            payload.order.total_amount,
            payload.order.payment_mode,
            payload.order.status,
            payload.order.order_type,
            payload.order.payment_type,
            payload.order.created_on,
            payload.order.order_from
        ))

        

        # Insert order items
        for item in payload.order.items:
            cur.execute("""
                INSERT INTO order_items (item_id, order_id, item_name, quantity, price_per_unit, total_price)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                item.item_id,
                item.order_id,
                item.item_name,
                item.quantity,
                item.price_per_unit,
                item.total_price
            ))

        # Insert taxes
        for tax in payload.order.taxes or []:
            cur.execute("""
                INSERT INTO taxes (order_id, title, rate, amount)
                VALUES (%s, %s, %s, %s)
            """, (
                payload.order.order_id,
                tax.title,
                tax.rate,
                tax.amount
            ))

        # Insert discounts
        for disc in payload.order.discounts or []:
            cur.execute("""
                INSERT INTO discounts (order_id, title, type, rate, amount)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                payload.order.order_id,
                disc.title,
                disc.type,
                disc.rate, 
                disc.amount
            ))

        cur.close()