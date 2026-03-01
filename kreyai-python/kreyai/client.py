# kreyai/client.py
import time
import requests
from typing import Optional

from .errors import KreyAIError

DEFAULT_BASE_URL = "https://api.kreyai.com/v1"


class Client:
    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL, timeout: int = 60):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    # -------------------------
    # Internal helper
    # -------------------------
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
        }

    # -------------------------
    # Public API
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
        url = f"{self.base_url}/transcriptions"

        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {
                "language": language,
                "output_format": output_format,
                "diarization": str(diarization).lower(),
                "timestamps": str(timestamps).lower(),
            }

            resp = requests.post(
                url,
                headers=self._headers(),
                files=files,
                data=data,
                timeout=self.timeout,
            )

        if resp.status_code != 200:
            raise KreyAIError.from_response(resp)

        return resp.json()

    def get_job(self, job_id: str) -> dict:
        url = f"{self.base_url}/jobs/{job_id}"
        resp = requests.get(url, headers=self._headers(), timeout=self.timeout)

        if resp.status_code != 200:
            raise KreyAIError.from_response(resp)

        return resp.json()

    def wait(
        self,
        job_id: str,
        *,
        poll_interval: float = 2.0,
        timeout: Optional[float] = None,
    ) -> dict:
        start = time.time()

        while True:
            job = self.get_job(job_id)
            status = job.get("status")

            if status in ("completed", "failed"):
                return job

            if timeout is not None and (time.time() - start) > timeout:
                raise TimeoutError(f"Job {job_id} did not complete in time")

            time.sleep(poll_interval)
