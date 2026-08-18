import os
import aiohttp
import asyncio
import random
import string

DEFAULT_WORDLIST = [
    "robots.txt", "sitemap.xml", ".env", "admin", "config",
    "backup.zip", "login.php", "api", "dashboard", ".git/config"
]

def load_wordlist(file_path="wordlist.txt"):
    """Loads custom wordlist if exists, otherwise uses default."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return DEFAULT_WORDLIST

def get_random_string(length=12):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(length))

async def calibrate_target(session, target_url, headers):
    dummy_path = get_random_string()
    test_url = f"{target_url}/{dummy_path}"
    try:
        async with session.get(test_url, headers=headers, timeout=5, ssl=False) as resp:
            if resp.status == 200:
                content = await resp.read()
                return len(content)
    except Exception:
        pass
    return None

async def check_path(session, sem, url, path, headers, baseline_length):
    target_url = f"{url}/{path.lstrip('/')}"
    async with sem:
        try:
            async with session.get(target_url, headers=headers, timeout=5, ssl=False, allow_redirects=False) as resp:
                status = resp.status
                if status in [200, 204, 301, 302, 403, 500]:
                    if status == 200 and baseline_length is not None:
                        content = await resp.read()
                        if abs(len(content) - baseline_length) < 50:
                            return None
                    return {"url": url, "path": path.lstrip('/'), "status": status}
        except Exception:
            pass
    return None

async def _async_run_fuzzer(live_urls):
    results = []
    headers = {"User-Agent": "Mozilla/5.0 Corpo-Recon/1.0"}
    wordlist = load_wordlist()
    
    # Using TCPConnector to disable SSL verification
    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        sem = asyncio.Semaphore(100) # Prevent socket exhaustion
        
        for url in live_urls:
            if isinstance(url, dict):
                url = url.get("url") # Handle if dict is passed
            if not url:
                continue

            baseline_length = await calibrate_target(session, url, headers)
            
            tasks = [check_path(session, sem, url, path, headers, baseline_length) for path in wordlist]
            completed = await asyncio.gather(*tasks)
            
            for res in completed:
                if res:
                    results.append(res)
                    
    return results

def run_fuzzer(live_urls):
    """
    Main synchronous wrapper for the async fuzzer.
    """
    if not live_urls:
        return []
    
    urls = []
    for u in live_urls:
        if isinstance(u, dict):
            urls.append(u.get("url"))
        elif isinstance(u, str):
            urls.append(u)
            
    try:
        return asyncio.run(_async_run_fuzzer(urls))
    except Exception as e:
        return []