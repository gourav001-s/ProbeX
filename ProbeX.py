#!/usr/bin/env python3

import asyncio
import aiohttp
import argparse
import random
import time
import json
from datetime import datetime
from playwright.async_api import async_playwright

# ======================================================
# BANNER
# ======================================================

BANNER = r"""
██████╗ ██████╗  ██████╗ ██████╗ ███████╗██╗  ██╗
██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝╚██╗██╔╝
██████╔╝██████╔╝██║   ██║██████╔╝█████╗   ╚███╔╝ 
██╔═══╝ ██╔══██╗██║   ██║██╔══██╗██╔══╝   ██╔██╗ 
██║     ██║  ██║╚██████╔╝██████╔╝███████╗██╔╝ ██╗
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝

        ProbeX – Hybrid OSINT Framework
              Developed by RavX
====================================================
"""

# ======================================================
# CONFIG
# ======================================================

CONCURRENCY_LIMIT = 5
MIN_RESPONSE_LENGTH = 500
MAX_RETRIES = 2

REQUEST_COUNT = 0

PLATFORMS = [
    {"name": "Instagram", "url": "https://www.instagram.com/{}", "invalid": ["Sorry, this page isn't available"]},
    {"name": "Facebook", "url": "https://www.facebook.com/{}", "invalid": ["This content isn't available"]},
    {"name": "GitHub", "url": "https://github.com/{}", "invalid": ["Not Found"]},
    {"name": "Reddit", "url": "https://www.reddit.com/user/{}", "invalid": ["Sorry, nobody on Reddit goes by that name"]},
    {"name": "TikTok", "url": "https://www.tiktok.com/@{}", "invalid": ["Couldn't find this account"]},
    {"name": "Steam", "url": "https://steamcommunity.com/id/{}", "invalid": ["The specified profile could not be found"]},
]

# ======================================================
# PERMUTATION ENGINE
# ======================================================

def generate_permutations(username):
    base = username.lower()
    return list({
        base,
        base + "123",
        base + "01",
        base + "_official",
        base.replace(".", "_"),
        base.replace("_", "."),
        base + "x"
    })

# ======================================================
# CONFIDENCE ENGINE
# ======================================================

def confidence_score(count):
    if count >= 5:
        return "Very High"
    if count >= 3:
        return "High"
    if count >= 2:
        return "Medium"
    if count == 1:
        return "Low"
    return "None"

# ======================================================
# HTTP CHECK
# ======================================================

async def http_check(session, semaphore, platform, username):
    global REQUEST_COUNT
    url = platform["url"].format(username)

    async with semaphore:
        for _ in range(MAX_RETRIES + 1):
            try:
                REQUEST_COUNT += 1
                async with session.get(url, timeout=10) as resp:
                    text = await resp.text()

                    if resp.status == 200 and len(text) > MIN_RESPONSE_LENGTH:
                        if not any(bad.lower() in text.lower() for bad in platform["invalid"]):
                            return ("confirmed", platform["name"], url)

                    if resp.status in [403, 429]:
                        return ("blocked", platform["name"], url)

                await asyncio.sleep(random.uniform(0.4, 1.2))
            except:
                await asyncio.sleep(random.uniform(0.5, 1.5))

    return ("not_found", platform["name"], url)

# ======================================================
# BROWSER VERIFY
# ======================================================

async def browser_verify(name, url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=15000)
            content = await page.content()
            await browser.close()

            if "login" in content.lower():
                return False

            if len(content) > 1000:
                return True
    except:
        pass

    return False

# ======================================================
# HYBRID SCAN
# ======================================================

async def scan(username):
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    confirmed = []
    fallback = []

    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (X11; Linux x86_64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        ])
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [http_check(session, semaphore, p, username) for p in PLATFORMS]
        results = await asyncio.gather(*tasks)

    for status, name, url in results:
        if status == "confirmed":
            print(f"[HTTP FOUND] {name}: {url}")
            confirmed.append((name, url))
        elif status == "blocked":
            print(f"[HTTP BLOCKED] {name} → Browser verification required")
            fallback.append((name, url))

    for name, url in fallback:
        print(f"[BROWSER VERIFY] {name}")
        if await browser_verify(name, url):
            print(f"[BROWSER FOUND] {name}: {url}")
            confirmed.append((name, url))
        else:
            print(f"[BROWSER FAILED] {name}")

    return confirmed

# ======================================================
# MAIN
# ======================================================

async def main():
    parser = argparse.ArgumentParser(description="ProbeX Hybrid OSINT Framework")
    parser.add_argument("--username", help="Target username")
    parser.add_argument("--permutations", action="store_true")
    parser.add_argument("--report", help="Export report file")

    args = parser.parse_args()

    print(BANNER)

    if not args.username:
        args.username = input("Enter username to scan: ").strip()
        if not args.username:
            print("Username required.")
            return

        perm = input("Enable permutations? (y/n): ").lower()
        args.permutations = perm == "y"

        rep = input("Export report? (y/n): ").lower()
        if rep == "y":
            args.report = input("Enter report filename: ").strip()

    usernames = [args.username]
    if args.permutations:
        usernames = generate_permutations(args.username)

    start_time = time.time()
    results = {}
    total_found = 0

    for uname in usernames:
        print(f"\nScanning: {uname}")
        found = await scan(uname)
        if found:
            results[uname] = found
            total_found += len(found)

    confidence = confidence_score(total_found)
    scan_time = round(time.time() - start_time, 2)

    print("\n====================================================")
    print("Scan Complete")
    print("====================================================")
    print("Accounts Found:", total_found)
    print("Confidence:", confidence)
    print("Requests Made:", REQUEST_COUNT)
    print("Scan Time:", scan_time, "seconds")

    if args.report:
        with open(args.report, "w") as f:
            json.dump({
                "username": args.username,
                "results": results,
                "confidence": confidence,
                "requests": REQUEST_COUNT,
                "scan_time": scan_time,
                "timestamp": str(datetime.now())
            }, f, indent=4)
        print("Report saved.")

if __name__ == "__main__":
    asyncio.run(main())
