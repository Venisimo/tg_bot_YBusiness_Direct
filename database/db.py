import asyncio
import json
import aiosqlite
from enums.sources import Source

DB_PATH = "accounts.db"


async def init_db(db_path: str = DB_PATH) -> None:
    """
    Инициализирует базу данных и создаёт таблицу accounts, если она ещё не существует.
    Добавлено поле user_id для Telegram chat_id.
    """
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                auth TEXT NOT NULL,
                account_name TEXT NOT NULL DEFAULT '',
                user_id INTEGER DEFAULT NULL
            );
        """
        )
        await db.commit()


async def add_account(
    source: str,
    auth: dict,
    account_name: str = "",
    user_id: int = None,
    db_path: str = DB_PATH
) -> None:
    """
    Добавляет новый аккаунт в базу с chat_id.

    :param user_id: Telegram chat_id пользователя
    """
    try:
        source_enum = Source(source.upper())
    except ValueError:
        raise ValueError(
            f"Неподдерживаемый источник: {source}. Доступные источники: {[s.value for s in Source]}"
        )

    auth_json = json.dumps(auth)
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            "INSERT INTO accounts (source, auth, account_name, user_id) VALUES (?, ?, ?, ?)",
            (source_enum.value, auth_json, account_name, user_id),
        )
        await db.commit()


async def get_all_accounts(db_path: str = DB_PATH) -> list[dict]:
    """
    Получает все аккаунты из базы. Поле auth десериализуется из JSON в словарь.
    """
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM accounts") as cursor:
            rows = await cursor.fetchall()
            accounts = []
            for row in rows:
                account = dict(row)
                account["auth"] = json.loads(account["auth"])
                accounts.append(account)
            return accounts


async def update_account(
    account_id: int,
    source: str = None,
    auth: dict = None,
    account_name: str = None,
    user_id: int = None,
    db_path: str = DB_PATH,
) -> None:
    """
    Обновляет данные аккаунта по его ID.

    :param account_id: Идентификатор аккаунта
    :param user_id: Новый Telegram chat_id, если требуется обновление
    """
    fields = []
    values = []
    if source is not None:
        fields.append("source = ?")
        values.append(source)
    if auth is not None:
        fields.append("auth = ?")
        values.append(json.dumps(auth))
    if account_name is not None:
        fields.append("account_name = ?")
        values.append(account_name)
    if user_id is not None:
        fields.append("user_id = ?")
        values.append(user_id)
    if not fields:
        return
    values.append(account_id)
    query = f"UPDATE accounts SET {', '.join(fields)} WHERE id = ?"
    async with aiosqlite.connect(db_path) as db:
        await db.execute(query, values)
        await db.commit()


async def delete_account(account_id: int, db_path: str = DB_PATH) -> None:
    """
    Удаляет аккаунт по его ID.
    """
    async with aiosqlite.connect(db_path) as db:
        await db.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        await db.commit()


async def drop_table(db_path: str = DB_PATH) -> None:
    """
    Удаляет таблицу accounts из базы данных.
    """
    async with aiosqlite.connect(db_path) as db:
        await db.execute("DROP TABLE IF EXISTS accounts")
        await db.commit()


async def get_account_by_id(account_id: int, db_path: str = DB_PATH) -> dict | None:
    """
    Получает аккаунт из базы по его ID. Поле auth десериализуется из JSON в словарь.
    
    :param account_id: Идентификатор аккаунта
    :return: Словарь с данными аккаунта или None, если аккаунт не найден
    """
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM accounts WHERE id = ?", (account_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            account = dict(row)
            account["auth"] = json.loads(account["auth"])
            return account
