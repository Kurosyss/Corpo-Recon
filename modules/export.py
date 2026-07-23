"""
CORPO-RECON :: Export Module
Automated data export to JSON or TXT format.
"""

from __future__ import annotations

import json
import os


def save_results(recon_data: dict, output_file: str) -> str | None:
    """
    Export recon_data to output_file based on extension (.json or .txt).
    Returns None on success, or an error string on failure.
    """
    try:
        ext = os.path.splitext(output_file)[1].lower()

        with open(output_file, "w", encoding="utf-8") as f:
            if ext == ".json":
                json.dump(recon_data, f, indent=4)
            else:
                _write_txt(f, recon_data)

        return None
    except PermissionError:
        return "Permission Denied"
    except OSError as e:
        return f"OS Error: {e}"
    except Exception as e:
        return f"Export Failed: {e}"


def _write_txt(f, recon_data: dict) -> None:
    """Write a human-readable TXT report."""
    target = recon_data.get("target_name") or recon_data.get("scan_metadata", {}).get("target", "UNKNOWN")
    f.write(f"CORPO-RECON EXPORT :: {target}\n")
    f.write("=" * 60 + "\n\n")

    # DNS
    f.write("[DNS RECORDS]\n")
    dns = recon_data.get("dns_records", {})
    for rec_type in ("a_records", "mx_records", "txt_records"):
        for rec in dns.get(rec_type, []):
            val = rec.get("value", "")
            pri = f" (PRI: {rec.get('priority')})" if rec.get("priority") else ""
            f.write(f"  {rec.get('type')}\t{val}{pri}\n")
    f.write("\n")

    # Subdomains
    f.write("[SUBDOMAINS]\n")
    subs = recon_data.get("subdomains", [])
    if isinstance(subs, list) and subs and not str(subs[0]).startswith("ERROR"):
        for sub in subs:
            f.write(f"  {sub}\n")
    else:
        f.write("  No subdomains detected.\n")
    f.write("\n")

    # Live Hosts
    f.write("[LIVE HOSTS]\n")
    for host in recon_data.get("live_hosts", []):
        tech = host.get("tech", "Unknown")
        waf = host.get("waf", "-")
        f.write(f"  {host.get('status')}\t{host.get('url')}\t(Tech: {tech} | WAF: {waf})\n")
    f.write("\n")

    # Discovered Paths
    f.write("[DISCOVERED PATHS]\n")
    paths = recon_data.get("fuzz_paths", [])
    if paths:
        for p in paths:
            f.write(f"  {p.get('status')}\t{p.get('url')}/{p.get('path')}\n")
    else:
        f.write("  No hidden content detected.\n")
    f.write("\n")

    # Vulnerability Scan
    f.write("[VULNERABILITY SCAN]\n")
    for v in recon_data.get("vuln_data", []):
        server = v.get("server", "Hidden")
        missing = ", ".join(v.get("missing_headers", []))
        f.write(f"  {v.get('url')}\tServer: {server}\tMissing: {missing or 'None'}\n")
    f.write("\n")

    # CVE Findings
    f.write("[CVE / MISCONFIGURATIONS]\n")
    cve = recon_data.get("cve_findings", [])
    if cve:
        for c in cve:
            f.write(f"  {c.get('status')}\t{c.get('url')}\t{c.get('issue')}\n")
    else:
        f.write("  No critical leaks detected.\n")
    f.write("\n")

    # Open Ports
    f.write("[OPEN PORTS]\n")
    ports_data = recon_data.get("open_ports", {})
    if ports_data.get("error"):
        f.write(f"  ERROR: {ports_data['error']}\n")
    else:
        for p in ports_data.get("ports", []):
            f.write(f"  {p.get('port')}\t{p.get('service')}\t{p.get('state')}\n")
    f.write("\n")
