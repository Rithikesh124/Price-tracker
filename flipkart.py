import requests
from bs4 import BeautifulSoup

def get_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        # allow_redirects=True is default in requests, but explicit for clarity
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        
        if response.status_code != 200:
            return {"error": f"Failed to fetch page. Status code: {response.status_code}"}

        soup = BeautifulSoup(response.content, "html.parser")

        # Selectors for 2025 Flipkart layout
        title = soup.find("span", {"class": "B_NuCI"}) or soup.find("h1")
        price = soup.find("div", {"class": "_30jeq3 _16Jk6d"}) or soup.find("div", {"class": "Nx9W0j"})
        image = soup.find("img", {"class": "_396cs4 _2amPTt _3qGedV"}) or soup.find("img", {"class": "DByo9Z"})
        rating = soup.find("div", {"class": "_3LWZlK"})

        return {
            "title": title.get_text().strip() if title else "N/A",
            "price": price.get_text().strip() if price else "N/A",
            "image": image['src'] if image else None,
            "rating": rating.get_text().strip() if rating else "No rating",
            "url": response.url
        }
    except Exception as e:
        return {"error": str(e)}
