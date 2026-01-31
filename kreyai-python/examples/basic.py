# kreyai/errors.py

class KreyAIError(Exception):
    """Base SDK error."""


class AuthenticationError(KreyAIError):
    """Invalid or missing API key."""


class RateLimitError(KreyAIError):
    """Quota or rate limit exceeded."""


class APIError(KreyAIError):
    """Server-side error."""
