<div align="center">

```
   ___                          ____
  / __|___ _ _ _ __  ___ ___   |  _ \ ___  ___ ___  _ __
 | |  / _ \ '_| '_ \/ _ \___| | |_) / _ \/ __/ _ \| '_ \
 | |_| (_) | | | |_) \___  |  |  _ <  __/ (_| (_) | | | |
  \___\___/|_| | .__/|___/    |_| \_\___|\___\___/|_| |_|
               |_|
```

**Corporate Reconnaissance & Attack Surface Management Engine**

![Python](https://img.shields.io/badge/Python-3.12+-333333?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-333333?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-333333?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Cross--Platform-333333?style=flat-square)

---

*Monochromatic. Modular. Methodical.*

</div>

---

## Overview

Corpo-Recon is a terminal-native corporate reconnaissance engine designed for red teams, security researchers, and corporate risk analysts. It operates as a modular, multi-phase scanning pipeline with a strictly monochromatic Rich UI — no color noise, no clutter, just structured intelligence output.

The tool chains DNS enumeration, OSINT subdomain discovery, live host probing, technology fingerprinting, content discovery, vulnerability scanning, CVE matching, and port analysis into a single automated pipeline with structured JSON/TXT export.

---

## Architecture

```
Corpo-Recon/
  main.py                  Entry point (9 lines)
  core/
    cli.py                 Argument parser + custom help
    engine.py              Scan orchestrator (boot, recon, export)
    renderer.py            Monochrome Rich table renderers
  modules/
    dns_recon.py            A / MX / TXT record extraction
    osint_recon.py          crt.sh + HackerTarget subdomain enum
    http_probe.py           Concurrent HTTP/HTTPS live host probing
    fingerprint.py          Server tech + WAF signature detection
    fuzzer.py               Content discovery with catch-all detection
    vuln_scanner.py         Missing security header analysis
    cve_matcher.py          Exposed file / misconfiguration scanner
    port_scanner.py         Top 50 TCP port scanner (25 threads)
    export.py               JSON / TXT structured data export
    ai_report.py            AI-powered executive summary generator
  utils/
    logger.py               Ghost Palette UI engine (Rich layouts)
```

---

## Scan Modules

| Module | Description | Method |
|:---|:---|:---|
| DNS Recon | Extract A, MX, TXT records | `dnspython` resolver |
| OSINT Recon | Subdomain enumeration | crt.sh + HackerTarget API |
| Live Host Probing | HTTP/HTTPS availability check | Concurrent `requests` |
| Tech Fingerprint | Server banner + WAF detection | Header + cookie analysis |
| Content Discovery | Hidden file/directory fuzzing | Threaded wordlist scan |
| Vuln Scanner | Missing security header audit | HSTS, XFO, XCTO checks |
| CVE Matcher | Exposed config/file detection | .git, .env, swagger, phpinfo |
| Port Scanner | Top 50 TCP port sweep | 25-thread `socket` probe |
| AI Report | Executive penetration test summary | Gemini API / local template |

---

## Prerequisites

```
> Python 3.12+
> pip (package manager)
> Network access to target
```

---

## Installation

```bash
git clone https://github.com/yourname/corpo-recon.git
cd corpo-recon
pip install -r requirements.txt
```

---

## Usage

```bash
# Surface scan with auto-saved JSON report
python main.py -t example.com

# Deep scan with custom output file
python main.py -t example.com --deep-scan -o results.json

# Generate AI-powered executive summary
python main.py -t example.com --ai-report

# Export as formatted text
python main.py -t example.com -o report.txt
```

---

## CLI Reference

| Flag | Description | Required |
|:---|:---|:---|
| `-t`, `--target` | Target domain | Yes |
| `--deep-scan` | Enable deep-scan (extended boot sequence) | No |
| `-o`, `--output` | Output file path (.json or .txt) | No |
| `--ai-report` | Generate AI executive summary | No |
| `-h`, `--help` | Show monochrome help menu | No |

---

## Output Formats

**JSON** — Machine-readable structured export containing all scan data: DNS records, subdomains, live hosts (with tech/WAF fingerprints), discovered paths, vulnerability findings, CVE matches, and open ports. Suitable for pipeline automation.

**TXT** — Human-readable formatted report with section headers and tabulated findings. Designed for direct inclusion in penetration test deliverables.

**AI Report** — Executive penetration test summary with risk levels, key findings, attack surface analysis, and actionable mitigation steps. Powered by Google Gemini API with automatic local template fallback.

---

## Environment Variables

| Variable | Purpose |
|:---|:---|
| `GEMINI_API_KEY` | Google Gemini API key for AI report generation (optional) |

---

## Roadmap

```
[x] Multi-phase boot dashboard with Rich Live UI
[x] DNS / OSINT / Live Host / Port scanning pipeline
[x] WAF + Tech fingerprinting
[x] Content discovery with catch-all detection
[x] Vulnerability + CVE scanning
[x] JSON / TXT structured export
[x] AI-powered executive report generation
[ ] WHOIS + ASN enrichment module
[ ] SSL certificate chain analysis
[ ] Email security audit (SPF/DKIM/DMARC deep analysis)
[ ] HTML report generation with embedded charts
[ ] Plugin system for custom scan modules
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

*Built for precision. Designed for professionals.*

</div>
