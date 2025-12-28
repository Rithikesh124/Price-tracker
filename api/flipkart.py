import requests
from bs4 import BeautifulSoup

def get_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    try:
        # PURE REDIRECT HANDLING: 
        # We use a session and allow_redirects=True to handle fkrt.it and affiliate links
        session = requests.Session()
        response = session.get(url, headers=headers, allow_redirects=True, timeout=15)
        
        if response.status_code != 200:
            return {"error": f"Flipkart returned status {response.status_code}"}

        soup = BeautifulSoup(response.content, "html.parser")

        # 2025 Selectors
        title_element = soup.find("span", {"class": "B_NuCI"}) or soup.find("h1")
        price_element = soup.find("div", {"class": "Nx9W0j"}) or soup.find("div", {"class": "_30jeq3 _16Jk6d"})
        img_element = soup.find("img", {"class": "DByo9Z"}) or soup.find("img", {"class": "_396cs4"})
        rating_element = soup.find("div", {"class": "_3LWZlK"})

        return {
            "title": title_element.get_text().strip() if title_element else "Product Title Not Found",
            "price": price_element.get_text().strip() if price_element else "Price Not Available",
            "image": img_element['src'] if img_element else None,
            "rating": rating_element.get_text().strip() if rating_element else "N/A",
            "url": response.url
        }
    except Exception as e:
        return {"error": str(e)}
