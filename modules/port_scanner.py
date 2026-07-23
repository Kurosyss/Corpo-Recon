"""
CORPO-RECON :: Port Scanner Module
Multi-threaded scan of the top 50 common TCP ports.
"""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


# ── Top 50 Ports ──────────────────────────────────────────────
TOP_50_PORTS: list[int] = [
    21, 22, 23, 25, 26, 53, 80, 81, 110, 111,
    113, 135, 139, 143, 179, 199, 443, 445, 465,
    514, 515, 548, 554, 587, 646, 993, 995, 1025,
    1026, 1027, 1433, 1720, 1723, 2000, 2001, 3306,
    3389, 5060, 5666, 5900, 6001, 8000, 8008, 8080,
    8443, 8888, 9100, 9999, 10000, 32768,
]

PORT_SERVICE_MAP: dict[int, str] = {
    21: "FTP",       22: "SSH",       23: "Telnet",    25: "SMTP",
    26: "SMTP-ALT",  53: "DNS",       80: "HTTP",      81: "HTTP-ALT",
    110: "POP3",     111: "RPC",      113: "IDENT",    135: "MSRPC",
    139: "NetBIOS",  143: "IMAP",     179: "BGP",      199: "SMUX",
    443: "HTTPS",    445: "SMB",      465: "SMTPS",    514: "Syslog",
    515: "LPD",      548: "AFP",      554: "RTSP",     587: "Submission",
    646: "LDP",      993: "IMAPS",    995: "POP3S",    1025: "NFS",
    1026: "LSA",     1027: "IIS",     1433: "MSSQL",   1720: "H.323",
    1723: "PPTP",    2000: "Cisco",   2001: "DC",      3306: "MySQL",
    3389: "RDP",     5060: "SIP",     5666: "NRPE",    5900: "VNC",
    6001: "X11",     8000: "HTTP-ALT", 8008: "HTTP-ALT", 8080: "HTTP-Proxy",
    8443: "HTTPS-ALT", 8888: "HTTP-ALT", 9100: "JetDirect",
    9999: "AAAS",    10000: "Webmin", 32768: "FileMaker",
}


def _scan_single(host: str, port: int, timeout: float) -> dict | None:
    """Probe a single TCP port. Returns result dict if open, None if closed."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if sock.connect_ex((host, port)) == 0:
                return {
                    "port": port,
                    "state": "OPEN",
                    "service": PORT_SERVICE_MAP.get(port, "Unknown"),
                }
    except (socket.timeout, socket.error, OSError):
        pass
    return None


def run_port_scan(
    domain: str,
    timeout: float = 1.0,
    workers: int = 25,
) -> dict:
    """
    Execute multi-threaded port scan across top 50 TCP ports.

    Returns
    -------
    {
        "host": "93.184.216.34" | None,
        "ports": [{"port": 80, "state": "OPEN", "service": "HTTP"}, ...],
        "error": None | "error message",
    }
    """
    try:
        host: str = socket.gethostbyname(domain)
    except socket.gaierror:
        return {"host": None, "ports": [], "error": f"Cannot resolve {domain}"}

    open_ports: list[dict] = []

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(_scan_single, host, port, timeout): port
            for port in TOP_50_PORTS
        }
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                open_ports.append(result)

    open_ports.sort(key=lambda r: r["port"])
    return {"host": host, "ports": open_ports, "error": None}
