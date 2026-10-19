#!/usr/bin/env python3
"""
Offline practice driver for the Stripe-style OA repo.

  python practice.py                 # list all problems
  python practice.py p4              # start a timed 60-min session on problem 4
  python practice.py p4 --minutes 45 # custom time budget
  python practice.py p4 --test       # just run problem 4's tests, no timer

A "session" prints the problem, runs its tests once (so you see the stubs fail),
then shows a live countdown. Press Ctrl-C when you're done (or let the timer expire)
and it re-runs the tests and prints a pass/fail summary. Everything is stdlib-only
and works with no network.
"""
import argparse
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
PROBLEMS_DIR = os.path.join(ROOT, "problems")

TITLES = {
    "p1_card_range": "Card Range Registry",
    "p2_subscription": "Subscription Billing Engine",
    "p3_fraud": "Streaming Transaction Fraud Detection",
    "p4_load_balancer": "Multi-Stage Load Balancer (OOD)",
    "p5_name_registry": "Company Name Registry",
    "p6_store_closing": "Store Closing Time",
    "p7_card_validation": "Payment Card Validation",
    "p8_chat_billing": "Chat Token Billing",
    "p9_request_routing": "Request Routing System",
}


def discover():
    if not os.path.isdir(PROBLEMS_DIR):
        return []
    return sorted(d for d in os.listdir(PROBLEMS_DIR)
                  if os.path.isdir(os.path.join(PROBLEMS_DIR, d)) and d.startswith("p"))


def resolve(token, folders):
    token = token.lower()
    hits = [f for f in folders if f == token or f.startswith(token) or f.split("_", 1)[0] == token]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        print(f"No problem matches '{token}'. Known: {', '.join(folders)}")
    else:
        print(f"'{token}' is ambiguous: {', '.join(hits)}")
    return None


def spec_for(folder):
    num = folder.split("_", 1)[0][1:]  # p4_x -> 4
    for f in os.listdir(ROOT):
        if f.startswith(f"0{num}_") and f.endswith(".md"):
            return f
    return None


def list_problems(folders):
    print("\nAvailable problems:\n")
    for f in folders:
        print(f"  {f.split('_',1)[0]:>3}  {TITLES.get(f, f):<40}  ({f})")
    print("\nStart one with, e.g.:  python practice.py p4\n")


def run_tests(folder):
    path = os.path.join("problems", folder)
    return subprocess.call([sys.executable, "-m", "pytest", path, "-q"], cwd=ROOT)


def countdown(minutes):
    total = int(minutes * 60)
    try:
        for left in range(total, -1, -1):
            m, s = divmod(left, 60)
            sys.stdout.write(f"\r  time left: {m:02d}:{s:02d}   (Ctrl-C when done) ")
            sys.stdout.flush()
            time.sleep(1)
        print("\n\n  ⏰ time's up!\n")
    except KeyboardInterrupt:
        print("\n\n  stopped early — grading your work.\n")


def start(folder, minutes):
    title = TITLES.get(folder, folder)
    spec = spec_for(folder)
    print("=" * 70)
    print(f"  Problem: {title}")
    if spec:
        print(f"  Spec:     {spec}   (read all parts before writing code)")
    print(f"  Code:     problems/{folder}/solution_{folder.split('_',1)[0]}.py")
    print(f"  Budget:   {minutes} minutes")
    print("=" * 70)
    print("\n  Baseline (stubs should fail):\n")
    run_tests(folder)
    print()
    countdown(minutes)
    print("  Final result:\n")
    rc = run_tests(folder)
    print("\n  " + ("✅ all green — nice." if rc == 0 else "❌ not all passing yet."))


def main():
    ap = argparse.ArgumentParser(description="Timed offline practice for the Stripe-style OA repo.")
    ap.add_argument("problem", nargs="?", help="problem token, e.g. p4 or p4_load_balancer")
    ap.add_argument("--minutes", type=float, default=60, help="time budget (default 60)")
    ap.add_argument("--test", action="store_true", help="just run the tests, no timer")
    args = ap.parse_args()

    folders = discover()
    if not folders:
        print("No problems found. Run this from the repo root.")
        return
    if not args.problem:
        list_problems(folders)
        return
    folder = resolve(args.problem, folders)
    if not folder:
        return
    if args.test:
        sys.exit(run_tests(folder))
    start(folder, args.minutes)


if __name__ == "__main__":
    main()
