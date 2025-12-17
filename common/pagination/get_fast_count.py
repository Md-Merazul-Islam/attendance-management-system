from django.db import connection

def get_fast_count(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT reltuples::bigint FROM pg_class WHERE relname = '{table_name}';")
        return int(cursor.fetchone()[0])