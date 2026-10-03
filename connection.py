import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

ps = os.getenv("PASSWORD_DB")


async def connection():
    try:
        conn = await asyncpg.connect(
            port=5432,
            host="localhost",
            user="postgres",
            database="Chat-bot",
            password=ps
        )

        print("Connection Successful")
        return conn

    except Exception as error:
        print(f"Connection Error: {error}")
        return None


async def create_table():
    conn = await connection()

    if conn is None:
        return False

    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                tg_id BIGINT PRIMARY KEY,
                username VARCHAR(100)
            );

            CREATE TABLE IF NOT EXISTS chat(
                chat_id SERIAL PRIMARY KEY,
                tg_id BIGINT REFERENCES users(tg_id) ON DELETE CASCADE,
                chat_text TEXT,
                ai_text TEXT
            );
        """)

        print("Tables created successfully")
        return True

    except Exception as error:
        print(f"Error on Create table: {error}")
        return False

    finally:
        await conn.close()