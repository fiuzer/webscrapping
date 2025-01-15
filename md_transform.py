import json
from news_extractor import *

def salvar_em_md(articles, filename="README.md"):
  with open(filename, "w", encoding="utf-8") as file:
    file.write('# Últimas Notícias de Tecnologia\n\n')
    for article in articles:
      file.write(f"## {article['title']}\n")
      file.write(f"**Conteúdo:** {article['content'][:500]}...\n\n")
      file.write(f"[Leia a notícia completa]({article['url']})\n\n")
      file.write("---\n")
  print(f"Arquivo Markdown gerado: {filename}")

if __name__ == "__main__":
    with open("news.json", "r", encoding="utf-8") as file:
        articles = json.load(file)
    salvar_em_md(articles)