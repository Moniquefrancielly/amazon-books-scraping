# 📚 Amazon Books Scraping & Analysis

Projeto de coleta, análise e visualização de dados dos livros mais vendidos da Amazon Brasil.

---

## 🎯 Objetivo

Este projeto tem como objetivo coletar dados reais do ranking de livros mais vendidos da Amazon Brasil, tratar essas informações e gerar análises visuais que permitam identificar padrões de consumo, comportamento do público e características dos livros mais populares.

---

## ⚙️ Etapas do Projeto

### 1. Web Scraping

* Coleta automatizada dos dados diretamente do site da Amazon
* Extração de:

  * Título
  * Autor
  * Tipo de capa
  * Preço
  * Avaliação
  * Número de avaliações
  * Posição no ranking

Os dados são salvos em formato CSV para posterior análise.

### 2. Tratamento de Dados

* Limpeza e padronização dos valores
* Conversão de preços para formato numérico
* Organização das informações em estrutura tabular

### 3. Análise e Visualização

Foram criadas duas formas de visualização:

#### 📊 Dashboard Web (HTML + Chart.js)

* Gráficos interativos diretamente no navegador
* Distribuição de preços
* Comparação entre avaliação e preço
* Ranking dos livros
* Filtros por tipo de capa

#### 📈 Dashboard no Power BI

* Análise mais aprofundada dos dados
* Métricas principais:

  * Preço médio
  * Total de avaliações
  * Livro mais popular
* Gráficos:

  * Autores com mais livros
  * Livros com mais avaliações
  * Preço médio por tipo de capa
  * Relação entre preço e avaliação

---

## 🛠️ Tecnologias Utilizadas

* Python
* Playwright (Web Scraping)
* Pandas (Manipulação de dados)
* HTML / CSS / JavaScript
* Chart.js (Visualização web)
* Power BI (Dashboard analítico)

---

## 📁 Estrutura do Projeto

```
amazon-books-scraping/
├── scraper/        # Código de scraping (Python)
├── data/           # Arquivos CSV gerados
├── dashboard/      # Dashboard HTML
├── powerbi/        # Arquivo do Power BI (.pbix)
├── README.md
```

---

## 🚀 Como Executar

### 1. Clonar o repositório

```
git clone https://github.com/seu-usuario/amazon-books-scraping.git
cd amazon-books-scraping
```

### 2. Instalar dependências

```
pip install playwright pandas
playwright install
```

### 3. Rodar o scraper

```
python scraper/seu_script.py
```

### 4. Visualizar dashboard web

* Abrir o arquivo HTML na pasta `dashboard`
* Ou usar a extensão Live Server no VS Code

### 5. Visualizar no Power BI

* Abrir o arquivo `.pbix` na pasta `powerbi`

---

## 📊 Insights Obtidos

* A maioria dos livros mais vendidos está na faixa de preço entre R$30 e R$60
* Não existe relação direta entre preço e avaliação
* Livros com capa dura tendem a ser mais caros
* Gêneros como romance e suspense dominam o ranking

---

## 💡 Possíveis Melhorias

* Automatizar coleta periódica dos dados
* Criar API para servir os dados
* Deploy do dashboard web
* Análise temporal (evolução dos rankings)

---

## 👩‍💻 Autora

Projeto desenvolvido para fins educacionais e de portfólio, explorando conceitos de scraping, análise de dados e visualização.

---

## ⭐ Observação

Os dados utilizados são públicos e foram coletados apenas para fins de estudo.
