import os
import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Acessando Amazon Mais Vendidos em Livros...")
        await page.goto("https://www.amazon.com.br/gp/bestsellers/books", wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)

        dados = []
        titulos_vistos = set()
        tentativas_sem_novos = 0
        MAX_LIVROS = 100
        MAX_TENTATIVAS = 5

        while len(dados) < MAX_LIVROS and tentativas_sem_novos < MAX_TENTATIVAS:
            quantidade_antes = len(dados)

            cards = await page.query_selector_all("div.zg-grid-general-faceout")

            for card in cards:
                try:
                    # ── Título ───────────────────────────────────────
                    t = await card.query_selector("div[class*='p13n-sc-css-line-clamp']")
                    titulo = (await t.inner_text()).strip() if t else None
                    if not titulo or titulo in titulos_vistos:
                        continue
                    titulos_vistos.add(titulo)

                    # ── Autor e Tipo de Capa ─────────────────────────
                    # Estrutura HTML observada:
                    #   div.a-row.a-size-small → autor (ex: "Jonathan Haidt")
                    #   div.a-row              → tipo de capa (ex: "Capa comum")
                    linhas_small  = await card.query_selector_all("div.a-row.a-size-small")
                    linhas_normal = await card.query_selector_all("div.a-row:not(.a-size-small)")

                    autor = "Sem autor"
                    if linhas_small:
                        txt = (await linhas_small[0].inner_text()).strip()
                        if txt:
                            autor = txt.replace("›", "").strip()

                    # Tipo de capa — span com classes específicas observadas no F12
                    tipo_capa = "Não informado"
                    tipos_conhecidos = ["Capa comum", "Capa dura", "Livro de bolso",
                                        "Folheto", "Espiral", "Brochura"]
                    capa_el = await card.query_selector(
                        "span.a-size-small.a-color-secondary.a-text-normal"
                    )
                    if capa_el:
                        txt = (await capa_el.inner_text()).strip()
                        for tipo in tipos_conhecidos:
                            if tipo.lower() in txt.lower():
                                tipo_capa = tipo
                                break

                    # ── Preço ────────────────────────────────────────
                    preco_el  = await card.query_selector("span[class*='p13n-sc-price']")
                    preco_raw = (await preco_el.inner_text()).strip() if preco_el else ""
                    preco_num = None
                    if preco_raw:
                        try:
                            preco_num = float(
                                preco_raw.replace("R$", "").replace("\xa0", "")
                                         .replace(".", "").replace(",", ".").strip()
                            )
                        except:
                            preco_num = None

                    # ── Avaliação (estrelas) ──────────────────────────
                    av_el  = await card.query_selector("span.a-icon-alt")
                    av_raw = (await av_el.inner_text()).strip() if av_el else ""
                    avaliacao = None
                    if av_raw:
                        try:
                            avaliacao = float(av_raw.split()[0].replace(",", "."))
                        except:
                            avaliacao = None

                    # ── Número de avaliações ──────────────────────────
                    nav_el  = await card.query_selector("span.a-size-small")
                    nav_raw = (await nav_el.inner_text()).strip() if nav_el else "0"
                    try:
                        num_aval = int(nav_raw.replace(".", "").replace(",", "").split()[0])
                    except:
                        num_aval = 0

                    # ── Posição no ranking ────────────────────────────
                    rank_el  = await card.query_selector("span.zg-bdg-text")
                    rank_raw = (await rank_el.inner_text()).strip() if rank_el else ""
                    try:
                        posicao = int(rank_raw.replace("#", "").replace("Nº", "").strip())
                    except:
                        posicao = len(dados) + 1

                    dados.append({
                        "posicao":        posicao,
                        "titulo":         titulo,
                        "autor":          autor,
                        "tipo_capa":      tipo_capa,
                        "preco_brl":      preco_num,
                        "avaliacao":      avaliacao,
                        "num_avaliacoes": num_aval,
                        "data_coleta":    datetime.now().strftime("%d/%m/%Y %H:%M"),
                    })

                    print(f"  #{posicao} {titulo[:40]} | {autor[:25]} | {tipo_capa} | R${preco_num}")

                except Exception as e:
                    print(f"Erro num card: {e}")
                    continue

            novos = len(dados) - quantidade_antes
            print(f"\n[Scroll] Total: {len(dados)} | Novos: {novos}")

            if novos == 0:
                tentativas_sem_novos += 1
                print(f"Sem novos. Tentativa {tentativas_sem_novos}/{MAX_TENTATIVAS}")
            else:
                tentativas_sem_novos = 0

            # Tenta ir para próxima página
            prox = await page.query_selector("li.a-last a")
            if prox:
                await prox.click()
                await page.wait_for_timeout(3000)
            else:
                await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2500)

        # ── Exportação ────────────────────────────────────────────────
        pasta_script  = os.path.dirname(os.path.abspath(__file__))
        pasta_destino = os.path.join(pasta_script, "saidas_scrapings")
        os.makedirs(pasta_destino, exist_ok=True)

        caminho_csv = os.path.join(pasta_destino, "livros_amazon.csv")
        df = pd.DataFrame(dados)
        df.to_csv(caminho_csv, index=False, encoding="utf-8")

        print(f"\nSucesso! {len(dados)} livros salvos em '{caminho_csv}'")
        print(df.head(10).to_string(index=False))

        cols = [c for c in ["preco_brl", "avaliacao", "num_avaliacoes"] if c in df.columns]
        if cols:
            print("\n--- Estatísticas ---")
            print(df[cols].describe().round(2))

        await browser.close()

asyncio.run(run())