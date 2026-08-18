"""
CORPO-RECON :: Scan Engine
Orchestrates the full reconnaissance pipeline: boot dashboard, active scans, export.
"""

from __future__ import annotations

import time
import random
from datetime import datetime

from rich.live import Live
from rich.text import Text

from utils.logger import (
    console,
    GLOW, LIGHT, DARK, MUTED, PTR, BORDER,
    make_banner,
    make_module_panel,
    make_log_panel,
    make_footer,
    make_layout,
)

from core.cli import build_parser
from core.renderer import (
    done_line,
    render_dns,
    render_subdomains,
    render_live_hosts,
    render_fuzzing,
    render_vuln_scan,
    render_cve,
    render_ports,
)

from modules.dns_recon import run_dns_recon
from modules.port_scanner import run_port_scan
from modules.osint_recon import enumerate_subdomains
from modules.http_probe import probe_hosts
from modules.fuzzer import run_fuzzer
from modules.vuln_scanner import run_vuln_scan
from modules.cve_matcher import run_cve_scanner
from modules.export import save_results
from modules.financial import analyze_financials
from modules.darkweb import sweep_darkweb
from modules.nuclei_engine import run_nuclei
from modules.visualizer import generate_dashboard
from modules.sandbox import init_sandbox
from modules.threat_intel import sync_threat_intel
from modules.email_intel import run_email_intel
from modules.fingerprint import detect_tech


# ── Module Registry ───────────────────────────────────────────
MODULES_LIST: list[str] = [
    "Kernel Sandbox",
    "Threat Intel DB",
    "DNS Recon Engine",
    "Email Intelligence",
    "OSINT Pipelines",
    "Network Scanner",
    "Dark Web Index",
    "Financial Engine",
    "Report Generator",
]


# ── Operation Manifest ────────────────────────────────────────
def _build_operations(deep_scan: bool) -> list[tuple[str, str, float, list[str]]]:
    """Build the ordered operation sequence for the boot dashboard."""
    ops: list[tuple[str, str, float, list[str], bool]] = [
        ("[INIT]",  "Loading threat intelligence signatures",    0.6,  [],                    False),
        ("[INIT]",  "Initializing sandbox environment",          0.5,  ["Kernel Sandbox"],    False),
        ("[INIT]",  "Establishing upstream database connections", 0.7, ["Threat Intel DB"],   False),
        ("[DNS]",   "Resolving target nameservers",              0.8,  [],                    False),
        ("[DNS]",   "Enumerating subdomains via wordlist",       1.3,  [],                    False),
        ("[DNS]",   "Checking zone transfer vulnerability",      0.6,  [],                    False),
        ("[DNS]",   "Parsing TXT, MX, and SPF records",          0.9,  ["DNS Recon Engine"],  False),
        ("[SMTP]",  "Probing mail exchangers",                   0.7,  [],                    False),
        ("[SMTP]",  "Validating DKIM and DMARC policy",          0.9,  ["Email Intelligence"],False),
        ("[OSINT]", "Scraping public records and filings",       1.1,  [],                    False),
        ("[OSINT]", "Correlating social media profiles",         1.4,  [],                    False),
        ("[OSINT]", "Extracting organizational metadata",        0.9,  ["OSINT Pipelines"],   False),
        ("[NET]",   "Scanning common service ports",             1.1,  [],                    False),
        ("[NET]",   "Fingerprinting web technology stack",       0.8,  [],                    False),
        ("[NET]",   "Analyzing SSL/TLS certificate chain",       0.7,  ["Network Scanner"],   False),
        ("[DARK]",  "Connecting to Tor relay nodes",             1.5,  [],                    True),
        ("[DARK]",  "Sweeping hidden service directories",       1.7,  ["Dark Web Index"],    True),
        ("[FIN]",   "Querying SEC EDGAR database",               1.3,  [],                    True),
        ("[FIN]",   "Running financial anomaly detection",       1.6,  [],                    True),
        ("[FIN]",   "Calculating composite risk score",          0.9,  ["Financial Engine"],  True),
        ("[SYS]",   "Compiling executive report",                0.7,  [],                    False),
        ("[SYS]",   "Encrypting session artifacts",              0.4,  ["Report Generator"],  False),
    ]
    return [
        (tag, desc, dur, mods)
        for tag, desc, dur, mods, deep_only in ops
        if not deep_only or deep_scan
    ]


# ── Phase Map ─────────────────────────────────────────────────
_PHASE_MAP: dict[str, str] = {
    "[INIT]":  "INITIALIZING",
    "[DNS]":   "DNS RECON",
    "[SMTP]":  "EMAIL INTEL",
    "[OSINT]": "OSINT SWEEP",
    "[NET]":   "NETWORK SCAN",
    "[DARK]":  "DARK WEB",
    "[FIN]":   "FINANCIAL",
    "[SYS]":   "FINALIZING",
}


