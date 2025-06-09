import json

class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str | None = None):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail

class Response:
    def __init__(self, content: str | None = None, status_code: int = 200, headers: dict[str, str] | None = None):
        self.content = content or ""
        self.status_code = status_code
        self.headers = headers or {}
    def json(self):
        return json.loads(self.content)

class RedirectResponse(Response):
    def __init__(self, url: str, status_code: int = 307):
        super().__init__(content="", status_code=status_code, headers={"location": url})
        self.url = url

class FastAPI:
    def __init__(self):
        self.routes = []  # (method, path, func)

    def post(self, path: str):
        def decorator(func):
            self.routes.append(("POST", path, func))
            return func
        return decorator

    def get(self, path: str):
        def decorator(func):
            self.routes.append(("GET", path, func))
            return func
        return decorator

    def resolve(self, method: str, path: str):
        for m, p, func in self.routes:
            if m == method:
                params = self._match(p, path)
                if params is not None:
                    return func, params
        raise HTTPException(status_code=404)

    @staticmethod
    def _match(template: str, path: str):
        if template == path:
            return {}
        if template.startswith('/') and template.count('{') == 1 and template.endswith('}'):
            prefix = template.split('{', 1)[0]
            param = template.split('{', 1)[1][:-1]
            if path.startswith(prefix):
                value = path[len(prefix):]
                return {param: value}
        return None


# minimal TestClient in this module for simplicity
class TestClient:
    __test__ = False  # prevent pytest from collecting this as a test class
    def __init__(self, app: FastAPI):
        self.app = app

    def post(self, path: str, json: dict | None = None, allow_redirects: bool = True):
        func, params = self.app.resolve("POST", path)
        try:
            result = func(type("Body", (), json or {}))
        except HTTPException as e:
            return Response(status_code=e.status_code)
        return self._make_response(result)

    def get(self, path: str, allow_redirects: bool = True):
        func, params = self.app.resolve("GET", path)
        try:
            result = func(**params)
        except HTTPException as e:
            return Response(status_code=e.status_code)
        return self._make_response(result)

    @staticmethod
    def _make_response(result):
        if isinstance(result, Response):
            return result
        return Response(json.dumps(result), status_code=200, headers={"content-type": "application/json"})
