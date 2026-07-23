"""
CORPO-RECON :: OSINT Reconnaissance Module
Dual-pipeline failover system for subdomain enumeration.
Queries crt.sh as primary, falls back to HackerTarget.
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def enumerate_subdomains(target):
    """
    Fetches subdomains using multiple OSINT sources (HackerTarget + crt.sh).
    """
    target = target.replace("http://", "").replace("https://", "").strip()
    subdomains = set()
    subdomains.add(target)
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    # SOURCE 1: HackerTarget (Lightning Fast)
    try:
        url_ht = f"https://api.hackertarget.com/hostsearch/?q={target}"
        resp_ht = requests.get(url_ht, headers=headers, timeout=10)
        
        if resp_ht.status_code == 200:
            lines = resp_ht.text.split('\n')
            for line in lines:
                if ',' in line:
                    sub = line.split(',')[0].strip()
                    if sub.endswith(target):
                        subdomains.add(sub)
    except Exception:
        pass # Ignore errors and move to next source

    # SOURCE 2: crt.sh (Deep but sometimes slow/times out)
    try:
        url_crt = f"https://crt.sh/?q=%.{target}&output=json"
        resp_crt = requests.get(url_crt, headers=headers, timeout=10)
        
        if resp_crt.status_code == 200:
            data = resp_crt.json()
            for entry in data:
                name_value = entry.get("name_value", "")
                domains = name_value.split("\n") if "\n" in name_value else [name_value]
                for d in domains:
                    clean_domain = d.strip().replace("*.", "")
                    if clean_domain.endswith(target):
                        subdomains.add(clean_domain)
    except Exception:
        pass # Ignore timeout and return whatever we found so far

    return sorted(list(subdomains))