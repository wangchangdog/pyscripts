import sys
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore

# coloramaの初期化
init(autoreset=True)

def fetch_robots_txt(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch robots.txt: {response.status_code}")
        return None

def extract_sitemap_urls(robots_txt):
    sitemap_urls = []
    lines = robots_txt.split('\n')
    for line in lines:
        if line.strip().lower().startswith('sitemap:'):
            sitemap_url = line.split(':', 1)[1].strip()
            sitemap_urls.append(sitemap_url)
    return sitemap_urls

def validate_sitemap_url(sitemap_url):
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        print(f"Failed to fetch sitemap.xml: {sitemap_url} - Status code: {response.status_code}")
        return None
    return response.content

def validate_sitemap_content(content):
    try:
        soup = BeautifulSoup(content, 'xml')
        print("Sitemap is well-formed.")
    except Exception as e:
        print(f"Sitemap is not well-formed: {e}")
        return False

    urls = [loc.text for loc in soup.find_all('loc')]
    for url in urls:
        url_response = requests.get(url)
        if url_response.status_code == 200:
            print(Fore.GREEN + f"URL is valid: " + Fore.RESET + f"{url}")
        else:
            print(Fore.RED + f"URL is invalid: " + Fore.RESET + f"{url} - Status code: " + Fore.RED + f"{url_response.status_code}" + Fore.RESET)
    return True

def main(website_url):
    robots_url = f"{website_url}/robots.txt"
    robots_txt = fetch_robots_txt(robots_url)
    if robots_txt:
        sitemap_urls = extract_sitemap_urls(robots_txt)
        for sitemap_url in sitemap_urls:
            print(f"Validating sitemap: {sitemap_url}")
            sitemap_content = validate_sitemap_url(sitemap_url)
            if sitemap_content:
                validate_sitemap_content(sitemap_content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_sitemap.py <website_url>")
        sys.exit(1)
    
    website_url = sys.argv[1]
    main(website_url)