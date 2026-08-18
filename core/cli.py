"""
CORPO-RECON :: CLI Interface
Custom monochromatic argument parser and help formatter.
"""

from __future__ import annotations

import sys
import argparse

from rich.text import Text
from rich.table import Table
from rich import box

from utils.logger import console, GLOW, LIGHT, DARK, MUTED, PTR, BORDER


def print_custom_help() -> None:
    """Render a strictly monochromatic help menu, bypassing argparse defaults."""
    console.print()

    header = Text()
    header.append("  CORPO-RECON ", style=GLOW)
    header.append("\u2014 Corporate Reconnaissance Engine\n", style=DARK)
    console.print(header)

    usage = Text()
    usage.append("  USAGE: ", style=MUTED)
    usage.append("python main.py -t <target> [options]\n", style=LIGHT)
    console.print(usage)

    tbl = Table(
        box=box.SIMPLE,
        show_header=False,
        show_edge=False,
        border_style=BORDER,
        pad_edge=False,
        padding=(0, 2),
    )
    tbl.add_column("FLAG", style=PTR, width=18)
    tbl.add_column("DESC", style=LIGHT)

    tbl.add_row("-t, --target", "Target domain (Required)")
    tbl.add_row("--deep-scan", "Enable deep-scan (dark web + financial analysis)")
    tbl.add_row("-o, --output", "Export results (e.g., results.json or results.txt)")
    tbl.add_row("--ai-report", "Generate AI-powered executive summary")
    tbl.add_row("-h, --help", "Show this help message and exit")

    console.print(tbl)
    console.print()
    sys.exit(0)


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with custom help interception."""
    if "-h" in sys.argv or "--help" in sys.argv:
        print_custom_help()

    parser = argparse.ArgumentParser(
        prog="corpo-recon",
        description="Corpo-Recon \u2014 Corporate Reconnaissance Engine",
        add_help=False,
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target domain",
    )
    parser.add_argument(
        "--deep-scan",
        action="store_true",
        default=True,
        help="Enable deep-scan (dark web sweep, financial analysis)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file for results (.json or .txt)",
    )
    parser.add_argument(
        "--ai-report",
        action="store_true",
        default=True,
        help="Generate AI-powered executive summary",
    )
    return parser
