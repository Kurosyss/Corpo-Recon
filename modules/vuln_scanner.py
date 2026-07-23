"""
CORPO-RECON :: Vulnerability Scanner Module
Checks for missing security headers and identifies server technology.
"""

from __future__ import annotations

import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_HEADERS: dict[str, str] = {"User-Agent": "Mozilla/5.0 Corpo-Recon/1.0"}

_SECURITY_HEADERS: list[str] = [
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def _analyze_target(url: str) -> dict | None:
    """Analyze a single URL for tech stack and missing security headers."""
    result: dict = {
        "url": url,
        "server": "Hidden",
        "tech": [],
        "missing_headers": [],
    }

    try:
        resp = requests.get(url, headers=_HEADERS, timeout=5, verify=False)

        if "Server" in resp.headers:
            result["server"] = resp.headers["Server"]
        if "X-Powered-By" in resp.headers:
            result["tech"].append(resp.headers["X-Powered-By"])

        for sh in _SECURITY_HEADERS:
            if sh not in resp.headers:
                result["missing_headers"].append(sh)

        return result
    except requests.RequestException:
        return None


def run_vuln_scan(live_urls: list[str]) -> list[dict]:
    """Run the vulnerability scanner across all live hosts."""
    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(_analyze_target, url): url for url in live_urls}
        for future in as_completed(futures):
            res = future.result()
            if res is not None:
                results.append(res)
    return results