from pymysql import connect, Error
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
def db_disconnect(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


# Инициализация таблиц в базе данных
def init_tables():
    conn, cur = db_connect()
    try:
        QUERY = '''
        CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id VARCHAR(255),
                        first_name VARCHAR(255),
                        neuro VARCHAR(255)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                '''
        cur.execute(QUERY)
        db_disconnect(conn, cur)
        out("База данных: успешное создание необходимых таблиц!", "g")
    except Error as e:
        out(f"База данных: ошибка создания необходимых таблиц! {e}", "r")


# Создание нового пользователя в базе данных
def new_user(user_id, first_name):
    conn, cur = db_connect()
    QUERY = f'''
    INSERT
    INTO users (user_id, first_name)
    VALUES ('{user_id}', '{first_name}')
    '''
    cur.execute(QUERY)
    db_disconnect(conn, cur)
    if DEBUG:
        out("База данных: создан новый пользователь! "
            f"User ID: {user_id}.", "g")


# Поиск пользователя в базе данных
def search_user(user_id):
    conn, cur = db_connect()
    QUERY = f'''
    SELECT user_id, neuro
    FROM users
    WHERE user_id = '{user_id}'
    '''
    try:
        cur.execute(QUERY)
        user = cur.fetchone()
        if user is not None:
            out(f"База данных: Пользователь найден. User_id: {user_id}.", "g")
            isSearch = True
            neuro = user[1]
            db_disconnect(conn, cur)
            return isSearch, neuro
        else:
            out(f"База данных: Пользователь не найден. User_id: {user_id}.", "g")
    except Error as e:
        out(f"База данных: Ошибка поиска пользователя: {e}. User_id: {user_id}.", "r")
    return None, None


def update_neuro_user(user_id, neuro):
    conn, cur = db_connect()
    QUERY = f'''
    UPDATE users
    SET neuro = '{neuro}'
    WHERE user_id = '{user_id}'
    '''
    try:
        cur.execute(QUERY)
        out(f"База данных: Успешное обновление записи о нейросети. User_id: {user_id}.", "g")
    except Error as e:
        out(f"База данных: ошибка обновления записи о нейросети: {e}. User_id: {user_id}.", "r")
    db_disconnect(conn, cur)
