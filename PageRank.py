import numpy as np

# Definiowanie grafu stron jako macierzy sąsiedztwa
pages = ["index.html", "about.html", "services.html", "portfolio.html", "blog.html", "contact.html", "article.html"]
links = {
    "index.html": ["about.html", "services.html", "portfolio.html", "blog.html", "contact.html", "article.html"],
    "about.html": ["index.html", "services.html", "portfolio.html", "blog.html", "contact.html", "article.html"],
    "services.html": ["index.html", "about.html", "portfolio.html", "blog.html", "contact.html", "article.html"],
    "portfolio.html": ["index.html", "about.html", "services.html", "blog.html", "contact.html", "article.html"],
    "blog.html": ["index.html", "about.html", "services.html", "portfolio.html", "contact.html", "article.html"],
    "contact.html": ["index.html", "about.html", "services.html", "portfolio.html", "blog.html", "article.html"],
    "article.html": ["index.html", "about.html", "services.html", "portfolio.html", "blog.html", "contact.html"]
}

# Liczba stron
N = len(pages)

# Macierz sąsiedztwa
M = np.zeros((N, N))

# Wypełnianie macierzy sąsiedztwa
for i, page in enumerate(pages):
    for link in links[page]:
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