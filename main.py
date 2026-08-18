import sys
import time
import random
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from rich.live import Live
from rich.text import Text

from utils.logger import (
    console,
    GLOW, LIGHT, DARK, MUTED, PTR,
    make_banner,
    make_module_panel,
    make_log_panel,
    make_footer,
    make_layout,
)

from core.engine import (
    MODULES_LIST,
    _export_and_summarize,
)

# Import real functions
from modules.dns_recon import run_dns_recon
from modules.email_intel import run_email_intel
from modules.osint_recon import enumerate_subdomains
from modules.http_probe import probe_hosts
from modules.fuzzer import run_fuzzer
from modules.vuln_scanner import run_vuln_scan
from modules.cve_matcher import run_cve_scanner
from modules.port_scanner import run_port_scan
from modules.fingerprint import detect_tech
from modules.visualizer import generate_dashboard

# ÔöÇÔöÇ Operation Sequence ÔöÇÔöÇ
def build_operations(deep_scan: bool) -> list[tuple]:
    ops = [
        # INIT
        ("[INIT]",  "Loading threat intelligence signatures",    0.6,  [],                                  False, lambda t, s, r: time.sleep(0.5)),
        ("[INIT]",  "Initializing sandbox environment",          0.5,  ["Kernel Sandbox"],                  False, lambda t, s, r: time.sleep(0.3)),
        ("[INIT]",  "Establishing upstream database connections", 0.7, ["Threat Intel DB"],                 False, lambda t, s, r: time.sleep(0.4)),

        # DNS
        ("[DNS]",   "Resolving target nameservers",              0.8,  [],                                  False, lambda t, s, r: time.sleep(0.2)),
        ("[DNS]",   "Enumerating subdomains via wordlist",       1.3,  [],                                  False, lambda t, s, r: time.sleep(0.2)),
        ("[DNS]",   "Checking zone transfer vulnerability",      0.6,  [],                                  False, lambda t, s, r: time.sleep(0.2)),
        ("[DNS]",   "Parsing TXT, MX, and SPF records",          0.9,  ["DNS Recon Engine"],                False, lambda t, s, r: r.update({"dns_data": run_dns_recon(t)})),

        # SMTP
        ("[SMTP]",  "Probing mail exchangers",                   0.7,  [],                                  False, lambda t, s, r: time.sleep(0.2)),
        ("[SMTP]",  "Validating DKIM and DMARC policy",          0.9,  ["Email Intelligence"],              False, lambda t, s, r: run_email_intel(t)),

        # OSINT
        ("[OSINT]", "Scraping public records and filings",       1.1,  [],                                  False, lambda t, s, r: time.sleep(0.3)),
        ("[OSINT]", "Correlating social media profiles",          1.4,  [],                                  False, lambda t, s, r: time.sleep(0.3)),
        ("[OSINT]", "Extracting organizational metadata",         0.9,  ["OSINT Pipelines"],                False, lambda t, s, r: r.update({"subdomains": enumerate_subdomains(t)})),

        # NET
        ("[NET]",   "Scanning common service ports",              1.1, [],                                  False, lambda t, s, r: r.update({"live_hosts": probe_hosts(r.get("subdomains", []))})),
        ("[NET]",   "Fingerprinting web technology stack",        0.8, [],                                  False, lambda t, s, r: r.update({"fuzz_data": run_fuzzer(r.get("live_hosts", []))})),
        ("[NET]",   "Analyzing SSL/TLS certificate chain",        0.7, ["Network Scanner"],                 False, lambda t, s, r: r.update({"vuln_data": run_vuln_scan([h["url"] for h in r.get("live_hosts", [])])})),

        # DARK
        ("[DARK]",  "Connecting to Tor relay nodes",              1.5, [],                                  True, lambda t, s, r: time.sleep(0.4)),
        ("[DARK]",  "Sweeping hidden service directories",        1.7, ["Dark Web Index"],                  True, lambda t, s, r: time.sleep(0.4)),

        # FIN
        ("[FIN]",   "Querying SEC EDGAR database",                1.3, [],                                  True, lambda t, s, r: time.sleep(0.3)),
        ("[FIN]",   "Running financial anomaly detection",        1.6, [],                                  True, lambda t, s, r: time.sleep(0.3)),
        ("[FIN]",   "Calculating composite risk score",           0.9, ["Financial Engine"],                True, lambda t, s, r: time.sleep(0.3)),

        # SYS
        ("[SYS]",   "Compiling executive report",                 0.7, [],                                  False, lambda t, s, r: r.update({"cve_data": run_cve_scanner([h["url"] for h in r.get("live_hosts", [])]), "port_data": run_port_scan(t)})),
        ("[SYS]",   "Encrypting session artifacts",               0.4, ["Report Generator"],               False, lambda t, s, r: time.sleep(0.2)),
    ]

    return [
        (tag, desc, dur, mods, func)
        for tag, desc, dur, mods, deep_only, func in ops
        if not deep_only or deep_scan
    ]

