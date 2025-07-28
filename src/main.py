import pygame
from cliente import Cliente
import cadastro
import pesquisa

pygame.init()
pygame.font.init()
fonte = pygame.font.Font("src/fonts/Roboto-VariableFont_wdth,wght.ttf", 32)

class Botao:
    def __init__(self, texto, x, y, largura=400, altura=60):
        self.ret = pygame.Rect(x, y, largura, altura)
        self.texto = texto

    def desenhar(self, tela):
        pygame.draw.rect(tela, (0, 128, 0), self.ret)
        txt = fonte.render(self.texto, True, (255, 255, 255))
        tela.blit(txt, (self.ret.x + 20, self.ret.y + 15))

    def clicado(self, pos):
        return self.ret.collidepoint(pos)

def menu():
    app = Cliente("Menu do Herbário")
    if not app.Iniciar():
        return

    tela = app.GetTela()
    botoes = [
        Botao("Cadastrar Planta", 300, 200),
        Botao("Pesquisar por Nome", 300, 280),
        Botao("Pesquisar por Uso", 300, 360),
        Botao("Mostrar Todas as Plantas", 300, 440),
    ]

    while app.Rodando:
        tela.fill((240, 255, 240))
        titulo = fonte.render("Menu do Herbário", True, (0, 128, 0))
        tela.blit(titulo, (380, 100))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                app.Rodando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for i, botao in enumerate(botoes):
                    if botao.clicado(evento.pos):
                        if i == 0:
                            from cadastro import iniciar_cadastro
                            iniciar_cadastro(app)
                        elif i == 1:
                            from pesquisa import pesquisar_por_nome
                            pesquisar_por_nome(app)
                        elif i == 2:
                            from pesquisa import pesquisar_por_uso
                            pesquisar_por_uso(app)
                        elif i == 3:
                            from pesquisa import mostrar_paginas
                            resultado = app.conexao.Executar("SELECT * FROM plantas")
                            mostrar_paginas(app, resultado)
        for botao in botoes:
            botao.desenhar(tela)
        pygame.display.flip()

    app.Encerrar()

if __name__ == "__main__":
    menu()