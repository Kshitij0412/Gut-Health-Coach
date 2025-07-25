import requests
from bs4 import BeautifulSoup

urls = [
    "https://www.healthline.com/health/gut-health",
    "https://www.precisionnutrition.com/all-about-nutrition-gut-health",
    "https://pubmed.ncbi.nlm.nih.gov/35105664/",
]

def scrape_to_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    paragraphs = soup.find_all('p')
    return "\n".join(p.get_text() for p in paragraphs if len(p.get_text()) > 50)

all_text = ""
for url in urls:
    all_text += scrape_to_text(url) + "\n"

with open("data/gut_health_knowledge_1.txt", "w", encoding='utf-8') as f:
    f.write(all_text)