from database.db import get_connection

def get_categories():

    conn = get_connection()

    sql = """
    SELECT category_id, category_name
    FROM CATEGORY
    ORDER BY category_name
    """

    result = conn.execute(sql).fetchall()

    conn.close()

    return result


def get_menu_by_category(category_id):

    conn = get_connection()

    sql = """
    SELECT
        menu_id,
        menu_name,
        price
    FROM MENU
    WHERE category_id = ?
    """

    result = conn.execute(
        sql,
        (category_id,)
    ).fetchall()

    conn.close()

    return result