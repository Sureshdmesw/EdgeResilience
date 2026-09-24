# -*- coding: utf-8 -*-
"""
EdgeResilience — Automated Judge Test
Validates that the dashboard Command Center answers 8 semantic questions.

Run: python src/dashboard/judge_test.py
Requires: server running on http://127.0.0.1:8765
"""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
URL = "http://127.0.0.1:8765"

def fetch(url):
    """Fetch URL content as string."""
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.read().decode("utf-8")
    except Exception as e:
        print(f"ERROR: Cannot reach {url}: {e}")
        print("Make sure the dashboard is running: python src/dashboard/server.py")
        sys.exit(1)


def main():
    html = fetch(URL)
    evidence = json.loads(fetch(URL + "/api/evidence"))

    # Get cycle-003 (last cycle) risk level from evidence
    last_cycle = evidence["cycles"][-1]
    risk_level = last_cycle["risk"]["predictive_risk_level"]  # MEDIUM

    print("=" * 60)
    print("JUDGE TEST — 8 Semantic Questions")
    print("=" * 60)

    checks = [
        # 1. What is EdgeResilience?
        (
            "Product identity visible?",
            "EdgeResilience" in html
            and "Snapdragon-Powered" in html
            and "Connected Vehicle Safety" in html,
        ),
        # 2. What does the AI predict?
        (
            "AI prediction target visible?",
            "future_degradation" in html
            and "Temporal Predictor" in html,
        ),
        # 3. What is the current predictive risk?
        #    The Command Center must show the semantic label "Predictive Risk"
        #    AND the actual risk level from the evidence data (e.g. MEDIUM).
        (
            "Risk visible?",
            "Predictive Risk" in html
            and risk_level in html,
        ),
        # 4. What happens during connectivity loss?
        (
            "Connectivity resilience visible?",
            "LOCAL" in html
            and ("ALWAYS ACTIVE" in html or "always active" in html)
            and "BUFFERING" in html.upper(),
        ),
        # 5. Does local intelligence continue?
        (
            "Local inference visible?",
            "Local" in html
            and ("ALWAYS ACTIVE" in html or "always active" in html)
            and "inference" in html.lower(),
        ),
        # 6. Is evidence preserved?
        (
            "Evidence preservation visible?",
            "SHA-256" in html
            and "Evidence" in html
            and "evidence" in html.lower(),
        ),
        # 7. What is actually verified?
        (
            "Verification status visible?",
            "VERIFIED" in html
            and "NOT VERIFIED" in html,
        ),
        # 8. Is Snapdragon hardware verified?
        (
            "Snapdragon honesty visible?",
            "Snapdragon" in html
            and "NOT VERIFIED" in html,
        ),
    ]

    fails = 0
    for name, ok in checks:
        status = "PASS" if ok else "FAIL"
        print(f"  {status}  {name}")
        if not ok:
            fails += 1

    print()
    print("=" * 60)
    result = "ALL_PASS" if fails == 0 else f"{fails}_FAILURES"
    print(f"JUDGE_TEST: {result}")
    print("=" * 60)

    return fails == 0


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
