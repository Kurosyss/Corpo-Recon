<div align="center">
  <h1>CORPO-RECON</h1>
  <p><b>Advanced Corporate Reconnaissance & Financial Risk Engine</b></p>
</div>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-white.svg?style=for-the-badge&logo=python&logoColor=black" alt="Python">
  <img src="https://img.shields.io/badge/UI-Rich-white.svg?style=for-the-badge&logo=cli&logoColor=black" alt="Rich">
  <img src="https://img.shields.io/badge/Environment-Isolated-white.svg?style=for-the-badge" alt="Environment">
  <img src="https://img.shields.io/badge/License-MIT-white.svg?style=for-the-badge" alt="License">
</div>

<br>

## THE OVERVIEW

Corpo-Recon is a stealthy, asynchronous, terminal-native reconnaissance platform engineered specifically for elite red teams, security researchers, and corporate risk analysts. Operating entirely within a strict, high-contrast monochromatic command-line interface, it systematically extracts, correlates, and analyzes organizational threat surfaces. The architecture is designed to bypass the visual noise of traditional security tooling, delivering actionable intelligence through a state-machine style telemetry dashboard.

The engine executes with clinical, methodical precision. It seamlessly bridges the gap between passive open-source intelligence gathering and deep-web financial anomaly detection—moving fluidly from DNS vulnerability enumeration to querying SEC EDGAR databases and sweeping Tor hidden services. Corpo-Recon prioritizes operational discretion and structured log output, ensuring operators maintain absolute tactical clarity without UI clutter.

<br>

<div align="center">
  <img src="./assets/Corpo-Recon.png" alt="Corpo-Recon Terminal Execution" width="850">
</div>

---

## CORE ARCHITECTURE

The execution pipeline is divided into nine specialized modules, designed to sequentially map out the entire operational, network, and financial footprint of a target organization.

| Module | Technical Execution Protocol |
| :--- | :--- |
| **Kernel Sandbox** | Initializes an isolated, ephemeral execution environment to ensure secure telemetry collection and mitigate reverse-engineering risks during active scans. |
| **Threat Intel DB** | Establishes encrypted upstream database connections to synchronize the latest adversarial signatures and threat intelligence indicators. |
| **DNS Recon Engine** | Executes comprehensive nameserver resolution, conducts zone transfer vulnerability assessments, and systematically parses TXT, MX, and SPF records. |
| **Email Intelligence** | Probes target mail exchangers via SMTP protocols and validates the enforcement of DKIM and DMARC policies against domain spoofing architectures. |
| **OSINT Pipelines** | Automates the scraping of public records and regulatory filings while algorithmically correlating social graph metadata to extract organizational hierarchies. |
| **Network Scanner** | Performs stealthy port scanning across common service infrastructure, fingerprints web technology stacks, and analyzes SSL/TLS certificate chains for cryptographic decay. |
| **Dark Web Index** | Connects autonomously to Tor relay nodes to execute deep-sweeps across hidden service directories, identifying compromised corporate credentials or proprietary data leaks. |
| **Financial Engine** | Queries the SEC EDGAR database to extract financial filings, executes anomaly detection algorithms against fiscal data, and calculates a composite corporate risk score. |
| **Report Generator** | Compiles all acquired telemetry into a structured executive brief and encrypts the resulting session artifacts to ensure strict chain of custody and data integrity. |

---

## SYSTEM REQUIREMENTS & INSTALLATION

The framework requires a secure, Unix-like environment (Linux/macOS or WSL2) for optimal socket operations and Tor routing.

```bash
# Clone the repository into a secure directory
git clone [https://github.com/Kurosyss/Corpo-Recon.git](https://github.com/Kurosyss/Corpo-Recon.git)
cd Corpo-Recon

# Initialize an isolated virtual environment
python3 -m venv recon-env
source recon-env/bin/activate

# Install core dependencies
pip install -r requirements.txt
```

---

## DEPLOYMENT & EXECUTION

Initialize the engine and specify the target domain. The tool supports granular execution modes to control the operator's digital footprint.

**Surface Scan Protocol:**
Executes passive OSINT pipelines, DNS reconnaissance, and network perimeter mapping. The Dark Web and Financial modules remain on standby to minimize operational noise and API exhaustion.

```bash
python main.py -t target-corp.com
```

**Deep Scan Protocol:**
Engages the complete reconnaissance suite. The `--deep-scan` flag explicitly authorizes connections to Tor relay nodes and initiates aggressive financial anomaly analysis.

```bash
python main.py -t target-corp.com --deep-scan
```

---

## LEGAL & OPERATIONAL DISCLAIMER

Corpo-Recon is intended strictly for authorized security auditing, defensive research, and corporate risk analysis. The developers and contributors assume absolutely no liability for the misuse of this tool. Operators must ensure total compliance with all applicable local, state, and federal laws, as well as the terms of service of any third-party infrastructure interacted with during a scan. Engaging in unauthorized reconnaissance or hostile operations against targets without explicit, documented consent is strictly prohibited.