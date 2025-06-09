from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import secrets
import string

app = FastAPI()

url_db: dict[str, str] = {}

ALPHABET = string.ascii_letters + string.digits

class URLRequest(BaseModel):
    url: str

def generate_code(length: int = 6) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

@app.post('/shorten')
def shorten(req: URLRequest) -> dict[str, str]:
    code = generate_code()
    while code in url_db:
        code = generate_code()
    url_db[code] = req.url
    return {"code": code}

@app.get('/{code}')
def redirect(code: str):
    if code not in url_db:
        raise HTTPException(status_code=404, detail="Not found")
    return RedirectResponse(url_db[code])
