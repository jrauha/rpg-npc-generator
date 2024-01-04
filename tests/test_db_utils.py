import random
import string

import pytest
from sqlalchemy import text

from npcgen.core.db_utils import (
    create_record,
    delete_record,
    read_random_record,
    read_record_by_attr,
    read_record_by_id,
    read_records,
    update_record,
)


@pytest.fixture()
def temp_test_table(session):
    table_name = "test_table"
    id_column = "id"
    column1 = "column1"
    column2 = "column2"

    # Generate a random table name
    table_name = "test_" + "".join(
        random.choices(string.ascii_lowercase, k=10)
    )

    # Create the temporary test table
    create_table_query = f"""
        CREATE TABLE {table_name}
        ({id_column} INT, {column1} TEXT, {column2} TEXT)
    """
    session.execute(text(create_table_query))

    # Insert test rows
    insert_row_query = f"""
        INSERT INTO {table_name} ({id_column}, {column1}, {column2})
        VALUES (1, 'value1', 'value2'), (2, 'value3', 'value4')
    """
    session.execute(text(insert_row_query))

    yield table_name

    # Drop the temporary test table
    drop_table_query = f"DROP TABLE {table_name}"
    session.execute(text(drop_table_query))


def test_create_record(session, temp_test_table):
    table_name = temp_test_table
    kwargs = {"id": 1, "column1": "value1", "column2": "value2"}

    record_id = create_record(session, table_name, **kwargs)

    assert isinstance(record_id, int)
    assert record_id > 0


def test_read_records(session, temp_test_table):
    table_name = temp_test_table

    records = read_records(session, table_name)

    assert isinstance(records, list)
    assert len(records) > 0


def test_read_record_by_id(session, temp_test_table):
    table_name = temp_test_table
    record_id = 1

    record = read_record_by_id(session, table_name, record_id)

    assert record is not None


def test_read_record_by_attr(session, temp_test_table):
    table_name = temp_test_table
    attr = "column1"
    value = "value1"

    record = read_record_by_attr(session, table_name, attr, value)

    assert record is not None


def test_read_random_record(session, temp_test_table):
    table_name = temp_test_table

    record = read_random_record(session, table_name)

    assert record is not None


def test_update_record(session, temp_test_table):
    table_name = temp_test_table
    record_id = 1
    kwargs = {"column1": "new_value1", "column2": "new_value2"}

    update_record(session, table_name, record_id, **kwargs)

    updated_record = read_record_by_id(session, table_name, record_id)
    assert updated_record is not None
    assert updated_record.column1 == kwargs["column1"]
    assert updated_record.column2 == kwargs["column2"]


def test_delete_record(session, temp_test_table):
    table_name = temp_test_table
    record_id = 1

    delete_record(session, table_name, record_id)

    deleted_record = read_record_by_id(session, table_name, record_id)
    assert deleted_record is None
