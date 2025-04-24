import qrcode

def generate_qr_for_link(url, filename="qr_code.png"):
    # Create a QR code from the given URL
    qr = qrcode.make(url)

    # Save and show the QR image
    qr.save(filename)
    qr.show()

    print(f" QR code created and saved as: {filename}")
    print(f" It will open: {url}")

def main():
    # 👇 Change this to any link you want
    link = "https://pointerpointer.com"
    
    generate_qr_for_link(link)

if __name__ == "__main__":
    main()
