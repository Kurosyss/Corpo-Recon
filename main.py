"""
CORPO-RECON :: Entry Point
Methodical scan with structured log output.
Usage: python main.py -t <target> [--deep-scan]
"""

import argparse
import time
import random

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


# ── Module Registry ───────────────────────────────────────────
MODULES_LIST = [
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


# ── Operation Sequence ────────────────────────────────────────
#   (tag, description, base_duration_sec, modules_to_mark_done, deep_scan_only)

def build_operations(deep_scan: bool) -> list[tuple]:
    """Builds the ordered operation manifest."""
    ops: list[tuple] = [
        # ── INIT ──
        ("[INIT]",  "Loading threat intelligence signatures",    0.6,  [],                                  False),
        ("[INIT]",  "Initializing sandbox environment",          0.5,  ["Kernel Sandbox"],                  False),
        ("[INIT]",  "Establishing upstream database connections", 0.7, ["Threat Intel DB"],                 False),

        # ── DNS ──
        ("[DNS]",   "Resolving target nameservers",              0.8,  [],                                  False),
        ("[DNS]",   "Enumerating subdomains via wordlist",       1.3,  [],                                  False),
        ("[DNS]",   "Checking zone transfer vulnerability",      0.6,  [],                                  False),
        ("[DNS]",   "Parsing TXT, MX, and SPF records",          0.9,  ["DNS Recon Engine"],                False),

        # ── SMTP ──
        ("[SMTP]",  "Probing mail exchangers",                   0.7,  [],                                  False),
        ("[SMTP]",  "Validating DKIM and DMARC policy",          0.9,  ["Email Intelligence"],              False),

        # ── OSINT ──
        ("[OSINT]", "Scraping public records and filings",       1.1,  [],                                  False),
        ("[OSINT]", "Correlating social media profiles",          1.4,  [],                                  False),
        ("[OSINT]", "Extracting organizational metadata",         0.9,  ["OSINT Pipelines"],                False),

        # ── NET ──
        ("[NET]",   "Scanning common service ports",              1.1, [],                                  False),
        ("[NET]",   "Fingerprinting web technology stack",        0.8, [],                                  False),
        ("[NET]",   "Analyzing SSL/TLS certificate chain",        0.7, ["Network Scanner"],                 False),

        # ── DARK (deep-scan only) ──
        ("[DARK]",  "Connecting to Tor relay nodes",              1.5, [],                                  True),
        ("[DARK]",  "Sweeping hidden service directories",        1.7, ["Dark Web Index"],                  True),

        # ── FIN (deep-scan only) ──
        ("[FIN]",   "Querying SEC EDGAR database",                1.3, [],                                  True),
        ("[FIN]",   "Running financial anomaly detection",        1.6, [],                                  True),
        ("[FIN]",   "Calculating composite risk score",           0.9, ["Financial Engine"],                True),

        # ── SYS ──
        ("[SYS]",   "Compiling executive report",                 0.7, [],                                  False),
        ("[SYS]",   "Encrypting session artifacts",               0.4, ["Report Generator"],               False),
    ]

    # Filter: keep all ops if deep_scan, otherwise skip deep_scan_only ops
    return [
        (tag, desc, dur, mods)
        for tag, desc, dur, mods, deep_only in ops
        if not deep_only or deep_scan
    ]


# ── Phase Map ─────────────────────────────────────────────────
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


# ── Argument Parser ───────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="corpo-recon",
        description="Corpo-Recon \u2014 Corporate Reconnaissance Engine",
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target domain, company, or email",
    )
    parser.add_argument(
        "--deep-scan",
        action="store_true",
        default=False,
        help="Enable deep-scan (dark web sweep, financial analysis)",
    )
    return parser


# ── Main ──────────────────────────────────────────────────────
def main() -> None:
    args = build_parser().parse_args()

    # Build ops
    operations = build_operations(args.deep_scan)

    # Initialize module states
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

    def render():
        return make_layout(
            banner,
            make_module_panel(modules, frame),
            make_log_panel(log_entries, frame),
            make_footer(args.target, args.deep_scan, phase),
        )

    # ── Live Dashboard ────────────────────────────────────────
    with Live(
        render(),
        console=console,
        refresh_per_second=20,
        screen=True,
    ) as live:

        for tag, desc, base_dur, trigger_modules in operations:

            # Mark trigger modules as loading
            for mod in trigger_modules:
                if modules.get(mod) == "pending":
                    modules[mod] = "loading"

            # Add log entry as running
            entry = {"tag": tag, "desc": desc, "status": "running"}
            log_entries.append(entry)

            # Update phase
            phase = PHASE_MAP.get(tag, "SCANNING")

            # Animate: spinner runs while "working"
            jitter = random.uniform(0.8, 1.2)
            duration = base_dur * jitter
            t_start = time.time()
            while time.time() - t_start < duration:
                frame += 1
                live.update(render())
                time.sleep(0.05)

            # Mark operation done
            entry["status"] = "done"

            # Mark trigger modules done
            for mod in trigger_modules:
                modules[mod] = "done"

            # Brief beat after DONE appears before next line
            live.update(render())
            time.sleep(0.15)

        # ── Hold final state ──────────────────────────────────
        phase = "COMPLETE"
        for _ in range(80):     # 4 seconds at 20 fps
            frame += 1
            live.update(render())
            time.sleep(0.05)

    # ── Clean Exit Summary ────────────────────────────────────
    console.print()

    done_mods = sum(1 for s in modules.values() if s == "done")
    total_ops = len(operations)

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

    console.print(summary)
    console.print()


if __name__ == "__main__":
    main()
