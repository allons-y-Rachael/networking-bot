"""
Run this script to generate a batch of access codes for a new event.
Usage: python generate_codes.py

Paste the output into your secrets.toml and your Stripe confirmation email template.
"""

import secrets
import string


def generate_codes(n=100, prefix="DATATECH"):
    chars = string.ascii_uppercase + string.digits
    codes = set()
    while len(codes) < n:
        code = f"{prefix}-{''.join(secrets.choice(chars) for _ in range(8))}"
        codes.add(code)
    return sorted(codes)


if __name__ == "__main__":
    codes = generate_codes(100)
    print("── Paste into secrets.toml ──────────────────────────────────────")
    print(f'ACCESS_CODES = {codes}')
    print()
    print("── Individual codes (for Stripe email template) ─────────────────")
    for code in codes:
        print(code)
