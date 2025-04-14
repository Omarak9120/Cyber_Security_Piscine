import sys # to access command-line arguments (sys.argv)
import os
import hmac # for secure hashing using a key
import hashlib # provides hashing algorithms like SHA1
import time # to get the current time
import base64

# g stores a key securely

# -k reads the key and generates a 6-digit TOTP code based on the current time



def save_key(key_path):
    try:
        with open(key_path, 'r') as f:
            key = f.read().strip()

        key = key.strip()
        if len(key) != 64 or not all(c in "0123456789abcdefABCDEF" for c in key):
           print("Error: key must be 64 hexadecimal characters.")
           return

        # Validate hex
        int(key, 16)

        with open("ft_otp.key", "w") as out:
            out.write(key)
        print("Key was successfully saved in ft_otp.key.")

    except Exception as e:
        print(f"Error: {e}")
        
def generate_otp(path):
    try:
        with open(path, 'r') as f:
            key_hex = f.read().strip()
        
        if len(key_hex) != 64:
            print("Error: key must be 64 hexadecimal characters.")
            return

        key_bytes = bytes.fromhex(key_hex) # Convert hex string to bytes
        timestep = int(time.time()) // 30 # TOTP uses 30-second intervals
        # Convert the current time to a 64-bit or 8-byte integer
        timestep_bytes = timestep.to_bytes(8, 'big') # Big-endian byte order

        hmac_hash = hmac.new(key_bytes, timestep_bytes, hashlib.sha1).digest() # HMAC-SHA1 hash
        # Extract the last nibble (4 bits) of the last byte to determine the offset
        offset = hmac_hash[-1] & 0x0F # Last 4 bits of the last byte  # binary: 10011111
        # Extract 4 bytes from the hash using the offset

        # Dynamic Truncation
        code = (
            ((hmac_hash[offset] & 0x7F) << 24) |
            ((hmac_hash[offset + 1] & 0xFF) << 16) |
            ((hmac_hash[offset + 2] & 0xFF) << 8) |
            (hmac_hash[offset + 3] & 0xFF)
        )

        otp = code % 10**6
        print(f"{otp:06d}")  # Always 6-digit format

    except Exception as e:
        print(f"Error: {e}")


def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("  ./ft_otp -g key.hex    # generate and save encrypted key")
        print("  ./ft_otp -k ft_otp.key # generate a 6-digit TOTP")
        return

    option, path = sys.argv[1], sys.argv[2]

    if option == "-g":
        save_key(path)
    elif option == "-k":
        generate_otp(path)
    else:
        print("Unknown option. Use -g or -k.")

if __name__ == "__main__":
    main()
