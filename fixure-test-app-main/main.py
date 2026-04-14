from fastapi import FastAPI, HTTPException
import os
import sqlite3

app = FastAPI()

# ✅ FIX 1: Load secret from environment variable
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise Exception("SECRET_KEY not set in environment")

@app.get("/")
def read_root():
    return {"message": "Hello Fixure User"}

@app.get("/items/{item_id}")
def read_item(item_id: str):
    # ✅ FIX 2: Do NOT expose secrets
    return {"item_id": item_id}

@app.get("/search")
def search(user_input: str):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # ✅ FIX 3: Use parameterized query (prevents SQL injection)
        query = "SELECT * FROM users WHERE name = ?"
        cursor.execute(query, (user_input,))

        results = cursor.fetchall()
        return {"data": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        conn.close()