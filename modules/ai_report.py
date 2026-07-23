"""
CORPO-RECON :: AI-Powered Executive Report Generator
Generates a structured penetration test summary from scan results.
Uses Google Gemini API if available, falls back to a local template.
"""

from __future__ import annotations

import json
import os
from datetime import datetime


def _build_prompt(recon_data: dict, target: str) -> str:
    """Build a structured LLM prompt from scan results."""
    dns = recon_data.get("dns_records", {})
    subs = recon_data.get("subdomains", [])
    live = recon_data.get("live_hosts", [])
    fuzz = recon_data.get("fuzz_paths", [])
    vuln = recon_data.get("vuln_data", [])
    cve = recon_data.get("cve_findings", [])
    ports = recon_data.get("open_ports", {})

    prompt = f"""You are a senior penetration tester writing an executive summary.
Analyze the following reconnaissance data for target: {target}

DNS Records: {json.dumps(dns, indent=2)}
Subdomains Discovered: {len(subs)}
Live Hosts: {len(live)}
Discovered Paths (Content Discovery): {json.dumps(fuzz, indent=2)}
Missing Security Headers: {json.dumps(vuln, indent=2)}
CVE / Misconfiguration Findings: {json.dumps(cve, indent=2)}
Open Ports: {json.dumps(ports, indent=2)}

Write a professional Executive Penetration Test Summary with:
1. EXECUTIVE SUMMARY (2-3 sentences)
2. RISK LEVEL (Critical / High / Medium / Low) with justification
3. KEY FINDINGS (numbered list with severity tags)
4. ATTACK SURFACE ANALYSIS (what an attacker could exploit)
5. RECOMMENDED MITIGATIONS (specific, actionable steps)
6. CONCLUSION

Use a clinical, professional tone. No emojis. No markdown headers with #.
Use plain text section headers in ALL CAPS followed by a line break."""

    return prompt


def _generate_local_report(recon_data: dict, target: str) -> str:
    """Generate a template-based report without any API dependency."""
    dns = recon_data.get("dns_records", {})
    subs = recon_data.get("subdomains", [])
    live = recon_data.get("live_hosts", [])
    fuzz = recon_data.get("fuzz_paths", [])
    vuln = recon_data.get("vuln_data", [])
    cve = recon_data.get("cve_findings", [])
    ports = recon_data.get("open_ports", {})

    open_ports = ports.get("ports", [])
    a_count = len(dns.get("a_records", []))
    mx_count = len(dns.get("mx_records", []))

    # Determine risk level
    risk = "LOW"
    if cve:
        risk = "CRITICAL"
    elif len(open_ports) > 5 or fuzz:
        risk = "HIGH"
    elif vuln:
        risk = "MEDIUM"

    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("CORPO-RECON :: EXECUTIVE PENETRATION TEST SUMMARY")
    lines.append("=" * 60)
    lines.append(f"Target: {target}")
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Overall Risk Level: {risk}")
    lines.append("")

    lines.append("EXECUTIVE SUMMARY")
    lines.append("-" * 40)
    lines.append(
        f"Reconnaissance of {target} identified {len(subs)} subdomains, "
        f"{len(live)} live hosts, {len(open_ports)} open ports, "
        f"and {len(cve)} critical misconfigurations. "
        f"The overall risk posture is assessed as {risk}."
    )
    lines.append("")

    lines.append("KEY FINDINGS")
    lines.append("-" * 40)
    finding_num = 1
    if cve:
        for c in cve:
            lines.append(f"  [{finding_num}] [CRITICAL] {c.get('issue', 'Unknown')} at {c.get('url', '-')}")
            finding_num += 1
    if fuzz:
        for f_item in fuzz:
            lines.append(f"  [{finding_num}] [HIGH] Exposed path /{f_item.get('path', '')} on {f_item.get('url', '-')} (HTTP {f_item.get('status', '-')})")
            finding_num += 1
    if vuln:
        for v in vuln:
            missing = ", ".join(v.get("missing_headers", []))
            if missing:
                lines.append(f"  [{finding_num}] [MEDIUM] Missing headers on {v.get('url', '-')}: {missing}")
                finding_num += 1
    if open_ports:
        for p in open_ports:
            lines.append(f"  [{finding_num}] [INFO] Open port {p.get('port', '-')}/{p.get('service', 'Unknown')}")
            finding_num += 1
    if finding_num == 1:
        lines.append("  No significant findings detected.")
    lines.append("")

    lines.append("RECOMMENDED MITIGATIONS")
    lines.append("-" * 40)
    if cve:
        lines.append("  > Immediately remediate all exposed sensitive files (.env, .git, phpinfo)")
        lines.append("  > Implement WAF rules to block access to configuration paths")
    if vuln:
        lines.append("  > Deploy missing security headers (HSTS, X-Frame-Options, X-Content-Type-Options)")
    if open_ports:
        lines.append("  > Review all open ports and close unnecessary services")
        lines.append("  > Implement network segmentation for exposed services")
    if fuzz:
        lines.append("  > Remove or restrict access to discovered backup and admin paths")
    lines.append("  > Conduct regular automated security assessments")
    lines.append("")

    lines.append("=" * 60)
    lines.append("END OF REPORT")
    lines.append("=" * 60)

    return "\n".join(lines)


def generate_report(recon_data: dict, target: str) -> str:
    """
    Generate an executive summary report.
    Tries Gemini API first, falls back to local template.
    Returns the output filename.
    """
    output_file = f"executive_report_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_text: str = ""

    # Try Gemini API
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            prompt = _build_prompt(recon_data, target)
            response = model.generate_content(prompt)
            report_text = response.text
        except Exception:
            report_text = ""

    # Fallback to local template
    if not report_text:
        report_text = _generate_local_report(recon_data, target)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_text)

    return output_file
