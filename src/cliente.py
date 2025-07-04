import pygame
from conexao import Conexao

class Cliente:
    def __init__(self, Titulo) -> None:
        # Iniciar valores básicos
        self.__Fundo__ = (255, 255, 255)
        self.__Tamanho__ = (1280, 720)
        self.__Titulo__ = Titulo
        self.Rodando = False
        self.__Tela__ = None
        self.conexao = None

    def Iniciar(self):
        pygame.init()
        self.__Tela__ = pygame.display.set_mode(self.__Tamanho__)
        self.conexao = Conexao('herbario', '127.0.0.1')

        if not self.conexao.Iniciar():
            print("Não foi possível conectar!")
            return False

        pygame.display.set_caption(self.__Titulo__)
        self.__Tela__.fill(self.__Fundo__)
        pygame.display.flip()
        self.Rodando = True
        return True

    def Encerrar(self):
        if self.conexao:
            self.conexao.Fechar()
        pygame.quit()
        print("Aplicação encerrada.")

# Uso principal
tela = Cliente("Projeto Integrador")

if tela.Iniciar():
    print("Iniciando!")
    while tela.Rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tela.Rodando = False

    tela.Encerrar()
