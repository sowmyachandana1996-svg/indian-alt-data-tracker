# Indian Consumer Internet Alternative Data Tracker
# Run daily to track Swiggy, Zomato, Blinkit, Flipkart pricing & ratings

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random

# Example targets (easily expandable)
targets = {
    "Swiggy - Domino's Pizza (Bengaluru)": "https://www.swiggy.com/restaurants/dominos-pizza-indiranagar-bengaluru-2600",
    "Zomato - Behrouz Biryani (Delhi)": "https://www.zomato.com/ncr/behrouz-biryani-rajouri-garden-new-delhi",
    "Blinkit - Amul Milk 1L": "https://blinkit.com/prn/amul-gold-homogenised-standardised-milk-1-l/prid/75438",
    "Flipkart - iPhone 16 128GB": "https://www.flipkart.com/apple-iphone-16-black-128-gb/p/itm8b5b2f0f3a9b3"
}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def scrape_item(url):
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        price_tags = soup.find_all(string=lambda text: "₹" in str(text) or "Rs" in str(text))
        rating_tags = soup.find_all(string=lambda text: "." in str(text) and text.replace('.','').isdigit())
        
        price = next((p for p in price_tags if len(p) < 20), "N/A")
        rating = next((r for r in rating_tags if 1 <= float(r) <= 5), "N/A")
        
        return str(price), str(rating)
    except:
        return "Error", "Error"

# Main scrape
results = []
print("Starting daily alternative data scrape...\n")

for name, url in targets.items():
    print(f"Scraping: {name}")
    price, rating = scrape_item(url)
    results.append({
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Item": name,
        "Price": price,
        "Rating": rating,
        "Anomaly_Flag": "YES" if price != "N/A" and "₹" in price and int(''.join(filter(str.isdigit, price))) > 800 else "No",
        "URL": url
    })
    time.sleep(random.uniform(2, 5))

# Save results
df = pd.DataFrame(results)
filename = f"indian_alt_data_{datetime.now().strftime('%Y%m%d')}.csv"
df.to_csv(filename, index=False)

print(f"\nScrape complete! Saved to {filename}")
print(df[["Item", "Price", "Rating", "Anomaly_Flag"]])
