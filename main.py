from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
import hashlib
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import starlette.status as status
from mangum import Mangum
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
client = AsyncIOMotorClient("mongodb+srv://arpitahb2002:Arpitahb2002@cluster0.g2zzw60.mongodb.net/?retryWrites=true&w=majority")
database = client["shorturl"]
collection = database["urls"] 


# Function to generate a short URL
def generate_short_url(url):
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()[:8]  # Customize the length as needed

# @app.get("/")
# async def read_index():
#     html_path = Path("frontend") / "index.html"
#     return FileResponse(html_path)

@app.get('/test/hello')
def hello_api(name: str = 'World'):
    return {"hello": name}

# API endpoint to shorten a URL
@app.post("/generate/shorten")
async def shorten_url(body: dict):
    short_url = generate_short_url(body.get('url'))
    try:
        await collection.insert_one({"original_url": body.get('url'), "short_url": short_url})
        return {"short_url": short_url}
    
    except DuplicateKeyError:
        return {"short_url": short_url}



# API endpoint to expand a short URL
@app.get("/li/{short_url}")
async def expand_url(short_url: str):
    result = await collection.find_one({"short_url": short_url})
    if result:
        # return {"original_url": result["original_url"]}
        return RedirectResponse(url=result["original_url"], status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")



app.mount("/", StaticFiles(directory="frontend"), name="static")


@app.get("/")
async def read_index():
    html_path = Path("frontend") / "index.html"
    return FileResponse(html_path)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, port=8000)

handler = Mangum(app)