import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="Coin Search Tool", layout="wide")
st.title("🪙 Coin Search Across Auction Sites")

# --- Helper Functions ---
HEADERS = {"User-Agent": "Mozilla/5.0"}

def search_ebay(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    return [item.text.strip() for item in soup.select(".s-item__title")[:5] if item.text.strip()]

def search_heritage(query):
    url = f"https://coins.ha.com/c/search-results.zx?N=792+231+51+1055+4294942355&Ntk=SI_Titles-Desc&Nty=1&Ntt={query.replace(' ', '+')}"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    return [item.text.strip() for item in soup.select(".item-title")[:5] if item.text.strip()]

def search_greatcollections(query):
    url = f"https://www.greatcollections.com/search.php?search={query.replace(' ', '+')}"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    return [item.text.strip() for item in soup.select(".item_title")[:5] if item.text.strip()]

def search_ma_shops(query):
    url = f"https://www.ma-shops.com/search.php?searchstr={query.replace(' ', '+')}"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    return [item.text.strip() for item in soup.select(".title")[:5] if item.text.strip()]

def search_vcoins(query):
    url = f"https://www.vcoins.com/en/Search.aspx?search={query.replace(' ', '+')}"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    return [item.text.strip() for item in soup.select(".item-title")[:5] if item.text.strip()]

# --- App Interface ---
uploaded_file = st.file_uploader("Upload your Excel file with a 'Variety' column", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if "Variety" not in df.columns:
            st.error("The file must contain a column named 'Variety'.")
        else:
            varieties = df["Variety"].dropna().tolist()

            st.success(f"Loaded {len(varieties)} varieties.")
            sites = st.multiselect("Select auction sites to search:", [
                "eBay", "Heritage Auctions", "GreatCollections", "MA-Shops", "VCoins"
            ], default=["eBay", "Heritage Auctions"])

            if st.button("Start Search"):
                st.info("Searching, please wait...")
                search_funcs = {
                    "eBay": search_ebay,
                    "Heritage Auctions": search_heritage,
                    "GreatCollections": search_greatcollections,
                    "MA-Shops": search_ma_shops,
                    "VCoins": search_vcoins
                }

                results = []
                progress = st.progress(0)
                total = len(varieties) * len(sites)
                count = 0

                for variety in varieties:
                    for site in sites:
                        try:
                            listings = search_funcs[site](variety)
                            for listing in listings:
                                results.append({
                                    "Variety": variety,
                                    "Auction Site": site,
                                    "Listing": listing
                                })
                        except Exception as e:
                            results.append({
                                "Variety": variety,
                                "Auction Site": site,
                                "Listing": f"Error: {e}"
                            })
                        count += 1
                        progress.progress(count / total)
                        time.sleep(1.5)

                st.success("Search completed.")
                df_out = pd.DataFrame(results)
                st.dataframe(df_out)

                # Provide download
                from io import BytesIO

# Create Excel file in memory
output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_out.to_excel(writer, index=False)
output.seek(0)

# Streamlit download button
st.download_button(
    label="📥 Download Results as Excel",
    data=output,
    file_name="coin_search_results.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
    except Exception as e:
        st.error(f"Failed to load file: {e}")
else:
    st.warning("Please upload a spreadsheet to begin.")
