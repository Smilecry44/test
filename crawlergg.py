import requests
from bs4 import BeautifulSoup
import streamlit as st 
import pandas as pd

st.set_page_config(page_title="Keyword SERP parser", layout="wide")
st.write("# Keyword SERP parser")
st.write("Choisissez votre mot clé pour analyse")
st.sidebar.write("## Votre mot clé : ")

keyword = st.sidebar.text_input("")



def search_google(keyword):
    url = f"https://www.google.com/search?q={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_search_results(html):
    soup = BeautifulSoup(html, "html.parser")
    results = soup.select(".g")
    search_results = []
    for result in results:
        title_element = result.select_one("h3")
        if title_element is not None:
            title = title_element.text
            link = result.select_one("a")["href"]
            search_results.append({"title": title, "link": link})

    return search_results

def write_results_to_file(results, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Analyse de SERP réalisée sur le kwd : {keyword} \n\n")
        for result in results:
            file.write(f"Titre : {result['title']}\n")
            file.write(f"Lien : {result['link']}\n\n")

search_html = search_google(keyword)
results = parse_search_results(search_html)

# Créer un DataFrame pandas à partir des résultats puis Afficher le DataFrame en utilisant st.table()
df = pd.DataFrame(results)
st.table(df)