import os
import requests
import urllib3
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

# Suppress SSL warnings for cleaner terminal output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# The default internal wordlist (Fallback if wordlist.txt is missing)
DEFAULT_WORDLIST = [
    "robots.txt", "sitemap.xml", ".env", "admin", "config",
    "backup.zip", "login.php", "api", "dashboard", ".git/config"
]

def load_wordlist(file_path="wordlist.txt"):
    """Loads custom wordlist if exists, otherwise uses default."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            # Read lines, strip whitespace, and ignore empty lines
            return [line.strip() for line in f if line.strip()]
    return DEFAULT_WORDLIST

def get_random_string(length=12):
    """Generates a random string to test for Catch-All traps."""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def calibrate_target(target_url, headers):
    """
    Pings a random non-existent path to see if the server lies (returns 200 OK).
    Returns the length of the fake response page to use as a baseline.
    """
    dummy_path = get_random_string()
    test_url = f"{target_url}/{dummy_path}"
    
    try:
        resp = requests.get(test_url, headers=headers, timeout=5, verify=False)
        if resp.status_code == 200:
            # The server is lying! It's a catch-all. Record the page size.
            return len(resp.content)
    except Exception:
        pass
    
    # Server is acting normally (probably returned a 404 for a fake path)
    return None

def check_path(url, path, headers, baseline_length):
    """Checks a single path against the target with Trap Buster logic."""
    # Ensure smooth URL concatenation
    target_url = f"{url}/{path.lstrip('/')}"
    try:
        # allow_redirects=False lets us see 301/302 codes accurately
        resp = requests.get(target_url, headers=headers, timeout=5, verify=False, allow_redirects=False)
        
        status = resp.status_code
        # We care about interesting statuses (200 OK, 301/302 Redirects, 403 Forbidden)
        if status in [200, 204, 301, 302, 403, 500]:
            
            # THE TRAP BUSTER LOGIC:
            if status == 200 and baseline_length is not None:
                current_length = len(resp.content)
                # If the current page size is very close to the fake page, it's junk.
                if abs(current_length - baseline_length) < 50: 
                    return None
                    
            return (url, f"/{path.lstrip('/')}", status)
    except Exception:
        pass
    return None

def run_fuzzer(live_urls):
    """
    Main function to run the smart fuzzer across all live hosts.
    Imported by main.py
    """
    results = []
    # Added a custom User-Agent signature for your framework
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Corpo-Recon/1.0"}
    wordlist = load_wordlist()
    
    for url in live_urls:
        # Step 1: Calibrate the target (Find the trap)
        baseline_length = calibrate_target(url, headers)
        
        # Step 2: Multi-threaded attack on the target
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_path = {
                executor.submit(check_path, url, path, headers, baseline_length): path 
                for path in wordlist
            }
            
            for future in as_completed(future_to_path):
                result = future.result()
                if result:
                    results.append(result)
                    
    return results