# ── Boot Dashboard ────────────────────────────────────────────
def _run_boot_dashboard(
    target: str,
    deep_scan: bool,
    operations: list[tuple[str, str, float, list[str]]],
    modules: dict[str, str],
) -> None:
    """Execute the animated boot sequence dashboard."""
    log_entries: list[dict] = []
    frame: int = 0
    phase: str = "INITIALIZING"
    banner = make_banner()

    def render():
        return make_layout(
            banner,
            make_module_panel(modules, frame),
            make_log_panel(log_entries, frame),
            make_footer(target, deep_scan, phase),
        )

    with Live(render(), console=console, refresh_per_second=20, screen=True) as live:
        for tag, desc, base_dur, trigger_modules in operations:
            for mod in trigger_modules:
                if modules.get(mod) == "pending":
                    modules[mod] = "loading"

            entry: dict = {"tag": tag, "desc": desc, "status": "running"}
            log_entries.append(entry)
            phase = _PHASE_MAP.get(tag, "SCANNING")

            duration = base_dur * random.uniform(0.8, 1.2)
            t_start = time.time()
            while time.time() - t_start < duration:
                frame += 1
                live.update(render())
                time.sleep(0.05)

            entry["status"] = "done"
            for mod in trigger_modules:
                modules[mod] = "done"

            live.update(render())
            time.sleep(0.15)

        phase = "COMPLETE"
        for _ in range(60):
            frame += 1
            live.update(render())
            time.sleep(0.05)


# ── Active Reconnaissance ─────────────────────────────────────
def _run_recon(target: str, deep_scan: bool) -> dict:
    """Execute all active scan phases and return aggregated results."""
    console.print()
    header = Text()
    header.append("  RECONNAISSANCE", style=GLOW)
    header.append("  target=", style=MUTED)
    header.append(target, style=LIGHT)
    console.print(header)
    console.print()

    # ── Kernel Sandbox ────────────────────────────────────────
    with console.status(Text("  Initializing Kernel Sandbox", style=DARK), spinner="dots", spinner_style="bold white"):
        sandbox_data = init_sandbox()
    done_line("Kernel Sandbox")
    console.print()

    # ── Threat Intelligence ───────────────────────────────────
    with console.status(Text("  Syncing Threat Intel DB", style=DARK), spinner="dots", spinner_style="bold white"):
        threat_data = sync_threat_intel(target)
    done_line("Threat Intel DB")
    console.print()

    # ── DNS ───────────────────────────────────────────────────
    with console.status(Text("  DNS Reconnaissance", style=DARK), spinner="dots", spinner_style="bold white"):
        dns_data = run_dns_recon(target)
    done_line("DNS Reconnaissance")
    console.print()
    render_dns(dns_data)
    console.print()

    # ── Email Intelligence ────────────────────────────────────
    with console.status(Text("  Email Infrastructure Intelligence", style=DARK), spinner="dots", spinner_style="bold white"):
        email_data = run_email_intel(target)
    done_line("Email Intelligence")
    console.print()

    # ── OSINT ─────────────────────────────────────────────────
    with console.status(Text("  OSINT Reconnaissance", style=DARK), spinner="dots", spinner_style="bold white"):
        subdomains = enumerate_subdomains(target)
    done_line("OSINT Reconnaissance")
    console.print()
    render_subdomains(subdomains)
    console.print()

    # ── Live Hosts ────────────────────────────────────────────
    with console.status(Text("  Live Host Probing", style=DARK), spinner="dots", spinner_style="bold white"):
        live_hosts = probe_hosts(subdomains) if isinstance(subdomains, list) else []
    done_line("Live Host Probing")
    console.print()
    render_live_hosts(live_hosts)
    console.print()

    # ── Content Discovery ─────────────────────────────────────
    with console.status(Text("  Content Discovery", style=DARK), spinner="dots", spinner_style="bold white"):
        fuzz_data = run_fuzzer(live_hosts)
    done_line("Content Discovery")
    console.print()
    render_fuzzing(fuzz_data)
    console.print()

    # ── Vuln & Tech Scan ──────────────────────────────────────
    live_urls: list[str] = [h["url"] for h in live_hosts] if live_hosts else []

    with console.status(Text("  Vulnerability & Tech Scan", style=DARK), spinner="dots", spinner_style="bold white"):
        vuln_data = run_vuln_scan(live_urls)
    done_line("Vulnerability Scan")
    console.print()
    render_vuln_scan(vuln_data)
    console.print()
    
    # ── WAF & Fingerprint ─────────────────────────────────────
    fingerprints = []
    if live_urls:
        with console.status(Text("  WAF & Stack Fingerprinting", style=DARK), spinner="dots", spinner_style="bold white"):
            fingerprints = [detect_tech(url) for url in live_urls]
        done_line("Tech Fingerprint")
        console.print()

    # ── CVE / Leak Scan ───────────────────────────────────────
    with console.status(Text("  Deep CVE & Leakage Scan", style=DARK), spinner="dots", spinner_style="bold white"):
        cve_data = run_cve_scanner(live_urls)
    done_line("CVE Scan")
    console.print()
    render_cve(cve_data)
    console.print()

    # ── Port Scan ─────────────────────────────────────────────
    with console.status(Text("  Port Scan (50 ports)", style=DARK), spinner="dots", spinner_style="bold white"):
        port_data = run_port_scan(target)
    done_line("Port Scan")

    if port_data.get("host"):
        resolved = Text()
        resolved.append("    resolved ", style=MUTED)
        resolved.append(port_data["host"], style=LIGHT)
        console.print(resolved)

    console.print()
    render_ports(port_data)
    console.print()

    # ── Nuclei Engine ─────────────────────────────────────────
    with console.status(Text("  Nuclei Vulnerability Correlation", style=DARK), spinner="dots", spinner_style="bold white"):
        nuclei_data = run_nuclei(live_urls)
    done_line("Nuclei Scan")
    console.print()

    # ── Deep Scan Modules ─────────────────────────────────────
    financial_data = {}
    darkweb_data = {}
    if deep_scan:
        with console.status(Text("  Tor Dark Web Indexing", style=DARK), spinner="dots", spinner_style="bold white"):
            darkweb_data = sweep_darkweb(target)
        done_line("Dark Web Index")
        console.print()
        
        with console.status(Text("  SEC Financial Anomaly Detection", style=DARK), spinner="dots", spinner_style="bold white"):
            financial_data = analyze_financials(target)
        done_line("Financial Engine")
        console.print()

    return {
        "dns_data": dns_data,
        "subdomains": subdomains if isinstance(subdomains, list) else [],
        "live_hosts": live_hosts,
        "fuzz_data": fuzz_data,
        "vuln_data": vuln_data,
        "cve_data": cve_data,
        "nuclei_data": nuclei_data,
        "port_data": port_data,
        "financial_data": financial_data,
        "darkweb_data": darkweb_data,
        "sandbox_data": sandbox_data,
        "threat_data": threat_data,
        "email_data": email_data,
        "fingerprints": fingerprints,
    }


