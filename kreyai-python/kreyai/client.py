# kreyai/client.py

import requests
from .errors import AuthenticationError, RateLimitError, APIError


class KreyAI:
    """
    Thin Python client for KreyAI API v1 (Stable).
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.kreyai.com/v1",
        timeout: int = 300,
    ):
        if not api_key:
            raise ValueError("API key is required")

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "kreyai-python/1.0",
            }
        )

    # -------------------------
    # Core API
    # -------------------------
    def transcribe(
        self,
        file_path: str,
        *,
        language: str = "auto",
        output_format: str = "json",
        diarization: bool = False,
        timestamps: bool = True,
    ) -> dict:
        """
        Submit a transcription job.
        """

        with open(file_path, "rb") as f:
            response = self.session.post(
                f"{self.base_url}/transcriptions",
                files={"file": f},
                data={
                    "language": language,
                    "output_format": output_format,
                    "diarization": diarization,
                    "timestamps": timestamps,
                },
                timeout=self.timeout,
            )

        self._handle_errors(response)
        return response.json()

    # -------------------------
    # Internal helpers
    # -------------------------
    def _handle_errors(self, response: requests.Response) -> None:
        if response.status_code == 401:
            raise AuthenticationError("Invalid API key")

        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")

        if response.status_code >= 500:
            raise APIError("KreyAI server error")

        if response.status_code >= 400:
            raise APIError(response.text)
