# kreyai/errors.py
class KreyAIError(Exception):
    def __init__(self, message: str, code: str = "unknown_error", status_code: int = 0):
        super().__init__(message)
        self.code = code
        self.status_code = status_code

    @classmethod
    def from_response(cls, response):
        try:
            payload = response.json()
            err = payload.get("error", {})
            return cls(
                message=err.get("message", response.text),
                code=err.get("code", "api_error"),
                status_code=response.status_code,
            )
        except Exception:
            return cls(
                message=response.text,
                code="api_error",
                status_code=response.status_code,
            )
