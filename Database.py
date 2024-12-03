from asyncmy import connect
from Settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE


async def async_connect():
    try:
        conn = await connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_DATABASE
        )
        cur = await conn.cursor()
    except() as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None, None
    return conn, cur


async def disconnect(conn):
    await conn.commit()
    await conn.close()
