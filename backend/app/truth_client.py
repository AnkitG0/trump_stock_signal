import os 
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter, Retry

from .models import Post
from .config import get_settings

settings = get_settings()

API_KEY = settings.truth_social_api_key
BASE_URL = settings.truth_social_base_url


class ScrapeCreatorsError(Exception):
    """Base exception for ScrapeCreators API errors."""


class ScrapeCreatorsAuthError(ScrapeCreatorsError):
    """Authentication/authorization failures."""


class ScrapeCreatorsRateLimitError(ScrapeCreatorsError):
    """Rate limiting errors."""


class ScrapeCreatorsAPIResponseError(ScrapeCreatorsError):
    """Non-success responses from the API."""


def _get_session() -> requests.Session:
    """
    Create a requests session with retry strategy for transient errors.
    Retries on 429 / 5xx with backoff.
    """
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_truthsocial_posts(
    user_id: Optional[str] = None,
    handle: Optional[str] = None,
    next_max_id: Optional[str] = None,
    trim: bool = True,
    timeout: int = 10,
) -> Dict[str, Any]:
    """
    Fetch Truth Social posts via ScrapeCreators API.

    One of user_id or handle is required.
    Returns parsed JSON on success or raises a descriptive exception.
    """
    if not API_KEY:
        raise ScrapeCreatorsError(
            "Missing API key. Set SCRAPECREATORS_API_KEY environment variable."
        )

    if not (user_id or handle):
        raise ValueError("You must provide either user_id or handle.")

    params: Dict[str, Any] = {
        "trim": str(trim).lower(),  # API often expects 'true' / 'false' as strings
    }
    if user_id:
        params["user_id"] = user_id
    if handle:
        params["handle"] = handle
    if next_max_id:
        params["next_max_id"] = next_max_id

    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json",
    }

    session = _get_session()

    try:
        resp = session.get(BASE_URL, headers=headers, params=params, timeout=timeout)
    except requests.exceptions.Timeout as e:
        raise ScrapeCreatorsError(
            f"Request to ScrapeCreators timed out after {timeout}s."
        ) from e
    except requests.exceptions.RequestException as e:
        raise ScrapeCreatorsError(f"Network error while calling ScrapeCreators: {e}") from e

    # Handle HTTP-level errors explicitly
    if resp.status_code == 401 or resp.status_code == 403:
        raise ScrapeCreatorsAuthError(
            f"Auth failed with status {resp.status_code}. "
            "Check that your x-api-key is correct and active."
        )
    if resp.status_code == 429:
        raise ScrapeCreatorsRateLimitError(
            "Rate limit hit (429). Slow down or add backoff before retrying."
        )
    if not (200 <= resp.status_code < 300):
        # Try to include error payload if present
        try:
            err_data = resp.json()
        except ValueError:
            err_data = resp.text
        raise ScrapeCreatorsAPIResponseError(
            f"Unexpected status {resp.status_code} from API: {err_data}"
        )

    # Parse JSON safely
    try:
        data = resp.json()
    except ValueError as e:
        raise ScrapeCreatorsError("Failed to parse JSON from ScrapeCreators.") from e

    # API-level success flag check
    if not isinstance(data, dict) or not data.get("success", False):
        raise ScrapeCreatorsAPIResponseError(
            f"API returned non-success response: {data}"
        )

    # Basic validation of expected keys
    posts = data.get("posts", [])
    if not isinstance(posts, list):
        raise ScrapeCreatorsAPIResponseError(
            f"Unexpected 'posts' format in response: {type(posts)}"
        )

    return data


def fetch_trump_posts(limit_pages: int = 1) -> List[Dict[str, Any]]:
    """
    Convenience helper: fetch Donald Trump's public posts.

    Uses user_id for efficiency.
    Paginates using next_max_id up to limit_pages.
    """
    user_id = "107780257626128497"
    all_posts: List[Dict[str, Any]] = []
    next_max_id = None

    for _ in range(limit_pages):
        data = get_truthsocial_posts(
            user_id=user_id,
            next_max_id=next_max_id,
            trim=True,
        )
        posts = data.get("posts", [])
        all_posts.extend(posts)
  
        next_max_id = data.get("next_max_id")
        if not next_max_id:
            break  # no more pages

    posts: List[Post] = []
    for item in all_posts:
        if item.get("text"):
            post = Post(
                id = item.get("id"),
                text = item.get("text"),
                created_at = _parse_datetime(item.get("created_at"))
            )
            posts.append(post)

    return posts

def _parse_datetime(value: str) -> datetime:
    """
    Helper to parse datetime strings from the API.
    Adjust if your API uses a different format.
    """

    # Common ISO8601 format with 'Z'
    # e.g. "2025-01-01T12:34:56Z"
    try:
        # Python 3.11+ has fromisoformat that doesn't handle 'Z' directly,
        # so we can replace 'Z' with '+00:00'
        if value.endswith("Z"):
            value = value.replace("Z", "+00:00")
        return datetime.fromisoformat(value)
    except Exception:
        # As a fallback, just return naive datetime without timezone
        return datetime.strptime(value[:19], "%Y-%m-%dT%H:%M:%S")

if __name__ == "__main__":
    posts = fetch_trump_posts()
    print(f"length of posts: {len(posts)}")
    for p in posts:
        print(p.created_at, '-', p.text)

