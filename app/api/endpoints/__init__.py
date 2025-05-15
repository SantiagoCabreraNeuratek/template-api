"""
Auto-discovery for API endpoints.
This module automatically imports all Python files in the endpoints directory
and exposes their router objects if available.
"""
import importlib
import os
import pkgutil
from pathlib import Path
from typing import Dict, List

from fastapi import APIRouter

# Dictionary to store all routers by their module name
routers: Dict[str, APIRouter] = {}

# Get the directory of this file
package_dir = Path(__file__).resolve().parent

# For each Python file in the directory
for (_, module_name, _) in pkgutil.iter_modules([str(package_dir)]):
    # Skip the current file
    if module_name == "__init__":
        continue
    
    # Import the module
    module = importlib.import_module(f"{__package__}.{module_name}")
    
    # If the module has a router attribute, add it to our routers dictionary
    if hasattr(module, "router"):
        routers[module_name] = module.router

# Expose all routers
__all__ = ["routers"]
