import aiosqlite

DB_NAME = "biznes.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            description TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS debts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            person_name TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            is_paid INTEGER DEFAULT 0,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            unit TEXT DEFAULT 'dona'
        )''')
        await db.commit()

async def add_transaction(user_id, type_, amount, category, description):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO transactions (user_id, type, amount, category, description) VALUES (?, ?, ?, ?, ?)",
            (user_id, type_, amount, category, description)
        )
        await db.commit()

async def get_transactions(user_id, limit=10):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT type, amount, category, description, date FROM transactions WHERE user_id=? ORDER BY date DESC LIMIT ?",
            (user_id, limit)
        ) as cursor:
            return await cursor.fetchall()

async def get_summary(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT SUM(amount) FROM transactions WHERE user_id=? AND type='daromad'",
            (user_id,)
        ) as cursor:
            daromad = (await cursor.fetchone())[0] or 0
        async with db.execute(
            "SELECT SUM(amount) FROM transactions WHERE user_id=? AND type='xarajat'",
            (user_id,)
        ) as cursor:
            xarajat = (await cursor.fetchone())[0] or 0
        return daromad, xarajat

async def add_debt(user_id, person_name, amount, type_, description):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO debts (user_id, person_name, amount, type, description) VALUES (?, ?, ?, ?, ?)",
            (user_id, person_name, amount, type_, description)
        )
        await db.commit()

async def get_debts(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT id, person_name, amount, type, description FROM debts WHERE user_id=? AND is_paid=0",
            (user_id,)
        ) as cursor:
            return await cursor.fetchall()

async def pay_debt(debt_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE debts SET is_paid=1 WHERE id=?", (debt_id,))
        await db.commit()

async def add_product(user_id, name, quantity, price, unit):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO products (user_id, name, quantity, price, unit) VALUES (?, ?, ?, ?, ?)",
            (user_id, name, quantity, price, unit)
        )
        await db.commit()

async def get_products(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT id, name, quantity, price, unit FROM products WHERE user_id=?",
            (user_id,)
        ) as cursor:
            return await cursor.fetchall()

async def update_product_quantity(product_id, quantity):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE products SET quantity=? WHERE id=?", (quantity, product_id))
        await db.commit()
