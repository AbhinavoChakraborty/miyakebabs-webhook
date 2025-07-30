import os
from dotenv import load_dotenv
import psycopg2
from contextlib import contextmanager


# load_dotenv()


DB_URL =  "postgresql://postgres:HsUVWoYItgsIBHbsytYivLCCnaEFwNjp@interchange.proxy.rlwy.net:56909/railway"


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
        
        # Log and insert outlet
        print("[DB] Inserting outlet...")
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

        # Log and insert customer
        print("[DB] Inserting customer...")
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

        # Log and insert order
        print("[DB] Inserting order...")
        cur.execute("""
            INSERT INTO orders (order_id, outlet_id, customer_id, order_date, total_amount, payment_mode, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            payload.order.order_id,
            payload.order.outlet_id,
            payload.order.customer_id,
            payload.order.order_date,
            payload.order.total_amount,
            payload.order.payment_mode,
            payload.order.status
        ))

        # Log and insert order items
        print("[DB] Inserting order items...")
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

        print("[DB] ✅ All records inserted successfully.")
        cur.close()
