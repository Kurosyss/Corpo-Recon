"""
CORPO-RECON :: Result Renderers
All monochromatic Rich table/text renderers for scan output.
"""

from __future__ import annotations

from rich.text import Text
from rich.table import Table
from rich import box

from utils.logger import console, GLOW, LIGHT, DARK, MUTED, PTR, BORDER, RED


def done_line(label: str) -> None:
    """Print a grey > label  DONE status line."""
    line = Text()
    line.append("  > ", style=PTR)
    line.append(f"{label}  ", style=DARK)
    line.append("DONE", style=GLOW)
    console.print(line)


def _make_table() -> Table:
    """Factory for a standard monochrome borderless table."""
    return Table(
        box=box.SIMPLE,
        show_edge=False,
        border_style=BORDER,
        header_style=LIGHT,
        pad_edge=False,
        padding=(0, 2),
    )


def render_dns(data: dict) -> None:
    """Render DNS records (A, MX, TXT) as a monochrome table."""
    tbl = _make_table()
    tbl.add_column("TYPE", style=PTR, width=6, no_wrap=True)
    tbl.add_column("VALUE", style=LIGHT)
    tbl.add_column("PRI", style=DARK, width=6, justify="right")

    has_rows = False
    for rec in data.get("a_records", []):
        tbl.add_row(rec["type"], rec["value"], "-")
        has_rows = True
    for rec in data.get("mx_records", []):
        tbl.add_row(rec["type"], rec["value"], rec.get("priority", "-"))
        has_rows = True
    for rec in data.get("txt_records", []):
        val = rec["value"]
        if len(val) > 80:
            val = val[:77] + "..."
        tbl.add_row(rec["type"], val, "-")
        has_rows = True

    if not has_rows:
        tbl.add_row("-", "No records detected", "-")

    console.print(tbl)


def render_subdomains(data: list[str] | str) -> None:
    """Render OSINT subdomains as a monochrome table."""
    tbl = _make_table()
    tbl.add_column("SUBDOMAIN", style=LIGHT)

    if isinstance(data, str):
        tbl.add_row(data)
    elif data:
        for sub in data:
            tbl.add_row(sub)
    else:
        tbl.add_row("No subdomains detected")

    console.print(tbl)


def render_live_hosts(data: list[dict]) -> None:
    """Render live hosts with tech/WAF fingerprint columns."""
    tbl = _make_table()
    tbl.add_column("URL", style=LIGHT)
    tbl.add_column("TECH", style=MUTED, width=20, no_wrap=True)
    tbl.add_column("WAF", style=DARK, width=12, no_wrap=True)
    tbl.add_column("STATUS", style=GLOW, justify="right")

    if data:
        for host in data:
            tbl.add_row(
                host["url"],
                host.get("tech", "Unknown"),
                host.get("waf", "-"),
                str(host["status"]),
            )
    else:
        tbl.add_row("No live hosts detected", "-", "-", "-")

    console.print(tbl)


def render_fuzzing(data: list[dict]) -> None:
    """Render discovered paths from content fuzzing."""
    tbl = _make_table()
    tbl.add_column("TARGET URL", style=MUTED)
    tbl.add_column("DISCOVERED PATH", style=LIGHT)
    tbl.add_column("STATUS", style=GLOW, justify="right")

    if data:
        for item in data:
            tbl.add_row(item["url"], f"/{item['path']}", str(item["status"]))
    else:
        tbl.add_row("-", "No hidden content detected", "-")

    console.print(tbl)


def render_vuln_scan(data: list[dict]) -> None:
    """Render security header / tech scan results."""
    tbl = _make_table()
    tbl.add_column("TARGET URL", style=MUTED)
    tbl.add_column("SERVER / TECH", style=LIGHT)
    tbl.add_column("MISSING HEADERS", style=GLOW)

    if data:
        for item in data:
            tech_str = ", ".join(item["tech"]) if item["tech"] else "-"
            headers_str = ", ".join(item["missing_headers"]) if item["missing_headers"] else "-"
            server_tech = f"{item['server']} | {tech_str}" if tech_str != "-" else item["server"]
            if len(headers_str) > 50:
                headers_str = headers_str[:47] + "..."
            tbl.add_row(item["url"], server_tech, headers_str)
    else:
        tbl.add_row("-", "No tech or headers detected", "-")

    console.print(tbl)


def render_cve(data: list[dict]) -> None:
    """Render CVE / misconfiguration findings."""
    tbl = _make_table()
    tbl.add_column("VULNERABLE ENDPOINT", style=MUTED)
    tbl.add_column("IDENTIFIED ISSUE", style=RED)
    tbl.add_column("STATUS", style=GLOW, justify="right")

    if data:
        for vuln in data:
            tbl.add_row(vuln["url"], vuln["issue"], str(vuln["status"]))
    else:
        tbl.add_row("-", "No critical leaks detected", "-")

    console.print(tbl)


def render_ports(data: dict) -> None:
    """Render open port scan results."""
    tbl = _make_table()
    tbl.add_column("PORT", style=PTR, width=8, no_wrap=True)
    tbl.add_column("SERVICE", style=LIGHT, width=16)
    tbl.add_column("STATE", style=GLOW, width=8)

    if data.get("error"):
        tbl.add_row("-", data["error"], "ERROR")
    elif data["ports"]:
        for p in data["ports"]:
            tbl.add_row(str(p["port"]), p["service"], p["state"])
    else:
        tbl.add_row("-", "No open ports detected", "-")

    console.print(tbl)
