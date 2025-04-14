import os                    # File operations: paths, folders
import argparse              # Command-line arguments parser
import requests              # To fetch HTML pages and images
from bs4 import BeautifulSoup  # HTML parsing
from urllib.parse import urljoin, urlparse  # URL handling

SUPPORTED_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def download_image(img_url, save_dir):
    try:
        response = requests.get(img_url, timeout=5)
        response.raise_for_status()
        filename = os.path.basename(urlparse(img_url).path) # Return the tail (basename) part of a path, same as split(path)[1]
        """Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>

    The result is a named 6-tuple with fields corresponding to the
    above. It is either a ParseResult or ParseResultBytes object,
    depending on the type of the url parameter.

    The username, password, hostname, and port sub-components of netloc
    can also be accessed as attributes of the returned object.

    The scheme argument provides the default value of the scheme
    component when no scheme is found in url.

    If allow_fragments is False, no attempt is made to separate the
    fragment component from the previous component, which can be either
    path or query.

    Note that % escapes are not expanded.
    """
        if not filename:
            return False
        os.makedirs(save_dir, exist_ok=True)
        """makedirs(name [, mode=0o777][, exist_ok=False])

    makedirs; create a leaf directory and all intermediate ones.  Works like
    mkdir, except that any intermediate path segment (not just the rightmost)
    will be created if it does not exist. If the target directory already
    exists, raise an OSError if exist_ok is False. Otherwise no exception is
    raised.  This is recursive.

    """
        with open(os.path.join(save_dir, filename), 'wb') as f:
            f.write(response.content)
        print(f"[+] Downloaded: {img_url}")
        return True
    except Exception as e:
        print(f"[!] Failed to download {img_url}: {e}")
        return False

#     url,           # the current page to scrape
#     save_dir,      # where to save the images locally
#     visited,       # a set to track visited URLs (avoid loops)
#     depth,         # current recursion level
#     max_depth,     # maximum depth allowed
#     max_images,    # maximum number of images to download
#     image_counter  # a mutable counter (list) to track how many images have been downloaded

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
    '''<html>
  <head><title>Example</title></head>
  <body>
    <img src="image.jpg">
    <a href="next-page.html">Next</a>
  </body>
</html>'''
    # Download image tags
    for img_tag in soup.find_all('img'):
        if max_images is not None and image_counter[0] >= max_images:
            return
        img_src = img_tag.get('src') # <img src="media/image1.jpg">
        if not img_src:
            continue
        full_url = urljoin(url, img_src) # base = http://omar.com/page.html, src="images/img1.jpg" → result = http://omar.com/images/img1.jpg
        if full_url.lower().endswith(SUPPORTED_EXT):
            if download_image(full_url, save_dir):
                image_counter[0] += 1

    # Follow links
    for link_tag in soup.find_all('a'): # This goes through every <a> (link) tag on the page
        if max_images is not None and image_counter[0] >= max_images:
            return
        href = link_tag.get('href') 
        if href:
            next_url = urljoin(url, href) # base = http://omar.com/page.html, href="next-page.html" → result = http://omar.com/next-page.html
            # Check if the next URL is within the same domain
            if urlparse(next_url).netloc == urlparse(url).netloc: # Avoids going to external sites
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
