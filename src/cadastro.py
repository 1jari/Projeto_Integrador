import pygame
import sys
from cliente import Cliente
pygame.font.init()
fonte = pygame.font.SysFont(None, 28)

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
    fonte = pygame.font.SysFont(None, 28)

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
        tela.fill((255, 255, 255))
        eventos = pygame.event.get()

        entradas = []
        for i, campo in enumerate(campos):
            entrada = desenhar_input(tela, campo, 50 + i * 80, campo_ativo == i)
            entradas.append(entrada)

        botao = pygame.Rect(100, 550, 200, 50)
        pygame.draw.rect(tela, (0, 150, 0), botao)
        texto_botao = fonte.render("Cadastrar Planta", True, (255, 255, 255))
        tela.blit(texto_botao, (botao.x + 15, botao.y + 10))

        for evento in eventos:
            if evento.type == pygame.QUIT:
                app.Rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
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
                            print("Planta cadastrada com sucesso!")
                            for c in campos:
                                c["texto"] = ""
                        except Exception as e:
                            print("Erro ao cadastrar:", e)
                    else:
                        print("Preencha os campos obrigatórios!")

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    campos[campo_ativo]["texto"] = campos[campo_ativo]["texto"][:-1]
                elif evento.key == pygame.K_TAB:
                    campo_ativo = (campo_ativo + 1) % len(campos)
                else:
                    campos[campo_ativo]["texto"] += evento.unicode

        pygame.display.flip()

    app.Encerrar()