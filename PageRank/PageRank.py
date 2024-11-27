import requests
from bs4 import BeautifulSoup
import numpy as np
import csv

# Funkcja pobiera wszystkie linki z danej strony,
# które prowadzą do tej samej domeny i kończą się na .html
def get_links(url, domain):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/'):
                href = domain + href
            elif not href.startswith('http'):
                href = domain + '/' + href
            if domain in href and href.endswith('.html'):
                links.add(href)
        print(f"Links found on {url}: {links}")
        return links
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set()

domain = 'https://kamknap.github.io'
pages = [
    'https://kamknap.github.io/index.html',
    'https://kamknap.github.io/about.html',
    'https://kamknap.github.io/services.html',
    'https://kamknap.github.io/portfolio.html',
    'https://kamknap.github.io/blog.html',
    'https://kamknap.github.io/contact.html',
    'https://kamknap.github.io/article.html',
    'https://kamknap.github.io/articlePhp.html'
]

links = {page: get_links(page, domain) for page in pages}

# Liczba stron
N = len(pages)

# Macierz sąsiedztwa
M = np.zeros((N, N))

# Wypełnianie macierzy sąsiedztwa
for i, page in enumerate(pages):
    for link in links[page]:
        if link in pages:  # Sprawdzanie, czy link jest wewnętrzny
            j = pages.index(link)
            M[j, i] = 1 / len(links[page])

# Parametry algorytmu PageRank
d = 0.85  # Damping factor
num_iterations = 100
tolerance = 1.0e-6

# Inicjalizacja rankingu stron
rank = np.ones(N) / N

# Iteracyjne obliczanie PageRank
for _ in range(num_iterations):
    new_rank = (1 - d) / N + d * M @ rank
    if np.linalg.norm(new_rank - rank, 1) < tolerance:
        break
    rank = new_rank

# Wyświetlanie wyników
page_ranks = {pages[i]: rank[i] for i in range(N)}
sorted_page_ranks = sorted(page_ranks.items(), key=lambda item: item[1], reverse=True)

print("PageRank dla stron:")
for page, rank in sorted_page_ranks:
    print(f"{page}: {rank:.4f}")

# Zapisanie węzłów do pliku CSV
with open('nodes.csv', 'w', newline='') as csvfile:
    fieldnames = ['Id', 'Label', 'PageRank']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for page, rank in page_ranks.items():
        writer.writerow({'Id': page, 'Label': page, 'PageRank': rank})

# Zapisanie krawędzi do pliku CSV z wagami zgodnie z PageRank
with open('edges.csv', 'w', newline='') as csvfile:
    fieldnames = ['Source', 'Target', 'Weight']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i, page in enumerate(pages):
        for link in links[page]:
            if link in pages:
                weight = page_ranks[page]  # Użycie PageRank wagi
                print(f"Edge from {page} to {link} with weight {weight}")
                writer.writerow({'Source': page, 'Target': link, 'Weight': weight})