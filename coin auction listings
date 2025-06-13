import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("Sold Coin Listings Scraper")

# User input for search term
search_term = st.text_input("Enter coin search term", "Morgan Dollar")

# Build eBay sold listings URL
def build_ebay_url(search_term):
    base_url = "https://www.ebay.com/sch/i.html"
    params = {
        "_nkw": search_term,
        "_sacat": "11116",  # Coins & Paper Money category
        "LH_Sold": "1",
        "LH_Complete": "1"
    }
    query = "&".join([f"{k}={v.replace(' ', '+') if isinstance(v, str) else v}" for k, v in params.items()])
    return f"{base_url}?{query}"

if st.button("Scrape Sold Listings"):
    url = build_ebay_url(search_term)
    st.write(f"Scraping: {url}")

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    items = soup.find_all("li", class_="s-item")
    results = []
    for item in items:
        title_tag = item.find("h3", class_="s-item__title")
        price_tag = item.find("span", class_="s-item__price")
        link_tag = item.find("a", class_="s-item__link")
        date_tag = item.find("span", class_="s-item__endedDate")
        if title_tag and price_tag and link_tag:
            title = title_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            link = link_tag["href"]
            date = date_tag.get_text(strip=True) if date_tag else ""
            results.append({"Title": title, "Price": price, "Date": date, "URL": link})

    if results:
        df = pd.DataFrame(results)
        st.dataframe(df)
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "sold_coins.csv", "text/csv")
    else:
        st.warning("No sold listings found. Try another search term.")

st.markdown("""
---
**How it works:**  
- Enter a coin search term (e.g., "Morgan Dollar")  
- Click "Scrape Sold Listings"  
- View results and download as CSV

**Note:** This demo scrapes eBay. For other auction sites, the scraping logic must be adapted to their HTML structure.
""")
