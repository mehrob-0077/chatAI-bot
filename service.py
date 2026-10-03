from connection import connection
import requests
import os
from dotenv import load_dotenv

load_dotenv()

it = os.getenv("AI_TOKEN")


async def save_user(tg_id, username):
    conn = await connection()

    if conn is None:
        return

    try:
        user = await conn.fetchrow("""
            SELECT tg_id FROM users
            WHERE tg_id = $1
        """, tg_id)

        if user is None:
            await conn.execute("""
                INSERT INTO users(tg_id, username)
                VALUES($1, $2)
            """, tg_id, username)

    except Exception as error:
        print(f"Error in Save User: {error}")

    finally:
        await conn.close()


async def get_history(tg_id):
    conn = await connection()

    if conn is None:
        return []

    try:
        rows = await conn.fetch("""
            SELECT chat.chat_text, chat.ai_text FROM users
            JOIN chat ON users.tg_id = chat.tg_id
            WHERE users.tg_id = $1
            ORDER BY chat.chat_id ASC
        """, tg_id)

        history = []

        for row in rows:
            history.append({
                "role": "user",
                "content": row["chat_text"]
            })

            history.append({
                "role": "assistant",
                "content": row["ai_text"]
            })

        return history

    except Exception as error:
        print(f"Error in get history: {error}")
        return []

    finally:
        await conn.close()


def get_message(message, history):

    messages = history.copy()

    messages.append({
        "role": "user",
        "content": message
    })

    response = requests.post(
        "https://api.inceptionlabs.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {it}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mercury-2.5",
            "reasoning_effort": "high",
            "messages": messages
        }
    )

    if response.status_code != 200:
        print("AI Error:", response.text)
        return "AI ҷавоб дода натавонист."

    data = response.json()

    if "choices" not in data:
        print("AI Error:", data)
        return "Ҷавоби AI гирифта нашуд."

    return data["choices"][0]["message"]["content"]


async def save_text(tg_id, chat_text, ai_text):

    conn = await connection()

    if conn is None:
        return

    try:
        await conn.execute("""
            INSERT INTO chat(tg_id, chat_text, ai_text)
            VALUES($1, $2, $3)
        """, tg_id, chat_text, ai_text)

        print("Chat saved successfully")

    except Exception as error:
        print(f"Error in Add Text: {error}")

    finally:
        await conn.close()