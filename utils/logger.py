"""
CORPO-RECON :: UI Engine
Ghost Monochrome Theme — Shades of Grey + Bold White Glow
"""

import sys
import io

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from rich import box


# ── Force UTF-8 on Windows ────────────────────────────────────
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace"
    )
if sys.stderr.encoding != "utf-8":
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding="utf-8", errors="replace"
    )


# ── Ghost Palette ─────────────────────────────────────────────
#   Only shades of grey and pure white.
#   No blue. No neon. No cyan. No green. No purple.
GLOW   = "bold white"       # Pure white glow — spinner, active highlight
LIGHT  = "#cccccc"           # Light grey — active/scanning text
DARK   = "#777777"           # Dark grey — inactive, descriptions
PTR    = "#808080"           # Grey — all > pointers and markers
BORDER = "#333333"           # Near-invisible borders
MUTED  = "#555555"           # Muted grey — secondary elements
RED    = "#8b0000"           # Dark red — critical only, used sparingly


# ── Console ───────────────────────────────────────────────────
console = Console(
    force_terminal=True,
    legacy_windows=False,
    highlight=False,
)


# ── Braille Spinner ───────────────────────────────────────────
BRAILLE = "\u280b\u2819\u2839\u2838\u283c\u2834\u2826\u2827\u2807\u280f"


# ── Banner ────────────────────────────────────────────────────
def make_banner() -> Panel:
    """Minimal bold white title. Nothing else."""
    title = Text("CORPO-RECON", style=GLOW, justify="center")
    return Panel(
        Align.center(title),
        border_style=BORDER,
        box=box.SIMPLE,
        padding=(0, 1),
        subtitle=f"[{MUTED}]Corporate Reconnaissance Engine[/{MUTED}]",
        subtitle_align="center",
    )


# ── Module Panel ──────────────────────────────────────────────
def make_module_panel(modules: dict, frame: int = 0) -> Panel:
    """
    modules: {name: "pending" | "loading" | "done" | "standby"}
    """
    content = Text()
    spinner = BRAILLE[frame % len(BRAILLE)]
    done_count = sum(1 for s in modules.values() if s == "done")
    total = len(modules)

    for name, status in modules.items():
        if status == "done":
            content.append("  > ", style=PTR)
            content.append(f"{name}\n", style=LIGHT)
        elif status == "loading":
            content.append(f"  {spinner} ", style=GLOW)
            content.append(f"{name}\n", style=LIGHT)
        elif status == "standby":
            content.append("  - ", style=MUTED)
            content.append(f"{name}\n", style=MUTED)
        else:
            content.append("    ")
            content.append(f"{name}\n", style=DARK)

    if done_count == total:
        title_str = f"[{GLOW}]MODULES [{done_count}/{total}][/{GLOW}]"
    else:
        title_str = f"[{DARK}]MODULES [{done_count}/{total}][/{DARK}]"

    return Panel(
        content,
        title=title_str,
        title_align="left",
        border_style=BORDER,
        box=box.SIMPLE,
        padding=(1, 1),
    )


# ── Log Panel ─────────────────────────────────────────────────
def make_log_panel(
    entries: list[dict],
    frame: int = 0,
    max_visible: int = 22,
) -> Panel:
    """
    Renders a structured, readable operations log.

    Each entry: {tag, desc, status}
    status: "running" | "done"
    """
    visible = entries[-max_visible:] if len(entries) > max_visible else entries
    content = Text()
    spinner = BRAILLE[frame % len(BRAILLE)]

    for entry in visible:
        tag = f"{entry['tag']:<7}"
        desc = entry["desc"]

        if entry["status"] == "done":
            content.append(f"  {tag} ", style=MUTED)
            content.append(desc, style=DARK)
            content.append("  DONE\n", style=GLOW)
        elif entry["status"] == "running":
            content.append(f"  {tag} ", style=DARK)
            content.append(desc, style=LIGHT)
            content.append(f"  {spinner}\n", style=GLOW)

    # Empty state
    if not entries:
        content.append("  Awaiting target lock...\n", style=MUTED)

    return Panel(
        content,
        title=f"[{DARK}]LOG[/{DARK}]",
        title_align="left",
        border_style=BORDER,
        box=box.SIMPLE,
        padding=(0, 1),
    )


# ── Footer ────────────────────────────────────────────────────
def make_footer(target: str, deep_scan: bool, phase: str = "") -> Panel:
    line = Text()
    line.append("  TARGET ", style=DARK)
    line.append(target, style=GLOW)
    line.append("  \u2502  ", style=BORDER)
    if deep_scan:
        line.append("DEEP", style=LIGHT)
    else:
        line.append("SURFACE", style=DARK)
    if phase:
        line.append("  \u2502  ", style=BORDER)
        line.append(phase, style=DARK)

    return Panel(
        Align.center(line),
        border_style=BORDER,
        box=box.SIMPLE,
        padding=(0, 0),
    )


# ── Layout ────────────────────────────────────────────────────
def make_layout(
    banner: Panel,
    module_panel: Panel,
    log_panel: Panel,
    footer: Panel,
) -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )
    layout["body"].split_row(
        Layout(name="modules", ratio=1, minimum_size=28),
        Layout(name="log", ratio=2),
    )

    layout["header"].update(banner)
    layout["modules"].update(module_panel)
    layout["log"].update(log_panel)
    layout["footer"].update(footer)

    return layout
