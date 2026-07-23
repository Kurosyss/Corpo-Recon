"""
CORPO-RECON :: CVE & Misconfiguration Scanner
Checks for critical exposed files and misconfigurations on live hosts.
"""

from __future__ import annotations

import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_HEADERS: dict[str, str] = {"User-Agent": "Mozilla/5.0 Corpo-Recon/1.0"}

_RISKY_PATTERNS: list[dict[str, str]] = [
    {"path": ".git/HEAD",    "desc": "Git Repository Exposure (Critical)"},
    {"path": "swagger.json", "desc": "Exposed API Documentation"},
    {"path": "api/v1/",      "desc": "Unprotected API Endpoint"},
    {"path": "phpinfo.php",  "desc": "PHP Info Leakage"},
    {"path": ".env",         "desc": "Environment Variables Leakage"},
]


def _check_pattern(url: str, pattern: dict[str, str]) -> dict | None:
    """Check a single URL/pattern combination for exposure."""
    full_url = f"{url.rstrip('/')}/{pattern['path']}"
    try:
        resp = requests.get(
            full_url,
            headers=_HEADERS,
            timeout=5,
            verify=False,
            allow_redirects=False,
        )
        if resp.status_code == 200 and len(resp.content) > 0:
            content_type = resp.headers.get("Content-Type", "")
            if "html" not in content_type.lower() or ".git" in pattern["path"] or "json" in pattern["path"]:
                return {
                    "url": full_url,
                    "issue": pattern["desc"],
                    "status": resp.status_code,
                }
    except requests.RequestException:
        pass
    return None


def run_cve_scanner(live_urls: list[str]) -> list[dict]:
    """Scan live URLs for critical misconfigurations and exposed files."""
    findings: list[dict] = []
    tasks: list[tuple[str, dict[str, str]]] = [
        (url, pattern)
        for url in live_urls
        for pattern in _RISKY_PATTERNS
    ]

    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {
            executor.submit(_check_pattern, item[0], item[1]): item
            for item in tasks
        }
        for future in as_completed(futures):
            res = future.result()
            if res is not None:
                findings.append(res)

    return findings