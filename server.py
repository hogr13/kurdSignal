from fastapi import FastAPI, Request
import json
import os
import uvicorn

app = FastAPI(title="KurdSignal API", version="1.0")

# ناوی داتابەیسەکە
DB_FILE = "towers_database.json"

# دڵنیابوون لەوەی فایلی داتابەیسەکە هەیە
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

@app.post("/upload_tower_data")
async def receive_tower_data(request: Request):
    try:
        # وەرگرتنی داتا لە مۆبایلەکەوە
        new_data = await request.json()
        
        # خوێندنەوەی داتابەیسە کۆنەکە
        with open(DB_FILE, "r") as f:
            towers = json.load(f)
            
        # زیادکردنی داتا نوێیەکە
        towers.append(new_data)
        
        # پاشەکەوتکردنەوەی
        with open(DB_FILE, "w") as f:
            json.dump(towers, f, indent=4)
            
        return {"status": "success", "message": "داتاکە بە سەرکەوتوویی وەرگیرا"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def home():
    return {"message": "سێرڤەری KurdSignal بە سەرکەوتوویی کار دەکات! 🚀"}

# ئەم بەشە بۆ هەڵکردنی سێرڤەرەکە لەسەر کۆمپیوتەر و Render
if __name__ == "__main__":
    # Render پۆرتەکە لە ژینگەکە (Environment) دیاری دەکات، ئەگەر نەبوو 8000 بەکاربێنە
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)