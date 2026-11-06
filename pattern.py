#!/usr/bin/env python3

"""
Pattern Generator & Offset Finder
Python version: 3.13.5
Tested on: Debian GNU/Linux (Kernel 6.12.113 x86_64)
"""

import sys
from string import ascii_uppercase, ascii_lowercase, digits

MAX_PATTERN_SIZE = 20276

def generate_pattern(pattern_size):
    if pattern_size > MAX_PATTERN_SIZE:
        print(f"[-] Error: Maximum pattern size is {MAX_PATTERN_SIZE}")
        sys.exit(1)

    pattern = ""
    for uppercase in ascii_uppercase:
        for lowercase in ascii_lowercase:
            for digit in digits:
                pattern += uppercase + lowercase + digit
                if len(pattern) >= pattern_size:
                    return pattern[:pattern_size]
    return pattern

def find_offset(crash_address):
    if crash_address.startswith("0x"):
        crash_address = crash_address[2:]

    if len(crash_address) % 2 != 0:
        crash_address = "0" + crash_address

    try:
        raw_bytes = bytes.fromhex(crash_address)[::-1]
        pattern_bytes = generate_pattern(MAX_PATTERN_SIZE).encode('utf-8')
        exact_offset = pattern_bytes.find(raw_bytes)

        if exact_offset > -1:
            return exact_offset
        else:
            print(f"[-] Error: Could not find 0x{crash_address} anywhere in the pattern.")
            sys.exit(1)

    except ValueError:
        print("[-] Error: Invalid hexadecimal address provided.")
        sys.exit(1)

def help_menu():
    print(f"[*] Usage: python3 {sys.argv[0]} <pattern_size> OR <crash_address>")

def main():
    if len(sys.argv) != 2 or sys.argv[1] == "--help":
        help_menu()
        sys.exit(0)

    user_input = sys.argv[1]

    if user_input.isdigit():
        pattern_size = int(user_input)
        generated_buffer = generate_pattern(pattern_size)
        print(f"[+] Generated pattern (Size: {pattern_size} bytes):")
        print(generated_buffer)

    elif user_input.startswith("0x") or all(c in "0123456789abcdefABCDEF" for c in user_input):
        exact_offset = find_offset(user_input)
        print("[+] Exact match found!")
        print(f"[+] Required buffer offset: {exact_offset} bytes")

    else:
        print("[!] Warning: Invalid input. Try --help")

if __name__ == "__main__":
    main()
