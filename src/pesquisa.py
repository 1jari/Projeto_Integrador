import pygame
from conexao import Conexao
import hashlib
import os

pygame.init()
pygame.font.init()
fonte = pygame.font.Font("src/fonts/Roboto-VariableFont_wdth,wght.ttf", 32)

def criar_hash(txt):
    resultado = 0
    for c in txt:
        resultado += ord(c)  # Usa o código ASCII/unicode do caractere
    return resultado

def quebrar_texto(texto, fonte, largura_max):
    palavras = texto.split(' ')
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        teste_linha = linha_atual + palavra + " "
        largura, _ = fonte.size(teste_linha)
        if largura <= largura_max:
            linha_atual = teste_linha
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "
    linhas.append(linha_atual)
    return linhas

def pesquisar_por_nome(app):
    buscar(app, campo="nome")

def pesquisar_por_uso(app):
    buscar(app, campo="uso")

def buscar(app, campo):
    tela = app.GetTela()
    texto = ""
    ativo = True

    while ativo:
        tela.fill((255, 255, 255))
        txt = fonte.render(f"Buscar por {campo}:", True, (0, 0, 0))
        input_txt = fonte.render(texto, True, (0, 0, 0))
        tela.blit(txt, (50, 50))
        tela.blit(input_txt, (50, 100))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ativo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    resultado = app.conexao.Executar(f"SELECT * FROM plantas WHERE {campo} LIKE '%{texto}%'")
                    mostrar_paginas(app, resultado)
                    return
                elif evento.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                else:
                    texto += evento.unicode

def mostrar_paginas(app, resultados, plantas_por_pagina=3):
    tela = app.GetTela()
    total = len(resultados)
    pagina_atual = 0
    largura_texto = 700  

    rodando = True
    while rodando:
        tela.fill((255, 255, 255))

        inicio = pagina_atual * plantas_por_pagina
        fim = inicio + plantas_por_pagina
        pagina_plantas = resultados[inicio:fim]

        y = 50
        for planta in pagina_plantas:
            id_, nome, nome_cientifico, descricao, caracteristicas, uso, _ = planta

            # Caminho baseado no nome da planta (ex: "alecrim.jpg")
            nome_arquivo = f"{hashlib.md5(nome.encode()).hexdigest()}.jpg"
            caminho_img = os.path.join("dados", "img", nome_arquivo)

            try:
                if os.path.isfile(caminho_img):
                    img = pygame.image.load(caminho_img)
                    img = pygame.transform.scale(img, (100, 100))
                    tela.blit(img, (50, y))
                else:
                    print(f"Imagem não encontrada: {caminho_img}")
            except Exception as e:
                print(f"Erro ao carregar imagem: {e}")

            tela.blit(fonte.render(f"Nome: {nome}", True, (0, 0, 0)), (160, y))
            tela.blit(fonte.render(f"Nome Científico: {nome_cientifico}", True, (0, 0, 0)), (160, y + 25))

            linhas_desc = quebrar_texto(descricao, fonte, largura_texto)
            linhas_caract = quebrar_texto(caracteristicas, fonte, largura_texto)
            linhas_uso = quebrar_texto(uso, fonte, largura_texto)

            offset = 50
            for linha in linhas_desc:
                tela.blit(fonte.render(linha, True, (0, 0, 0)), (160, y + offset))
                offset += 25

            tela.blit(fonte.render("Características:", True, (0, 0, 0)), (160, y + offset))
            offset += 25
            for linha in linhas_caract:
                tela.blit(fonte.render(linha, True, (0, 0, 0)), (160, y + offset))
                offset += 25

            tela.blit(fonte.render("Uso:", True, (0, 0, 0)), (160, y + offset))
            offset += 25
            for linha in linhas_uso:
                tela.blit(fonte.render(linha, True, (0, 0, 0)), (160, y + offset))
                offset += 25

            y += max(offset + 20, 140)

        texto_pagina = fonte.render(f"Página {pagina_atual + 1} de {((total - 1) // plantas_por_pagina) + 1}", True, (0, 0, 0))
        tela.blit(texto_pagina, (50, 20))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT and fim < total:
                    pagina_atual += 1
                elif evento.key == pygame.K_LEFT and pagina_atual > 0:
                    pagina_atual -= 1
                elif evento.key == pygame.K_ESCAPE:
                    rodando = False

def aguardar_fechar():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type in [pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                esperando = False