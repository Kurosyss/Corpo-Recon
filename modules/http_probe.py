import requests
import concurrent.futures
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Stealth Headers to bypass basic WAFs and bot-detections
STEALTH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def check_host(item):
    # Safely extract subdomain string whether it's a dict or string
    if isinstance(item, dict):
        target = item.get("subdomain", item.get("domain", str(item)))
    else:
        target = str(item)
        
    target = target.strip().replace("http://", "").replace("https://", "")
    
    live_list = []
    
    # Check both HTTP and HTTPS
    for schema in ["http://", "https://"]:
        url = f"{schema}{target}"
        try:
            # Tuple timeout: (3.0s connect, 7.0s read) to prevent hangs
            # allow_redirects=True to follow WAF 301/302 redirects naturally
            response = requests.get(
                url, 
                headers=STEALTH_HEADERS, 
                verify=False, 
                timeout=(3.0, 7.0),
                allow_redirects=True
            )
            
            if response.status_code:
                # EXACT DICTIONARY FORMAT REQUIRED BY main.py
                live_list.append({
                    "url": url,
                    "tech": "-",          # Placeholder for UI
                    "waf": "-",           # Placeholder for UI
                    "status": str(response.status_code)
                })
                break  # Stop at first successful connection
                
        except requests.exceptions.RequestException:
            # Silently pass if connection fails
            continue
            
    return live_list

def probe_hosts(subdomains):
    if not subdomains:
        return []
        
    # Ensure subdomains is an iterable list
    if isinstance(subdomains, str):
        subdomains = [subdomains]

    live_hosts = []
    
    # Threading for faster execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_host, subdomains)
        for result in results:
            if result:
                live_hosts.extend(result)
                
    return live_hosts