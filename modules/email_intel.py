"""
CORPO-RECON :: Email Intelligence Module
Validates email infrastructure security (MX, SPF, DMARC).
"""

import dns.resolver
import dns.exception

def run_email_intel(domain: str) -> dict:
    """
    Checks MX records and validates SPF and DMARC policies.
    """
    result = {
        "mx_records": [],
        "spf_record": None,
        "dmarc_record": None,
        "secure": False,
        "issues": []
    }

    try:
        # Check MX Records
        try:
            mx_answers = dns.resolver.resolve(domain, 'MX')
            for rdata in mx_answers:
                result["mx_records"].append(rdata.exchange.to_text().strip('.'))
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            result["issues"].append("No MX records found.")

        # Check SPF Record
        try:
            txt_answers = dns.resolver.resolve(domain, 'TXT')
            for rdata in txt_answers:
                txt = rdata.to_text().strip('"')
                if txt.startswith("v=spf1"):
                    result["spf_record"] = txt
                    break
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            pass

        if not result["spf_record"]:
            result["issues"].append("Missing SPF record (v=spf1). Email spoofing highly likely.")
        elif "~all" in result["spf_record"]:
            result["issues"].append("SPF is configured as SoftFail (~all). Spoofing possible.")
        elif "+all" in result["spf_record"]:
            result["issues"].append("SPF is configured to allow ALL (+all). Critical spoofing risk.")

        # Check DMARC Record
        dmarc_domain = f"_dmarc.{domain}"
        try:
            dmarc_answers = dns.resolver.resolve(dmarc_domain, 'TXT')
            for rdata in dmarc_answers:
                txt = rdata.to_text().strip('"')
                if txt.startswith("v=DMARC1"):
                    result["dmarc_record"] = txt
                    break
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            pass

        if not result["dmarc_record"]:
            result["issues"].append("Missing DMARC record. Domain is vulnerable to impersonation.")
        elif "p=none" in result["dmarc_record"]:
            result["issues"].append("DMARC policy is 'none'. Spoofed emails will still be delivered.")

        # Security Status
        if result["spf_record"] and result["dmarc_record"] and "-all" in result["spf_record"] and ("p=reject" in result["dmarc_record"] or "p=quarantine" in result["dmarc_record"]):
            result["secure"] = True

    except Exception as e:
        result["issues"].append(f"DNS Resolution Error: {str(e)}")

    return result
