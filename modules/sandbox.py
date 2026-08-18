"""
CORPO-RECON :: Kernel Sandbox Module
Initializes an isolated environment and checks system integrity.
"""

import os
import platform

def init_sandbox() -> dict:
    """
    Checks environment integrity.
    """
    result = {
        "sandbox_active": True,
        "platform": platform.system(),
        "is_root": False,
        "warnings": []
    }
    
    if platform.system() == "Linux" or platform.system() == "Darwin":
        if os.geteuid() == 0:
            result["is_root"] = True
            result["warnings"].append("Running as root is not recommended for isolated sandbox execution.")
            
    # Mock checks for virtualization/containerization
    if os.path.exists("/.dockerenv"):
        result["environment"] = "Docker Container"
    else:
        result["environment"] = "Host / Virtual Machine"
        
    return result
