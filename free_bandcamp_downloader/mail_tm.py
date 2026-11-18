"""Minimal client for the mail.tm disposable email API (https://docs.mail.tm)."""

import secrets
import string
from typing import Dict, List

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

API_URL = "https://api.mail.tm"


class MailTmSession:
    """A freshly created mail.tm inbox. Not thread safe."""

    def __init__(self):
        self.session = requests.Session()
        # the API allows 8 requests per second per IP
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=None,
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

        domain = next(
            d["domain"]
            for d in self._request("GET", "/domains").json()["hydra:member"]
            if d["isActive"] and not d["isPrivate"]
        )
        alphabet = string.ascii_lowercase + string.digits
        local_part = "".join(secrets.choice(alphabet) for _ in range(16))
        self.address = f"{local_part}@{domain}"
        credentials = {"address": self.address, "password": secrets.token_urlsafe(24)}
        self._request("POST", "/accounts", json=credentials)
        token = self._request("POST", "/token", json=credentials).json()["token"]
        self.session.headers["Authorization"] = f"Bearer {token}"

    def get_messages(self) -> List[Dict]:
        """Summaries (no body) of every message in the inbox, across all pages."""
        messages = []
        page = 1
        while True:
            data = self._request("GET", "/messages", params={"page": page}).json()
            members = data["hydra:member"]
            messages += members
            if not members or len(messages) >= data["hydra:totalItems"]:
                return messages
            page += 1

    def get_message(self, message_id: str) -> Dict:
        """Full message, including the `text` and `html` bodies."""
        return self._request("GET", f"/messages/{message_id}").json()

    def delete_message(self, message_id: str):
        self._request("DELETE", f"/messages/{message_id}")

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        r = self.session.request(method, API_URL + path, timeout=30, **kwargs)
        r.raise_for_status()
        return r
