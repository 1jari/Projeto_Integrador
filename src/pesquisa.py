import pygame
from conexao import Conexao

pygame.init()
pygame.font.init()
fonte = pygame.font.SysFont(None, 28)

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

def mostrar_todas(app):
    tela = app.GetTela()
    resultado = app.conexao.Executar("SELECT * FROM plantas")
    tela.fill((255, 255, 255))

    y = 50
    for nome, url in resultado:
        try:
            imagem = pygame.image.load(url)
            tela.blit(imagem, (50, y))
        except:
            pass
        txt = fonte.render(nome, True, (0, 0, 0))
        tela.blit(txt, (200, y + 20))
        y += 100

    pygame.display.flip()
    aguardar_fechar()

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
            id_, nome, nome_cientifico, descricao, caracteristicas, uso, url = planta

            try:
                img = pygame.image.load(url)
                tela.blit(img, (50, y))
            except:
                pass

            tela.blit(fonte.render(f"Nome: {nome}", True, (0, 0, 0)), (200, y))
            tela.blit(fonte.render(f"Nome Científico: {nome_cientifico}", True, (0, 0, 0)), (200, y + 25))

            linhas_desc = quebrar_texto(descricao, fonte, largura_texto)
            linhas_caract = quebrar_texto(caracteristicas, fonte, largura_texto)
            linhas_uso = quebrar_texto(uso, fonte, largura_texto)

            offset = 50
            for linha in linhas_desc:
                tela.blit(fonte.render(linha, True, (0, 0, 0)), (200, y + offset))
                offset += 25

            tela.blit(fonte.render("Características:", True, (0, 0, 0)), (200, y + offset))
            offset += 25
            for linha in linhas_caract:
                tela.blit(fonte.render(linha, True, (0, 0, 0)), (200, y + offset))
                offset += 25

            tela.blit(fonte.render("Uso:", True, (0, 0, 0)), (200, y + offset))
            offset += 25
            for linha in linhas_uso:
                tela.blit(fonte.render(linha, True, (0, 0, 0)), (200, y + offset))
                offset += 25

            y += max(offset + 20, 140)  

        texto_pagina = fonte.render(f"Página {pagina_atual + 1} de {((total - 1) // plantas_por_pagina) + 1}", True, (0, 0, 0))
        tela.blit(texto_pagina, (50, 20))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    if fim < total:
                        pagina_atual += 1
                elif evento.key == pygame.K_LEFT:
                    if pagina_atual > 0:
                        pagina_atual -= 1
                elif evento.key == pygame.K_ESCAPE:
                    rodando = False

def aguardar_fechar():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type in [pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                esperando = False