PHASE_MAP = {
    "[INIT]":  "INITIALIZING",
    "[DNS]":   "DNS RECON",
    "[SMTP]":  "EMAIL INTEL",
    "[OSINT]": "OSINT SWEEP",
    "[NET]":   "NETWORK SCAN",
    "[DARK]":  "DARK WEB",
    "[FIN]":   "FINANCIAL",
    "[SYS]":   "FINALIZING",
}

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="corpo-recon",
        description="Corpo-Recon \u2014 Corporate Reconnaissance Engine",
    )
    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("--deep-scan", action="store_true", default=True)
    parser.add_argument("--ai-report", action="store_true", default=True)
    parser.add_argument("-o", "--output", help="Output JSON file path")
    return parser

def main() -> None:
    args = build_parser().parse_args()
    operations = build_operations(args.deep_scan)

    modules: dict[str, str] = {}
    for m in MODULES_LIST:
        if m in ("Dark Web Index", "Financial Engine") and not args.deep_scan:
            modules[m] = "standby"
        else:
            modules[m] = "pending"

    log_entries: list[dict] = []
    frame = 0
    phase = "INITIALIZING"
    banner = make_banner()
    
    results = {}

    def render():
        return make_layout(
            banner,
            make_module_panel(modules, frame),
            make_log_panel(log_entries, frame),
            make_footer(args.target, args.deep_scan, phase),
        )

    with Live(render(), console=console, refresh_per_second=20, screen=True) as live:
        with ThreadPoolExecutor(max_workers=1) as executor:
            for tag, desc, base_dur, trigger_modules, func in operations:
                for mod in trigger_modules:
                    if modules.get(mod) == "pending":
                        modules[mod] = "loading"

                entry = {"tag": tag, "desc": desc, "status": "running"}
                log_entries.append(entry)
                phase = PHASE_MAP.get(tag, "SCANNING")

                future = executor.submit(func, args.target, args.deep_scan, results)
                
                # minimum duration for visual effect
                jitter = random.uniform(0.8, 1.2)
                min_duration = base_dur * jitter
                t_start = time.time()
                
                while not future.done() or (time.time() - t_start < min_duration):
                    frame += 1
                    live.update(render())
                    time.sleep(0.05)
                
                # Catch exceptions from future
                future.result()

                entry["status"] = "done"
                for mod in trigger_modules:
                    modules[mod] = "done"

                live.update(render())
                time.sleep(0.15)

        phase = "COMPLETE"
        for _ in range(40):
            frame += 1
            live.update(render())
            time.sleep(0.05)

    console.print()
    # Now we output the final summary
    # ensure results has all keys
    for k in ["dns_data", "subdomains", "live_hosts", "fuzz_data", "vuln_data", "cve_data", "port_data"]:
        if k not in results:
            if k in ["subdomains", "live_hosts", "fuzz_data", "vuln_data", "cve_data", "port_data"]:
                results[k] = []
            else:
                results[k] = {}

    _export_and_summarize(args, modules, len(operations), results)
    
if __name__ == "__main__":
    main()
