from sqlalchemy import text


def create_record(cur, table_name, returning=None, **kwargs):
    columns = ", ".join(kwargs.keys())
    values = ", ".join([":" + sub for sub in kwargs.keys()])
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    if returning:
        query += " RETURNING " + returning
    result = cur.execute(text(query), kwargs)
    return result.fetchone() if returning else None


def read_records(cur, table_name):
    query = cur.execute(text(f"SELECT * FROM {table_name}"))
    return query.fetchall()


def read_record_by_id(cur, table_name, record_id):
    query = cur.execute(
        text(f"SELECT * FROM {table_name} WHERE id = :id"), {"id": record_id}
    )
    return query.fetchone()


def record_exists(cur, table_name, attr, value):
    query = cur.execute(
        text(
            f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {attr} = :value)"
        ),
        {"value": value},
    )
    return query.fetchone()[0]


def read_record_by_attr(cur, table_name, attr, value):
    query = cur.execute(
        text(f"SELECT * FROM {table_name} WHERE {attr} = :value"),
        {"value": value},
    )
    return query.fetchone()


def read_random_record(cur, table_name):
    query = cur.execute(
        text(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1")
    )
    return query.fetchone()


def update_record(cur, table_name, record_id, **kwargs):
    set_values = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
    query = f"UPDATE {table_name} SET {set_values} WHERE id = :id"
    kwargs["id"] = record_id
    cur.execute(text(query), kwargs)


def delete_record(cur, table_name, record_id):
    cur.execute(
        text(f"DELETE FROM {table_name} WHERE id = :id"), {"id": record_id}
    )
