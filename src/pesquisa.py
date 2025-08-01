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

def mostrar_paginas(app, resultados, plantas_por_pagina=2):
    tela = app.GetTela()
    total = len(resultados)
    pagina_atual = 0

    fonte_titulo = pygame.font.Font("src/fonts/Roboto-VariableFont_wdth,wght.ttf", 36)
    fonte_texto = pygame.font.Font("src/fonts/Roboto-VariableFont_wdth,wght.ttf", 24)

    largura_texto = 700
    margem_lateral = 40
    altura_disponivel = tela.get_height() - 100

    rodando = True
    while rodando:
        tela.fill((235, 255, 235))  # fundo

        inicio = pagina_atual * plantas_por_pagina
        fim = inicio + plantas_por_pagina
        pagina_plantas = resultados[inicio:fim]

        y = 80
        for planta in pagina_plantas:
            id_, nome, nome_cientifico, descricao, caracteristicas, uso, _ = planta

            linhas_desc = quebrar_texto(descricao, fonte_texto, largura_texto)
            linhas_caract = quebrar_texto(caracteristicas, fonte_texto, largura_texto)
            linhas_uso = quebrar_texto(uso, fonte_texto, largura_texto)

            altura_card = 160 + 25 * (len(linhas_desc) + len(linhas_caract) + len(linhas_uso))

            # Evita que vaze para fora da tela
            if y + altura_card > altura_disponivel:
                break

            # Cartão
            card_rect = pygame.Rect(margem_lateral, y - 10, 920, altura_card)
            sombra_rect = pygame.Rect(margem_lateral + 4, y - 6, 920, altura_card)
            pygame.draw.rect(tela, (200, 230, 200), sombra_rect, border_radius=12)
            pygame.draw.rect(tela, (255, 255, 255), card_rect, border_radius=12)

            # Imagem
            nome_arquivo = f"{hashlib.md5(nome.encode()).hexdigest()}.jpg"
            caminho_img = os.path.join("dados", "img", nome_arquivo)
            try:
                if os.path.isfile(caminho_img):
                    img = pygame.image.load(caminho_img)
                    img = pygame.transform.scale(img, (100, 100))
                    tela.blit(img, (margem_lateral + 20, y + 10))
            except Exception as e:
                print(f"Erro na imagem: {e}")

            texto_x = margem_lateral + 140
            texto_y = y + 10

            tela.blit(fonte_texto.render(f"Nome: {nome}", True, (0, 100, 0)), (texto_x, texto_y))
            texto_y += 28
            tela.blit(fonte_texto.render(f"Nome Científico: {nome_cientifico}", True, (0, 100, 0)), (texto_x, texto_y))
            texto_y += 35

            def desenhar_bloco(titulo, linhas, y_pos):
                tela.blit(fonte_texto.render(f"{titulo}:", True, (0, 0, 0)), (texto_x, y_pos))
                y_pos += 25
                for linha in linhas:
                    tela.blit(fonte_texto.render(linha, True, (50, 50, 50)), (texto_x, y_pos))
                    y_pos += 25
                return y_pos

            texto_y = desenhar_bloco("Descrição", linhas_desc, texto_y)
            texto_y = desenhar_bloco("Características", linhas_caract, texto_y)
            texto_y = desenhar_bloco("Uso", linhas_uso, texto_y)

            y += altura_card + 20

        # Número da página
        texto_pagina = fonte_titulo.render(
            f"Página {pagina_atual + 1} de {((total - 1) // plantas_por_pagina) + 1}",
            True, (0, 100, 0))
        tela.blit(texto_pagina, (tela.get_width() // 2 - texto_pagina.get_width() // 2, 20))

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