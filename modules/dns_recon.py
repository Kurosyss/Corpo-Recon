"""
CORPO-RECON :: DNS Reconnaissance Module
Extracts A, MX, and TXT records for a target domain.
"""

import dns.resolver
import dns.exception


def _query(domain: str, rdtype: str) -> list[dict]:
    """Run a single DNS query and return normalized records."""
    results: list[dict] = []
    try:
        answers = dns.resolver.resolve(domain, rdtype, lifetime=8)
        for rdata in answers:
            entry: dict = {"type": rdtype, "value": str(rdata)}
            if rdtype == "MX":
                entry["value"] = str(rdata.exchange).rstrip(".")
                entry["priority"] = str(rdata.preference)
            results.append(entry)
    except dns.resolver.NoAnswer:
        pass                       # record type simply doesn't exist
    except dns.resolver.NXDOMAIN:
        results.append({"type": rdtype, "value": "NXDOMAIN — domain does not exist"})
    except dns.resolver.NoNameservers:
        results.append({"type": rdtype, "value": "ERROR — no reachable nameservers"})
    except dns.exception.Timeout:
        results.append({"type": rdtype, "value": "ERROR — query timed out"})
    except Exception as exc:       # noqa: BLE001
        results.append({"type": rdtype, "value": f"ERROR — {exc}"})
    return results


def run_dns_recon(domain: str) -> dict[str, list[dict]]:
    """
    Execute full DNS reconnaissance.

    Returns
    -------
    {
        "a_records":  [{"type": "A",   "value": "..."}],
        "mx_records": [{"type": "MX",  "value": "...", "priority": "10"}],
        "txt_records":[{"type": "TXT", "value": "..."}],
    }
    """
    return {
        "a_records":   _query(domain, "A"),
        "mx_records":  _query(domain, "MX"),
        "txt_records": _query(domain, "TXT"),
    }
