import logging
from typing import Any

import requests

BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

logger = logging.getLogger(__name__)


class MetMuseumClient:
    def __init__(self, base_url: str = BASE_URL, timeout: float = 20.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, path: str, params: dict[str, Any] | None = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.info("Request: %s params=%s", url, params)

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
        except requests.RequestException as exc:
            logger.error("Request failed: %s params=%s error=%s", url, params, exc)
            raise

        logger.info("Response: %s %s", response.status_code, response.url)
        logger.debug("Body: %s", response.text[:2000])

        if not response.ok:
            logger.warning(
                "Unsuccessful response: status=%s url=%s body=%s",
                response.status_code,
                response.url,
                response.text[:500],
            )

        return response

    def get_object(self, object_id: int) -> requests.Response:
        return self._request(f"/objects/{object_id}")

    def search(self, **params: Any) -> requests.Response:
        return self._request("/search", params=params)
