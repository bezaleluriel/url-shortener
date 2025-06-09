# URL Shortener

This is a simple URL shortener built with **FastAPI**. The app stores URL mappings in memory.
The repository includes minimal stub implementations of `fastapi` and `pydantic`
so the code and tests run without external dependencies.

## Endpoints

- `POST /shorten` - Provide a JSON body `{ "url": "https://example.com" }` to receive a short code.
- `GET /{code}` - Redirects to the long URL.

Run the server with `uvicorn main:app --reload`.

Run tests with `pytest`.
