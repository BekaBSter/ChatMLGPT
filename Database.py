from mariadb import connect, Error
from Settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE, DEBUG, out


# Подключение к базе данных
def db_connect():
    try:
        conn = connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_DATABASE
        )
        cur = conn.cursor()
        if DEBUG:
            out("База данных: успешное подключение!", "g")
    except() as e:
        out(f"База данных: {e}", "r")
        return None, None
    return conn, cur


# Сохранение изменений в базе данных и отключение
def disconnect(conn):
    conn.commit()
    conn.close()


# Инициализация таблиц в базе данных
def init_tables():
    conn, cur = db_connect()
    try:
        QUERY = '''CREATE TABLE IF NOT EXISTS Users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id VARCHAR(255),
                        first_name VARCHAR(255),
                        past_message TEXT
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                '''
        cur.execute(QUERY)
        disconnect(conn)
        out("База данных: успешное создание необходимых таблиц!", "g")
    except Error as e:
        out(f"База данных: ошибка создания необходимых таблиц! {e}", "r")


# Создание нового пользователя в базе данных
def new_user(user_id):
    conn, cur = db_connect()
    # QUERY = f""
    # cur.execute()
    disconnect(conn)
    if DEBUG:
        out("База данных: создан новый пользователь! "
            f"User ID: {user_id}.", "g")


# Поиск пользователя в базе данных
async def search_user(user_id):
    pass
