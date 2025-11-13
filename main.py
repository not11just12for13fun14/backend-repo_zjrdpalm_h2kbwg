import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Hoodie, ContactMessage

app = FastAPI(title="Hoodie Wala API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hoodie Wala API running"}

# Public endpoints

@app.get("/hoodies", response_model=List[Hoodie])
def list_hoodies():
    try:
        docs = get_documents("hoodie")
        # Convert ObjectId to str and map to Hoodie
        hoodies = []
        for d in docs:
            d.pop("_id", None)
            hoodies.append(Hoodie(**d))
        return hoodies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/contact")
def send_contact(msg: ContactMessage):
    try:
        _id = create_document("contactmessage", msg)
        return {"status": "ok", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Seed a couple of hoodies if collection is empty
@app.post("/seed")
def seed():
    try:
        existing = get_documents("hoodie", limit=1)
        if existing:
            return {"seeded": False, "message": "Hoodies already exist"}
        sample = [
            Hoodie(
                name="Classic Black Hoodie",
                description="Soft fleece-lined hoodie with kangaroo pocket.",
                price=39.99,
                colors=["Black"],
                sizes=["S","M","L","XL"],
                image_url="https://images.unsplash.com/photo-1541099649105-f69ad21f3246?q=80&w=1600&auto=format&fit=crop",
            ),
            Hoodie(
                name="Streetwear Grey Hoodie",
                description="Oversized fit with premium cotton blend.",
                price=49.99,
                colors=["Grey"],
                sizes=["M","L","XL"],
                image_url="https://images.unsplash.com/photo-1603252109303-2751441dd157?q=80&w=1600&auto=format&fit=crop",
            ),
        ]
        for h in sample:
            create_document("hoodie", h)
        return {"seeded": True, "count": len(sample)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
