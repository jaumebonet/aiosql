from contextlib import contextmanager

from ..patterns import var_pattern
from ..record import assign_record_class

def replacer(match):
    gd = match.groupdict()
    if gd["dblquote"] is not None:
        return gd["dblquote"]
    elif gd["quote"] is not None:
        return gd["quote"]
    else:
        return f'{gd["lead"]}%({gd["var_name"]})s{gd["trail"]}'


class PsycoPG2Adapter:
    @staticmethod
    def process_sql(_query_name, _op_type, sql):
        return var_pattern.sub(replacer, sql)

    @staticmethod
    def select(conn, _query_name, sql, parameters, record_class=None):
        with conn.cursor() as cur:
            cur.execute(sql, parameters)
            results = cur.fetchall()
            if record_class is not None:
                column_names = [c.name for c in cur.description]
                results = assign_record_class(results, column_names, record_class)
        return results

    @staticmethod
    def select_one(conn, _query_name, sql, parameters, record_class=None):
        with conn.cursor() as cur:
            cur.execute(sql, parameters)
            result = cur.fetchone()
            if result is not None and record_class is not None:
                column_names = [c.name for c in cur.description]
                result = assign_record_class(results, column_names, record_class, True)
        return result

    @staticmethod
    @contextmanager
    def select_cursor(conn, _query_name, sql, parameters):
        with conn.cursor() as cur:
            cur.execute(sql, parameters)
            yield cur

    @staticmethod
    def insert_update_delete(conn, _query_name, sql, parameters):
        with conn.cursor() as cur:
            cur.execute(sql, parameters)

    @staticmethod
    def insert_update_delete_many(conn, _query_name, sql, parmeters):
        with conn.cursor() as cur:
            cur.executemany(sql, parmeters)

    @staticmethod
    def insert_returning(conn, _query_name, sql, parameters):
        with conn.cursor() as cur:
            cur.execute(sql, parameters)
            res = cur.fetchone()
            if res:
                return res[0] if len(res) == 1 else res
            else:
                return None

    @staticmethod
    def execute_script(conn, sql):
        with conn.cursor() as cur:
            cur.execute(sql)
