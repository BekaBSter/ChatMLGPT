from pymysql import connect, Error
from Settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE, DEBUG, out, generate_random_string
import json


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
        QUERY_1 = '''
        CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id VARCHAR(255),
                        first_name VARCHAR(255),
                        neuro VARCHAR(255),
                        balance FLOAT,
                        ref varchar(255)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                '''
        QUERY_2 = '''
                CREATE TABLE IF NOT EXISTS promocodes (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                promocode varchar(255),
                                sum FLOAT,
                                uses JSON
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                        '''
        cur.execute(QUERY_1)
        cur.execute(QUERY_2)
        db_disconnect(conn, cur)
        out("База данных: успешное создание необходимых таблиц!", "g")
    except Error as e:
        out(f"База данных: ошибка создания необходимых таблиц! {e}", "r")


# Создание нового пользователя в базе данных
def new_user(user_id, first_name):
    conn, cur = db_connect()
    ref = generate_random_string()
    QUERY = f'''
    INSERT
    INTO users (user_id, first_name, balance, ref)
    VALUES ('{user_id}', '{first_name}', 5.0, '{ref}')
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
    SELECT user_id, neuro, balance
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
            balance = user[2]
            db_disconnect(conn, cur)
            return isSearch, neuro, balance
        else:
            out(f"База данных: Пользователь не найден. User_id: {user_id}.", "g")
    except Error as e:
        out(f"База данных: Ошибка поиска пользователя: {e}. User_id: {user_id}.", "r")
    return None, None, None


def search_promocode(promocode):
    conn, cur = db_connect()
    QUERY = f'''
    SELECT promocode, sum, uses
    FROM promocodes
    WHERE promocode = '{promocode}'
    '''
    try:
        cur.execute(QUERY)
        result = cur.fetchone()
        if result is not None:
            out(f"База данных: Промокод найден. Promocode: {promocode}.", "g")
            sum = result[1]
            uses = result[2]
            if uses is not None:
                uses = json.loads(uses)
            else:
                uses = []
            return True, sum, uses
        else:
            out(f"База данных: Промокод не найден. Promocode: {promocode}.", "g")
            return False, 0, []
    except Error as e:
        out(f"База данных: Ошибка поиска промокода: {e}. Promocode: {promocode}", "r")
    return False, 0, None, []


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


def update_balance(user_id, balance):
    conn, cur = db_connect()
    QUERY = f'''
        UPDATE users
        SET balance = '{balance}'
        WHERE user_id = '{user_id}'
        '''
    try:
        cur.execute(QUERY)
        out(f"База данных: Успешное обновление записи о балансе. User_id: {user_id}.", "g")
    except Error as e:
        out(f"База данных: Ошибка обновления записи о балансе: {e}. User_id: {user_id}.", "r")
    db_disconnect(conn, cur)


def update_uses_promocode(promocode, uses):
    conn, cur = db_connect()
    uses = json.dumps(uses)
    QUERY = f'''
        UPDATE promocodes
        SET uses = '{uses}'
        WHERE promocode = '{promocode}'
    '''
    try:
        cur.execute(QUERY)
        out(f"База данных: Успешное обновление записи о промокоде. Promocode: {promocode}.", "g")
    except Error as e:
        out(f"База данных: ошибка обновления записи о промокоде: {e}. Promocode: {promocode}", "r")
    db_disconnect(conn, cur)
