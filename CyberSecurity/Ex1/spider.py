import os
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

SUPPORTED_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def download_image(img_url, save_dir):
    try:
        response = requests.get(img_url, timeout=5)
        response.raise_for_status()
        filename = os.path.basename(urlparse(img_url).path)
        if not filename:
            return False
        os.makedirs(save_dir, exist_ok=True)
        with open(os.path.join(save_dir, filename), 'wb') as f:
            f.write(response.content)
        print(f"[+] Downloaded: {img_url}")
        return True
    except Exception as e:
        print(f"[!] Failed to download {img_url}: {e}")
        return False

def extract_images_from_url(url, save_dir, visited, depth, max_depth, max_images, image_counter):
    if url in visited or depth > max_depth:
        return
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except Exception as e:
        print(f"[!] Failed to fetch {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Download image tags
    for img_tag in soup.find_all('img'):
        if max_images is not None and image_counter[0] >= max_images:
            return
        img_src = img_tag.get('src')
        if not img_src:
            continue
        full_url = urljoin(url, img_src)
        if full_url.lower().endswith(SUPPORTED_EXT):
            if download_image(full_url, save_dir):
                image_counter[0] += 1

    # Follow links
    for link_tag in soup.find_all('a'):
        if max_images is not None and image_counter[0] >= max_images:
            return
        href = link_tag.get('href')
        if href:
            next_url = urljoin(url, href)
            if urlparse(next_url).netloc == urlparse(url).netloc:
                extract_images_from_url(next_url, save_dir, visited, depth+1, max_depth, max_images, image_counter)

def main():
    parser = argparse.ArgumentParser(description="Spider: Image Web Scraper")
    parser.add_argument('-r', action='store_true', help="Recursive download")
    parser.add_argument('-l', type=int, default=5, help="Max depth level (default: 5)")
    parser.add_argument('-p', type=str, default='./data/', help="Save path (default: ./data/)")
    parser.add_argument('-n', type=int, default=None, help="Max number of images to download (optional)")
    parser.add_argument('url', type=str, help="URL to scrape")
    args = parser.parse_args()

    visited = set()
    image_counter = [0]  # Mutable counter

    print(f"[*] Starting download from {args.url}")
    extract_images_from_url(args.url, args.p, visited, 0, args.l if args.r else 0, args.n, image_counter)

if __name__ == '__main__':
    main()
