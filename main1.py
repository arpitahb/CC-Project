from fastapi import FastAPI, HTTPException
import hashlib

app = FastAPI()

# Dictionary to store URL mappings
url_mappings = {}

# Function to generate a short URL
def generate_short_url(url):
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()[:8]  # Customize the length as needed

# API endpoint to shorten a URL
@app.post("/shorten")
async def shorten_url(url: str):
    if url in url_mappings:
        return {"short_url": url_mappings[url]}

    short_url = generate_short_url(url)
    url_mappings[url] = short_url

    return {"short_url": short_url}

# API endpoint to expand a short URL
@app.get("/{short_url}")
async def expand_url(short_url: str):
    for url, mapped_short_url in url_mappings.items():
        if mapped_short_url == short_url:
            return {"original_url": url}

    raise HTTPException(status_code=404, detail="Short URL not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
