from asyncmy import connect
from Settings import db_user, db_password, db_host, db_port, db_database


async def async_connect():
    try:
        conn = await connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_database
        )
        cur = await conn.cursor()
    except() as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None, None
    return conn, cur


async def disconnect(conn):
    await conn.commit()
    await conn.close()
