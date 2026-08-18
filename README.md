<div align="center">
  <img src="./assets/corpo_recon_banner.jpg" alt="Corpo-Recon Hero Banner" width="100%">
  <br><br>
  <h1>C O R P O — R E C O N</h1>
  <p><i>Advanced Corporate Reconnaissance & Financial Risk Engine</i></p>
  <br>
  <img src="https://img.shields.io/badge/Python-3.9+-1a1a1a.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  &nbsp;
  <img src="https://img.shields.io/badge/License-MIT-1a1a1a.svg?style=for-the-badge" alt="License">
  &nbsp;
  <img src="https://img.shields.io/badge/UI-Rich_Terminal-1a1a1a.svg?style=for-the-badge&logo=gnometerminal&logoColor=white" alt="Rich UI">
  &nbsp;
  <img src="https://img.shields.io/badge/Build-Stable-1a1a1a.svg?style=for-the-badge" alt="Stable">
  <br><br>
  <code>Asynchronous. Monochromatic. Methodical.</code>
</div>

<br>

---

<br>

## SYSTEM OVERVIEW

**Corpo-Recon** is a terminal-native corporate reconnaissance platform engineered for elite red teams, security researchers, and financial risk analysts operating in high-stakes environments. It seamlessly bridges passive open-source intelligence gathering with deep-web financial anomaly detection and AI-driven telemetry synthesis.

The interface is strictly functional. There are no chaotic hex dumps or scrolling waterfalls of unreadable data. Every operation is structured as a sequential telemetry log: each task is dispatched, executed, and confirmed before the next begins. Operators maintain a clear tactical picture at all times.

Built on a modular Python architecture and the `rich` library, the dashboard renders a live two-panel layout — module status on the left, structured operation log on the right — using only shades of grey and bold white against a black terminal. The result is an instrument panel designed for absolute focus.

> *"No noise. No clutter. Just structured, actionable intelligence delivered with clinical precision."*

<br>

---

<br>

<div align="center">
  <img src="./assets/Corpo-Recon.png" alt="Corpo-Recon Terminal Telemetry" width="850">
  <br>
  <sup>Deep Scan execution against <code>acme-corp.com</code> — all 9 modules online, 22 operations complete.</sup>
</div>

<br>

---

<br>

## CORE ARCHITECTURE

The execution pipeline is composed of nine isolated modules. Each module is purpose-built to map a specific dimension of the target organization's operational and financial footprint.

<br>

| ID | Module | Execution Protocol | Scan Mode |
|:---:|:---|:---|:---:|
| **01** | **Kernel Sandbox** | Initializes an isolated, ephemeral execution environment to secure telemetry. | `SURFACE` `DEEP` |
| **02** | **Threat Intel DB** | Establishes encrypted connections to synchronize adversarial signatures. | `SURFACE` `DEEP` |
| **03** | **DNS Recon Engine** | Executes full nameserver resolution, zone transfer assessment (AXFR). | `SURFACE` `DEEP` |
| **04** | **Email Intelligence**| Probes mail exchangers via SMTP and validates DKIM/DMARC alignment. | `SURFACE` `DEEP` |
| **05** | **OSINT Pipelines** | Automates the scraping of public records and corporate registries. | `SURFACE` `DEEP` |
| **06** | **Network Scanner** | Performs stealthy port scanning and analyzes SSL/TLS certificates. | `SURFACE` `DEEP` |
| **07** | **Dark Web Index** | Connects autonomously to Tor relays and executes deep-sweeps across `.onion`. | `DEEP` only |
| **08** | **Financial Engine** | Queries SEC EDGAR database, executes anomaly detection algorithms. | `DEEP` only |
| **09** | **AI Report Gen**| Leverages Gemini API to compile telemetry into an executive brief. | `SURFACE` `DEEP` |
| **10** | **Trap Buster Fuzzer**| Asynchronous engine with honeypot detection to map hidden endpoints. | `SURFACE` `DEEP` |
| **11** | **Nuclei Vuln Engine**| Automates ProjectDiscovery's Nuclei for deep vulnerability correlation. | `SURFACE` `DEEP` |
| **12** | **Topology Visualizer**| Generates a Palantir-style HTML force-graph of the corporate infrastructure. | `SURFACE` `DEEP` |

<br>

> **Note:** Modules 07 (`Dark Web Index`) and 08 (`Financial Engine`) remain on `STANDBY` during a Surface Scan. They are activated exclusively by the `--deep-scan` flag.

<br>

---

<br>

## DEPLOYMENT & EXECUTION

### Prerequisites

[ SYSTEM TERMINAL ]
> git clone https://github.com/Kurosyss/corpo-recon.git
> cd corpo-recon
> python -m venv venv
> source venv/bin/activate        # macOS / Linux (WSL)
> venv\Scripts\activate           # Windows
> pip install -r requirements.txt
> cp .env.example .env

<br>

### Surface Scan Protocol

Executes passive reconnaissance — OSINT, DNS enumeration, email intelligence, and network perimeter mapping.

[ CORPO-RECON :: SURFACE ]
> python main.py -t target-corp.com

<br>

### Deep Scan Protocol

Engages the complete reconnaissance suite. The `--deep-scan` flag explicitly authorizes connections to Tor relay nodes and initiates financial anomaly analysis.

[ CORPO-RECON :: DEEP ]
> python main.py -t target-corp.com --deep-scan

<br>

### Command Reference

| Flag | Description |
|:---|:---|
| `-t`, `--target` | **Required.** Target domain, company name, or email address to investigate. |
| `--deep-scan` | Enables Dark Web Index and Financial Engine modules. |
| `-v`, `--verbose`| Activates Beast Mode for real-time streaming console feedback. |

<br>

---

<br>

## OPERATIONAL PHASES

[+] INITIALIZING    Sandbox boot, threat signature sync, upstream DB connections.
[+] DNS RECON       Nameserver resolution, subdomain enumeration, zone transfer checks.
[+] EMAIL INTEL     SMTP probing, DKIM/DMARC policy validation.
[+] OSINT SWEEP     Public records scraping, social graph correlation, metadata extraction.
[+] NETWORK SCAN    Port scanning, tech fingerprinting, SSL/TLS certificate analysis.
[+] WAF FUZZING     Heuristic honeypot evasion and asynchronous path discovery.
[+] VULN SCANNING   Nuclei template automation and deep CVE correlation.
[+] DARK WEB        Tor relay connection, hidden service directory sweeps.        (Deep only)
[+] FINANCIAL       SEC EDGAR queries, anomaly detection, composite risk scoring. (Deep only)
[+] TOPOLOGY MAP    Generation of interactive dark-mode HTML infrastructure graph.
[+] SYNTHESIZING    AI API integration for data correlation and executive report generation.
[+] FINALIZING      Session artifact encryption and local storage.
[+] COMPLETE        All modules online. All operations confirmed.

<br>

---

<br>

## LEAD ARCHITECT

**Corpo-Recon** is conceptualized, designed, and maintained by **Kurosyss (Piyush)**. 

* **Cybersecurity & OSINT Researcher**
* [GitHub Profile](https://github.com/Kurosyss)

*For professional inquiries, security audits, or red-team collaborations, reach out via direct channels.*

## LEGAL & OPERATIONAL DISCLAIMER

This software is intended **strictly** for authorized security auditing, defensive threat research, and corporate risk analysis conducted under explicit written authorization. 

The developers and contributors of Corpo-Recon assume **no liability** for misuse, unauthorized deployment, or any damages arising from the operation of this tool. Engaging in unauthorized reconnaissance is **strictly prohibited** and may constitute a criminal offense.
