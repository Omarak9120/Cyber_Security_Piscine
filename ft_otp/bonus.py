import sys
import os
import hmac
import hashlib
import time
import base64
import qrcode

def save_key(path):
    with open(path, 'r') as f:
        key = f.read().strip()
    if len(key) != 64 or not all(c in "0123456789abcdefABCDEF" for c in key):
        print("Error: key must be 64 hexadecimal characters.")
        return
    with open("ft_otp.key", "w") as out:
        out.write(key)
    print("Key was successfully saved in ft_otp.key.")

def generate_otp(path):
    with open(path, 'r') as f:
        key_hex = f.read().strip()
    if len(key_hex) != 64:
        print("Error: key must be 64 hexadecimal characters.")
        return

    key_bytes = bytes.fromhex(key_hex)
    timestep = int(time.time()) // 30
    timestep_bytes = timestep.to_bytes(8, 'big')

    hmac_hash = hmac.new(key_bytes, timestep_bytes, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F

    code = (
        ((hmac_hash[offset] & 0x7F) << 24) |
        ((hmac_hash[offset + 1] & 0xFF) << 16) |
        ((hmac_hash[offset + 2] & 0xFF) << 8) |
        (hmac_hash[offset + 3] & 0xFF)
    )
    otp = code % 10**6
    print(f"{otp:06d}")

def generate_qr():
    # Step 1: Generate a base32 seed (Google Auth-compatible)
    raw_key = os.urandom(20)
    base32_key = base64.b32encode(raw_key).decode().replace("=", "") # Remove padding

    # Step 2: Create a standard otpauth URI
    label = "Cyber42:student"
    issuer = "Cyber42"
    uri = f"otpauth://totp/{label}?secret={base32_key}&issuer={issuer}&digits=6&period=30" # 6 digits, 30 seconds

    # Step 3: Create and show QR code
    img = qrcode.make(uri)
    img.save("ft_otp_qr.png")
    img.show()

    print(" QR Code saved as ft_otp_qr.png")
    print(f" Base32 Secret (for Google Authenticator): {base32_key}")
    print(f" URI: {uri}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ft_otp.py -g key.hex      # Save 64-character hex key")
        print("  python ft_otp.py -k ft_otp.key   # Generate 6-digit TOTP")
        print("  python ft_otp.py --qr            # Generate QR code + base32 seed")
        return

    option = sys.argv[1]

    if option == "-g" and len(sys.argv) == 3:
        save_key(sys.argv[2])
    elif option == "-k" and len(sys.argv) == 3:
        generate_otp(sys.argv[2])
    elif option == "--qr":
        generate_qr()
    else:
        print("Invalid option or missing file. Use -g, -k, or --qr.")

if __name__ == "__main__":
    main()
