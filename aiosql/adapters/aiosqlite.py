from ..aioctxlib import aiocontextmanager
from ..record import assign_record_class

class AioSQLiteAdapter:
    is_aio_driver = True

    @staticmethod
    def process_sql(_query_name, _op_type, sql):
        """Pass through function because the ``aiosqlite`` driver can already handle the
        :var_name format used by aiosql and doesn't need any additional processing.

        Args:
            _query_name (str): The name of the sql query.
            _op_type (SQLOperationType): The type of SQL operation performed by the query.
            sql (str): The sql as written before processing.

        Returns:
            str: Original SQL text unchanged.
        """
        return sql

    @staticmethod
    async def select(conn, _query_name, sql, parameters, record_class=None):
        async with conn.execute(sql, parameters) as cur:
            results = await cur.fetchall()
            if record_class is not None:
                column_names = [c[0] for c in cur.description]
                results = assign_record_class(results, column_names, record_class)
        return results

    @staticmethod
    async def select_one(conn, _query_name, sql, parameters, record_class=None):
        async with conn.execute(sql, parameters) as cur:
            result = await cur.fetchone()
            if result is not None and record_class is not None:
                column_names = [c[0] for c in cur.description]
                result = assign_record_class(results, column_names, record_class, True)
        return result

    @staticmethod
    @aiocontextmanager
    async def select_cursor(conn, _query_name, sql, parameters):
        async with conn.execute(sql, parameters) as cur:
            yield cur

    @staticmethod
    async def insert_returning(conn, _query_name, sql, parameters):
        async with conn.execute(sql, parameters) as cur:
            return cur.lastrowid

    @staticmethod
    async def insert_update_delete(conn, _query_name, sql, parameters):
        cur = await conn.execute(sql, parameters)
        await cur.close()

    @staticmethod
    async def insert_update_delete_many(conn, _query_name, sql, parameters):
        cur = await conn.executemany(sql, parameters)
        await cur.close()

    @staticmethod
    async def execute_script(conn, sql):
        await conn.executescript(sql)
