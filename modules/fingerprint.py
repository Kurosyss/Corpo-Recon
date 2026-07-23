"""
CORPO-RECON :: WAF & Tech Stack Fingerprinting Module
Identifies backend technology and Web Application Firewalls from HTTP headers.
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WAF_SIGNATURES = {
    'cloudflare': 'Cloudflare',
    'akamaighost': 'Akamai',
    'sucuri': 'Sucuri',
    'incapsula': 'Imperva',
    'awselb': 'AWS WAF',
    'f5': 'F5 BIG-IP',
    'barracuda': 'Barracuda',
}

def detect_tech(url: str) -> dict:
    """
    Makes a fast HTTP request to fingerprint the server tech and WAF.
    
    Returns:
        {"tech": "Nginx/1.18", "waf": "Cloudflare" | "-"}
    """
    result = {"tech": "Unknown", "waf": "-"}
    
    try:
        # Use a quick GET request with a short timeout.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=3.0, verify=False, allow_redirects=False)
        
        # 1. Detect Technology (Server, X-Powered-By)
        tech_parts = []
        if 'Server' in resp.headers:
            tech_parts.append(resp.headers['Server'])
        if 'X-Powered-By' in resp.headers:
            tech_parts.append(resp.headers['X-Powered-By'])
            
        if tech_parts:
            # Join and truncate if it's too long
            joined_tech = " / ".join(tech_parts)
            result["tech"] = joined_tech[:30] + "..." if len(joined_tech) > 30 else joined_tech
            
        # 2. Detect WAF
        headers_str = str(resp.headers).lower()
        for sig, waf_name in WAF_SIGNATURES.items():
            if sig in headers_str:
                result["waf"] = waf_name
                break
                
        # Some WAFs use specific cookies (e.g. __cfduid for older cloudflare, BIGipServer for F5)
        cookies_str = str(resp.cookies).lower()
        if 'waf' not in result or result['waf'] == "-":
            if 'cf_clearance' in cookies_str or '__cf' in cookies_str:
                result["waf"] = "Cloudflare"
            elif 'bigipserver' in cookies_str:
                result["waf"] = "F5 BIG-IP"
            elif 'sucuri_cloudproxy_uuid' in cookies_str:
                result["waf"] = "Sucuri"

    except requests.RequestException:
        pass  # If request fails, return default Unknown/-
        
    return result
