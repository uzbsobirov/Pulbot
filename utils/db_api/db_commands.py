from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        user_id BIGINT NOT NULL UNIQUE,
        issubs TEXT NULL,
        phone TEXT NULL,
        referal_link TEXT NULL,
        parent_id BigInt NULL,
        count BigInt NULL,
        balance BigInt NULL,
        wallet TEXT NULL
        );
        """
        await self.execute(sql, execute=True)


    async def create_table_ban_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Ban (
        user_id BIGINT NOT NULL UNIQUE,
        phone TEXT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_admin_panel(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Admin (
        id BigInt UNIQUE,
        tolovtarixi TEXT NULL,
        qollanma TEXT NULL,
        adminuser TEXT NULL,
        minimalsumma BigInt NOT NULL,
        taklifsumma BigInt NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_sponsor(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Sponsor (
        id SERIAL PRIMARY KEY,
        channel TEXT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name: str, username: str, user_id: int, issubs: str, referal_link: str, parent_id: int, count: int, balance: int, wallet: str = None):
        sql = "INSERT INTO users (full_name, username, user_id, issubs, referal_link, parent_id, count, balance, wallet) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) returning *"
        return await self.execute(sql, full_name, username, user_id, issubs, referal_link, parent_id, count, balance, wallet, fetchrow=True)

    async def add_ban_user(self, user_id, phone):
        sql = "INSERT INTO ban (user_id, phone) VALUES($1, $2) returning *"
        return await self.execute(sql, user_id, phone, fetchrow=True)

    async def add_user_to_ban(self, user_id):
        sql = "INSERT INTO ban (user_id) VALUES($1) returning *"
        return await self.execute(sql, user_id, fetchrow=True)

    async def add_user_to_panel(self):
        sql = "INSERT INTO Admin (id, minimalsumma, taklifsumma) VALUES(1, 3000, 200) returning *"
        return await self.execute(sql, fetchrow=True)

    async def add_channel(self, channel):
        sql = "INSERT INTO Sponsor (channel) VALUES($1) returning *"
        return await self.execute(sql, channel, fetchrow=True)

    async def add_sponsor_test(self, channel):
        sql = "INSERT INTO Sponsor (channel) VALUES($1) returning *"
        return await self.execute(sql, channel, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_row_panel(self):
        sql = "SELECT * FROM Sponsor"
        return await self.execute(sql, fetch=True)

    async def select_one_users(self, user_id):
        sql = "SELECT * FROM Users WHERE user_id=$1"
        return await self.execute(sql, user_id, fetch=True)

    async def select_one_ban_user(self, user_id):
        sql = "SELECT * FROM Ban WHERE user_id=$1"
        return await self.execute(sql, user_id, fetch=True)


    async def select_from_panel(self, id):
        sql = "SELECT * FROM Admin WHERE id=$1"
        return await self.execute(sql, id, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_issubs(self, issubs, user_id):
        sql = "UPDATE Users SET issubs=$1 WHERE user_id=$2"
        return await self.execute(sql, issubs, user_id, execute=True)

    async def update_panel_min_sum(self, minimalsumma, id):
        sql = "UPDATE Admin SET minimalsumma=$1 WHERE id=$2"
        return await self.execute(sql, minimalsumma, id, execute=True)

    async def update_panel_taklif_sum(self, taklifsumma, id):
        sql = "UPDATE Admin SET taklifsumma=$1 WHERE id=$2"
        return await self.execute(sql, taklifsumma, id, execute=True)
    
    async def update_user_balans(self, balance, user_id):
        sql = "UPDATE Users SET balance=$1 WHERE telegram_id=$2"
        return await self.execute(sql, balance, user_id, execute=True)

    async def update_admin_tolov_tarix(self, tolovtarix, id):
        sql = "UPDATE Admin SET tolovtarixi=$1 WHERE id=$2"
        return await self.execute(sql, tolovtarix, id, execute=True)

    async def update_count(self, user_id):
        sql = "UPDATE Users SET count=count+1 WHERE user_id=$1"
        return await self.execute(sql, user_id, execute=True)

    # async def update_balance_count(self, miqdor, user_id):
    #     sql = f"UPDATE Users SET balance=balance+{miqdor} WHERE user_id=$2"
    #     return await self.execute(sql, miqdor, user_id, execute=True)

    async def update_balance_count(self, user_id):
        select_sql = "SELECT * FROM Admin"
        result = await self.execute(select_sql, fetch=True)

        if result:
            balans = result[0][5]
            sql = f"UPDATE Users SET balance=balance+{balans} WHERE user_id=$1"
            return await self.execute(sql, user_id, execute=True)

    async def update_admin_qollanma(self, qollanma, id):
        sql = "UPDATE Admin SET qollanma=$1 WHERE id=$2"
        return await self.execute(sql, qollanma, id, execute=True)

    async def update_admin_username(self, adminuser, id):
        sql = "UPDATE Admin SET adminuser=$1 WHERE id=$2"
        return await self.execute(sql, adminuser, id, execute=True)
    
    async def update_user_phone(self, phone, user_id):
        sql = "UPDATE Users SET phone=$1 WHERE user_id=$2"
        return await self.execute(sql, phone, user_id, execute=True)

    async def update_user_wallet(self, wallet, user_id):
        sql = "UPDATE Users SET wallet=$1 WHERE user_id=$2"
        return await self.execute(sql, wallet, user_id, execute=True)

    async def update_user_subs(self, issubs, user_id):
        sql = "UPDATE Users SET issubs=$1 WHERE user_id=$2"
        return await self.execute(sql, issubs, user_id, execute=True)

    async def update_user_balance_zero(self, balance, user_id):
        sql = "UPDATE Users SET balance=$1 WHERE user_id=$2"
        return await self.execute(sql, balance, user_id, execute=True)

    async def add_user_balance(self, user_id, miqdor):
        select_sql = "SELECT * FROM Users WHERE user_id=$1"
        result = await self.execute(select_sql, user_id, fetch=True)

        if result:
            balans = result[0][9]
            balans += miqdor
            sql = f"UPDATE Users SET balance={balans} WHERE user_id=$1"
            return await self.execute(sql, user_id, execute=True)

    async def subtraction_user_balance(self, user_id, miqdor):
        select_sql = "SELECT * FROM Users WHERE user_id=$1"
        result = await self.execute(select_sql, user_id, fetch=True)

        if result:
            balans = result[0][9]
            balans -= miqdor
            sql = f"UPDATE Users SET balance={balans} WHERE user_id=$1"
            return await self.execute(sql, user_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def delete_sponsor_channel(self, channel):
        sql = "DELETE FROM Sponsor WHERE channel=$1"
        await self.execute(sql, channel, execute=True)

    async def delete_user(self, user_id):
        sql = "DELETE FROM Users WHERE user_id=$1"
        await self.execute(sql, user_id, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    ### Kurslar uchun jadval (table) yaratamiz
    async def create_table_courses(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Courses (
        id SERIAL PRIMARY KEY,

        -- Kurs kategoriyasi
        category_code VARCHAR(50) NOT NULL,
        category_name VARCHAR(150) NOT NULL,

        -- Kurs kategoriya ichida ketgoriyasi ("Dasturlash"->"Python")
        subcategory_code VARCHAR(50) NOT NULL,
        subcategory_name VARCHAR(150) NOT NULL,

        -- Kurs haqida malumot
        coursename VARCHAR(150) NOT NULL,
        photo varchar(500) NULL,
        price BIGINT NOT NULL,
        description VARCHAR(5000) NULL
        );
        """
        await self.execute(sql, execute=True)

    async def add_course(
        self,
        category_code,
        category_name,
        subcategory_code,
        subcategory_name,
        coursename,
        photo=None,
        price=None,
        description="",
    ):
        sql = "INSERT INTO Courses (category_code, category_name, subcategory_code, subcategory_name, coursename, photo, price, description) VALUES($1, $2, $3, $4, $5, $6, $7, $8) returning *"
        return await self.execute(
            sql,
            category_code,
            category_name,
            subcategory_code,
            subcategory_name,
            coursename,
            photo,
            price,
            description,
            fetchrow=True,
        )

    async def get_categories(self):
        sql = "SELECT DISTINCT category_name, category_code FROM Courses"
        return await self.execute(sql, fetch=True)

    async def get_subcategories(self, category_code):
        sql = f"SELECT DISTINCT subcategory_name, subcategory_code FROM Courses WHERE category_code='{category_code}'"
        return await self.execute(sql, fetch=True)

    async def count_courses(self, category_code, subcategory_code=None):
        if subcategory_code:
            sql = f"SELECT COUNT(*) FROM Courses WHERE category_code='{category_code}' AND subcategory_code='{subcategory_code}'"
        else:
            sql = f"SELECT COUNT(*) FROM Courses WHERE category_code='{category_code}'"
        return await self.execute(sql, fetchval=True)

    async def get_courses(self, category_code, subcategory_code):
        sql = f"SELECT * FROM Courses WHERE category_code='{category_code}' AND subcategory_code='{subcategory_code}'"
        return await self.execute(sql, fetch=True)

    async def get_course(self, product_id):
        sql = f"SELECT * FROM Courses WHERE id={product_id}"
        return await self.execute(sql, fetchrow=True)

    async def drop_courses(self):
        await self.execute("DROP TABLE Courses", execute=True)