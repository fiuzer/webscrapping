import requests
from bs4 import BeautifulSoup
import json

url = 'https://g1.globo.com/tecnologia/' # Site para scraping de manchetes

# função onde vamos buscar a URl das noticias
def buscar_news(url):
  try:
    response = requests.get(url)
    response.raise_for_status()
    return response.text

  except requests.RequestException as e:
    print(f'Erro ao acessar {url}: {e}')
    return None
  
def extrair_conteudo_artigo(article_url):
    html = buscar_news(article_url)
    if not html:
        return "Falha ao obter o conteúdo do artigo."

    soup = BeautifulSoup(html, "html.parser")

    # Identifique o seletor que contém o texto principal do artigo
    content = soup.find("div", class_="wall protected-content")  # Ajuste conforme necessário
    if content:
        return content.get_text(strip=True)
    return "Conteúdo do artigo não encontrado."

# função onde vamos extrair as noticias
def extrair_news(html):
  soup = BeautifulSoup(html, "html.parser")
  articles = []

  for article in soup.find_all("div", class_="feed-post-body"):
    title = article.find("h2")
    summary = article.find("div", class_="feed-post-body-resumo")
    link = article.find("a", class_="feed-post-link")
  

    if title and summary and link:
      article_url = link.get("href")
      article_content = extrair_conteudo_artigo(article_url)
      articles.append({
        "title": title.get_text(strip=True) if title else "Título não encontrado",
        "summary": summary.get_text(strip=True) if summary else "Sem resumo disponível",
        "url": article_url,
        "content": article_content,
      })

  return articles

# função onde vamos salvar as noticias em um arquivo json
def salvar_news(articles, filename="news.json"):
  with open(filename, "w", encoding="utf-8") as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)
  print(f'Notícias salvas em {filename}')

# função principal para rodar o programa.

if __name__ == "__main__":
  print("Iniciando a coleta de noticias...")
  html_content = buscar_news(url)
  if html_content:
    print("Analisando o conteúdo...")
    news = extrair_news(html_content)
    if news:
      print(f'{len(news)} notícias relevante enctrada(s).')
      salvar_news(news)
    else:
      print("Nenhuma notícia relevante encontrada.")
  else:
    print("Falha ao obter conteúdo da página.")