# ── Export & Summary ──────────────────────────────────────────
def _export_and_summarize(
    args,
    modules: dict[str, str],
    total_ops: int,
    results: dict,
) -> None:
    """Handle data export and print the final summary block."""
    dns_data = results["dns_data"]
    subdomains = results["subdomains"]
    live_hosts = results["live_hosts"]
    fuzz_data = results["fuzz_data"]
    vuln_data = results["vuln_data"]
    cve_data = results["cve_data"]
    port_data = results["port_data"]

    # ── Build recon payload ───────────────────────────────────
    recon_data: dict = {
        "scan_metadata": {
            "target": args.target,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": "deep" if args.deep_scan else "surface",
        },
        "dns_records": dns_data,
        "subdomains": subdomains,
        "live_hosts": live_hosts,
        "fuzz_paths": fuzz_data,
        "vuln_data": vuln_data,
        "cve_findings": cve_data,
        "nuclei_findings": results.get("nuclei_data", []),
        "open_ports": port_data,
        "financial_data": results.get("financial_data", {}),
        "darkweb_data": results.get("darkweb_data", {}),
        "sandbox_data": results.get("sandbox_data", {}),
        "threat_data": results.get("threat_data", {}),
        "email_data": results.get("email_data", {}),
        "fingerprints": results.get("fingerprints", []),
    }

    # ── Export ────────────────────────────────────────────────
    export_error: str | None = None
    output_file: str | None = args.output

    if not output_file:
        # Auto-save to timestamped JSON
        output_file = f"recon_{args.target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    export_error = save_results(recon_data, output_file)

    if export_error:
        msg = Text()
        msg.append("  > ", style=PTR)
        msg.append(f"Export failed: {export_error}", style=DARK)
        console.print(msg)
    else:
        msg = Text()
        msg.append("  > ", style=PTR)
        msg.append("Report saved  ", style=DARK)
        msg.append(output_file, style=GLOW)
        console.print(msg)

    console.print()

    # ── AI Report ─────────────────────────────────────────────
    ai_file: str | None = None
    ai_report_text: str | None = None
    if args.ai_report:
        try:
            from modules.ai_report import generate_report
            with console.status(Text("  Generating executive AI summary", style=DARK), spinner="dots", spinner_style="bold white"):
                ai_file, ai_report_text = generate_report(recon_data, args.target)
                recon_data["ai_report"] = ai_report_text
            done_line("AI Report")
            console.print()
        except Exception as e:
            msg = Text()
            msg.append("  > ", style=PTR)
            msg.append(f"AI report generation skipped ({e})", style=DARK)
            console.print(msg)
            console.print()

    # ── Visualizer / Dashboard ────────────────────────────────
    import os
    dashboard_file: str | None = None
    try:
        with console.status(Text("  Generating Executive HTML Dashboard", style=DARK), spinner="dots", spinner_style="bold white"):
            out_dir = os.path.join(os.getcwd(), "results")
            dashboard_file = generate_dashboard(recon_data, out_dir)
        done_line("Executive Dashboard")
        console.print()
    except Exception as e:
        msg = Text()
        msg.append("  > ", style=PTR)
        msg.append(f"Dashboard generation skipped ({str(e)})", style=DARK)
        console.print(msg)
        console.print()

    # ── Summary ───────────────────────────────────────────────
    console.rule(style=BORDER)
    console.print()

    done_mods = sum(1 for s in modules.values() if s == "done")
    a_count  = len(dns_data.get("a_records", []))
    mx_count = len(dns_data.get("mx_records", []))
    tx_count = len(dns_data.get("txt_records", []))
    p_count  = len(port_data.get("ports", []))
    s_count  = len(subdomains)
    l_count  = len(live_hosts)
    f_count  = len(fuzz_data)
    v_count  = len(vuln_data)
    c_count  = len(cve_data)

    summary = Text()
    summary.append("  CORPO-RECON ", style=GLOW)
    summary.append("scan complete.\n\n", style=DARK)
    summary.append("  Target      ", style=MUTED)
    summary.append(f"{args.target}\n", style=LIGHT)
    summary.append("  Mode        ", style=MUTED)
    summary.append(f"{'Deep Scan' if args.deep_scan else 'Surface Scan'}\n", style=LIGHT)
    summary.append("  Modules     ", style=MUTED)
    summary.append(f"{done_mods}/{len(modules)} online\n", style=LIGHT)
    summary.append("  Operations  ", style=MUTED)
    summary.append(f"{total_ops}/{total_ops} complete\n", style=LIGHT)
    summary.append("  DNS Records ", style=MUTED)
    summary.append(f"{a_count} A  {mx_count} MX  {tx_count} TXT\n", style=LIGHT)
    summary.append("  Subdomains  ", style=MUTED)
    summary.append(f"{s_count} detected\n", style=LIGHT)
    summary.append("  Live Hosts  ", style=MUTED)
    summary.append(f"{l_count} detected\n", style=LIGHT)
    summary.append("  Discovered  ", style=MUTED)
    summary.append(f"{f_count} paths\n", style=LIGHT)
    summary.append("  Vuln Scans  ", style=MUTED)
    summary.append(f"{v_count} analyzed\n", style=LIGHT)
    summary.append("  CVE Alerts  ", style=MUTED)
    summary.append(f"{c_count} detected\n", style=LIGHT)
    summary.append("  Open Ports  ", style=MUTED)
    summary.append(f"{p_count} detected\n", style=LIGHT)

    summary.append("  Report      ", style=MUTED)
    if export_error:
        summary.append(f"FAILED ({export_error})\n", style=LIGHT)
    else:
        summary.append(f"{output_file}\n", style=LIGHT)

    if dashboard_file:
        summary.append("  Dashboard   ", style=MUTED)
        summary.append(f"{dashboard_file}\n", style=LIGHT)

    if ai_file:
        summary.append("  AI Report   ", style=MUTED)
        summary.append(f"{ai_file}\n", style=LIGHT)

    console.print(summary)
    console.print()


# ── Entry Point ───────────────────────────────────────────────
def run() -> None:
    """Main entry point for the Corpo-Recon engine."""
    args = build_parser().parse_args()

    operations = _build_operations(args.deep_scan)

    modules: dict[str, str] = {}
    for m in MODULES_LIST:
        if m in ("Dark Web Index", "Financial Engine") and not args.deep_scan:
            modules[m] = "standby"
        else:
            modules[m] = "pending"

    # Phase 1: Boot dashboard
    _run_boot_dashboard(args.target, args.deep_scan, operations, modules)

    # Phase 2: Active reconnaissance
    results = _run_recon(args.target, args.deep_scan)

    # Phase 3: Export, AI report, and summary
    _export_and_summarize(args, modules, len(operations), results)
