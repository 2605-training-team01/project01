from database.db import get_connection

def save_order(
        order_type,
        payment_type,
        total_amount):

    conn = get_connection()

    cursor = conn.cursor()

    sql = """
    INSERT INTO ORDERS
    (
        order_type,
        payment_type,
        total_amount
    )
    VALUES
    (
        ?, ?, ?
    )
    """

    cursor.execute(
        sql,
        (
            order_type,
            payment_type,
            total_amount
        )
    )

    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return order_id