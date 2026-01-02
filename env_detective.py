#!/usr/bin/env python3
"""ENV Variable Detective - Because your config is a crime scene."""

import os
import sys
import re
from pathlib import Path

def find_env_files():
    """Search for .env files - like finding breadcrumbs in a hurricane."""
    env_files = []
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.env') or file.endswith('.env.example'):
                env_files.append(Path(root) / file)
    return env_files

def extract_vars_from_file(filepath):
    """Parse env file - ignoring comments and empty lines (mostly)."""
    vars_set = set()
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Match VAR=value patterns
                    match = re.match(r'^([A-Z_][A-Z0-9_]*)=', line)
                    if match:
                        vars_set.add(match.group(1))
    except Exception as e:
        print(f"  Failed to read {filepath}: {e}")
    return vars_set

def check_os_env(vars_set):
    """Check which vars are actually set in OS - the moment of truth."""
    missing = []
    present = []
    for var in sorted(vars_set):
        if var in os.environ:
            present.append(var)
        else:
            missing.append(var)
    return present, missing

def main():
    print("🔍 ENV Variable Detective on the case!\n")
    
    # Find all the evidence
    env_files = find_env_files()
    if not env_files:
        print("No .env files found. Case closed - or is it?")
        return
    
    print(f"Found {len(env_files)} suspect files:")
    all_vars = set()
    for filepath in env_files:
        file_vars = extract_vars_from_file(filepath)
        all_vars.update(file_vars)
        print(f"  {filepath}: {len(file_vars)} variables")
    
    print(f"\nTotal unique variables in configs: {len(all_vars)}")
    
    # The big reveal
    present, missing = check_os_env(all_vars)
    
    print(f"\n✅ Present in environment: {len(present)}")
    for var in present[:5]:  # Show first 5
        print(f"  {var}")
    if len(present) > 5:
        print(f"  ... and {len(present) - 5} more")
    
    print(f"\n❌ Missing from environment: {len(missing)}")
    for var in missing:
        print(f"  {var}")
    
    if missing:
        print(f"\n🚨 Case status: UNSOLVED - {len(missing)} variables missing!")
        return 1
    else:
        print(f"\n🎉 Case status: SOLVED - All variables accounted for!")
        return 0

if __name__ == '__main__':
    sys.exit(main())