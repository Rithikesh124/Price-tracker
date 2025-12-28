import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_product_details(url):
    # Standardize the URL (Convert mobile deep links to web links)
    url = url.replace("dl.flipkart.com", "www.flipkart.com")
    
    # Setup a robust session with retries
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
    
    try:
        # Increase timeout to 25 seconds (Vercel hobby limit is usually 30s)
        response = session.get(url, headers=headers, allow_redirects=True, timeout=25)
        
        if response.status_code != 200:
            return {"error": f"Flipkart blocked us (Status: {response.status_code})"}

        soup = BeautifulSoup(response.content, "html.parser")

        # 2025 Layout Selectors
        title = soup.find("span", {"class": "B_NuCI"}) or soup.find("h1")
        # Try multiple price tags as Flipkart rotates classes
        price = soup.find("div", {"class": "Nx9W0j"}) or soup.find("div", {"class": "_30jeq3 _16Jk6d"})
        image = soup.find("img", {"class": "DByo9Z"}) or soup.find("img", {"class": "_396cs4"})
        rating = soup.find("div", {"class": "_3LWZlK"})

        return {
            "title": title.get_text().strip() if title else "Title not found",
            "price": price.get_text().strip() if price else "Price hidden",
            "image": image['src'] if image else None,
            "rating": rating.get_text().strip() if rating else "N/A",
            "url": response.url
        }
    except requests.exceptions.Timeout:
        return {"error": "Flipkart took too long to respond. Try again."}
    except Exception as e:
        return {"error": f"Connection Error: {str(e)}"}
