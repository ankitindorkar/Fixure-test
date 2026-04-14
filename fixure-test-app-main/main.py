from fastapi import FastAPI, HTTPException, Query
import os
import sqlite3

app = FastAPI()

# Secure secret handling
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("SECRET_KEY not set")

@app.get("/")
def read_root():
    return {"message": "Hello Fixure User"}

@app.get("/items/{item_id}")
def read_item(item_id: str):
    # Validate input
    if not item_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid item_id")

    return {"item_id": item_id}

@app.get("/search")
def search(user_input: str = Query(..., min_length=1, max_length=50)):
    if not user_input.isalnum():
        raise HTTPException(status_code=400, detail="Invalid input")

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        query = "SELECT id, name FROM users WHERE name = ?"
        cursor.execute(query, (user_input,))

        results = cursor.fetchall()

        # ✅ FIX: Do NOT return raw DB output
        safe_results = [{"id": r[0], "name": r[1]} for r in results]

        return {"data": safe_results}

    except Exception:
        raise HTTPException(status_code=500, detail="Internal error")

    finally:
        conn.close()