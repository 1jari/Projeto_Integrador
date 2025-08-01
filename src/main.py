import pygame
from cliente import Cliente
import cadastro
import pesquisa

pygame.init()
pygame.font.init()

fonte_titulo = pygame.font.Font("src/fonts/Roboto-VariableFont_wdth,wght.ttf", 48)
fonte_botao = pygame.font.Font("src/fonts/Roboto-VariableFont_wdth,wght.ttf", 32)

class Botao:
    def __init__(self, texto, x, y, largura=400, altura=60):
        self.ret = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.hover = False

    def desenhar(self, tela):
        cor_fundo = (34, 139, 34) if not self.hover else (50, 160, 50)
        sombra = pygame.Rect(self.ret.x + 4, self.ret.y + 4, self.ret.width, self.ret.height)
        pygame.draw.rect(tela, (0, 100, 0), sombra, border_radius=12)  # sombra
        pygame.draw.rect(tela, cor_fundo, self.ret, border_radius=12)

        txt = fonte_botao.render(self.texto, True, (255, 255, 255))
        tela.blit(txt, (self.ret.centerx - txt.get_width() // 2, self.ret.centery - txt.get_height() // 2))

    def atualizar_hover(self, pos):
        self.hover = self.ret.collidepoint(pos)

    def clicado(self, pos):
        return self.ret.collidepoint(pos)

def menu():
    app = Cliente("Menu do Herbario")
    if not app.Iniciar():
        return

    tela = app.GetTela()
    botoes = [
        Botao("Cadastrar Planta", 300, 200),
        Botao("Pesquisar por Nome", 300, 280),
        Botao("Pesquisar por Uso", 300, 360),
        Botao("Mostrar Todas as Plantas", 300, 440),
    ]

    fundo_cor = (235, 255, 235)

    while app.Rodando:
        tela.fill(fundo_cor)
        mouse_pos = pygame.mouse.get_pos()

        titulo = fonte_titulo.render("Menu do Herbario", True, (0, 100, 0))
        tela.blit(titulo, (tela.get_width() // 2 - titulo.get_width() // 2, 100))

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
            botao.atualizar_hover(mouse_pos)
            botao.desenhar(tela)

        pygame.display.flip()

    app.Encerrar()

if __name__ == "__main__":
    menu()
