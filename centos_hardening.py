#!/usr/bin/env python3

import os
import subprocess
import re

def check_firewalld_status():
    print("\n🔍 Checking if firewalld is active (CentOS)...")
    try:
        output = subprocess.check_output(['systemctl', 'is-active', 'firewalld']).decode().strip()
        if output == 'active':
            print("✅ firewalld is active.")
        else:
            print("❌ firewalld is not active.")
    except subprocess.CalledProcessError:
        print("⚠️ firewalld is not active or not installed.")

def check_open_ports():
    print("\n🔍 Checking for open ports using 'ss'...")
    try:
        result = subprocess.check_output(['ss', '-tuln']).decode()
        print("🟢 Open ports found:\n", result)
    except Exception as e:
        print(f"⚠️ Failed to check open ports: {e}")

def check_ssh_root_login():
    print("\n🔍 Checking if root login via SSH is disabled...")
    try:
        with open('/etc/ssh/sshd_config', 'r') as f:
            config = f.read()
        match = re.search(r'^\s*PermitRootLogin\s+(\w+)', config, re.MULTILINE)
        if match and match.group(1).lower() == 'no':
            print("✅ Root login via SSH is disabled.")
        else:
            print("❌ Root login via SSH is enabled or not set. Please set `PermitRootLogin no`.")
    except Exception as e:
        print(f"⚠️ Failed to read SSH config: {e}")

def guest_login_check():
    print("\n🚫 Guest login disabling for CentOS (GDM)...")
    try:
        gdm_config = "/etc/gdm/custom.conf"
        if os.path.exists(gdm_config):
            with open(gdm_config, 'r') as f:
                content = f.read()
            if "AllowGuest=false" in content:
                print("✅ Guest login is already disabled.")
            else:
                with open(gdm_config, 'a') as f:
                    f.write("\n[daemon]\nAllowGuest=false\n")
                print("✅ Guest login disabled in GDM.")
        else:
            print("⚠️ GDM config not found.")
    except Exception as e:
        print(f"⚠️ Failed to configure guest login: {e}")

def show_failed_login_logs():
    print("\n📜 Showing system logs of failed login attempts (SSHD)...")
    try:
        output = subprocess.check_output(['journalctl', '-xe', '_COMM=sshd']).decode()
        failed_lines = [line for line in output.split('\n') if "Failed password" in line]
        if failed_lines:
            print("\n".join(failed_lines))
        else:
            print("✅ No failed SSH login attempts found.")
    except Exception as e:
        print(f"⚠️ Failed to fetch logs: {e}")

if __name__ == "__main__":
    print("🔐 Starting CentOS Hardening Checks...\n")
    check_firewalld_status()
    check_open_ports()
    check_ssh_root_login()
    guest_login_check()
    show_failed_login_logs()
    print("\n✅ Hardening Check Completed on CentOS.\n")

