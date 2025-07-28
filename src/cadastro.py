import pygame
import sys
from cliente import Cliente
import pegarimagem
import os

pygame.font.init()
fonte = pygame.font.Font("src/fonts/Roboto-VariableFont_wdth,wght.ttf", 32)

def desenhar_input(tela, campo, y, ativo):
    cor = (200, 200, 255) if ativo else (230, 230, 230)
    ret = pygame.Rect(100, y, 800, 40)
    pygame.draw.rect(tela, cor, ret)
    label = fonte.render(campo["label"], True, (0, 0, 0))
    tela.blit(label, (100, y - 22))
    texto = fonte.render(campo["texto"] or "", True, (0, 0, 0))
    tela.blit(texto, (110, y + 8))
    return ret

def iniciar_cadastro(app):
    tela = app.GetTela()
    pygame.init()
    fonte_titulo = pygame.font.Font("src/fonts/Roboto-VariableFont_wdth,wght.ttf", 38)
    fonte_input = pygame.font.Font("src/fonts/Roboto-VariableFont_wdth,wght.ttf", 28)
    fonte_botao = pygame.font.Font("src/fonts/Roboto-VariableFont_wdth,wght.ttf", 28)

    campos = [
        {"nome": "nome", "label": "Nome*", "texto": "", "obrigatorio": True},
        {"nome": "nome_cientifico", "label": "Nome Científico", "texto": "", "obrigatorio": False},
        {"nome": "descricao", "label": "Descrição", "texto": "", "obrigatorio": False},
        {"nome": "caracteristicas", "label": "Características", "texto": "", "obrigatorio": False},
        {"nome": "uso", "label": "Uso", "texto": "", "obrigatorio": False},
    ]

    campo_ativo = 0
    app = Cliente("Cadastro de Planta")
    if not app.Iniciar():
        sys.exit()
    tela = app.GetTela()

    while app.Rodando:
        tela.fill((235, 255, 235))

        eventos = pygame.event.get()
        entradas = []

        # Título
        titulo = fonte_titulo.render("Cadastro de Planta", True, (0, 100, 0))
        tela.blit(titulo, (tela.get_width() // 2 - titulo.get_width() // 2, 20))

        for i, campo in enumerate(campos):
            y = 100 + i * 80
            ret = pygame.Rect(100, y, 800, 40)
            sombra = pygame.Rect(104, y + 4, 800, 40)

            # Estilo do input
            cor = (255, 255, 255)
            cor_borda = (150, 200, 150) if campo_ativo == i else (210, 210, 210)
            pygame.draw.rect(tela, (200, 230, 200), sombra, border_radius=8)
            pygame.draw.rect(tela, cor, ret, border_radius=8)
            pygame.draw.rect(tela, cor_borda, ret, width=2, border_radius=8)

            # Label
            label = fonte_input.render(campo["label"], True, (0, 0, 0))
            tela.blit(label, (100, y - 28))

            # Texto digitado
            texto = fonte_input.render(campo["texto"] or "", True, (0, 0, 0))
            tela.blit(texto, (110, y + 6))
            entradas.append(ret)

        # Botão
        botao = pygame.Rect(100, 530, 250, 50)
        pygame.draw.rect(tela, (0, 120, 0), botao, border_radius=10)
        texto_botao = fonte_botao.render("Cadastrar Planta", True, (255, 255, 255))
        tela.blit(texto_botao, (botao.x + 20, botao.y + 10))

        for evento in eventos:
            if evento.type == pygame.QUIT:
                app.Rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for i, entrada in enumerate(entradas):
                    if entrada.collidepoint(evento.pos):
                        campo_ativo = i
                if botao.collidepoint(evento.pos):
                    if all(c["texto"] for c in campos if c["obrigatorio"]):
                        valores = [f"'{c['texto']}'" if c['texto'] else "NULL" for c in campos]
                        colunas = ", ".join(c["nome"] for c in campos)
                        valores_str = ", ".join(valores)
                        sql = f"INSERT INTO plantas ({colunas}) VALUES ({valores_str})"
                        try:
                            app.conexao.Executar(sql)
                            nome_planta = campos[0]["texto"]
                            if os.path.exists(pegarimagem.caminho_contador):
                                with open(pegarimagem.caminho_contador, "r") as arquivo:
                                    contador = int(arquivo.read().strip())
                            pegarimagem.buscar_e_salvar_imagem(nome_planta, contador)
                            print("Planta cadastrada com sucesso!")
                            for c in campos:
                                c["texto"] = ""
                        except Exception as e:
                            print("Erro ao cadastrar:", e)
                    else:
                        print("Preencha os campos obrigatórios!")
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    campos[campo_ativo]["texto"] = campos[campo_ativo]["texto"][:-1]
                elif evento.key == pygame.K_TAB:
                    campo_ativo = (campo_ativo + 1) % len(campos)
                elif evento.key == pygame.K_ESCAPE:
                    app.Rodando = False
                else:
                    campos[campo_ativo]["texto"] += evento.unicode

        pygame.display.flip()

    app.Encerrar()
