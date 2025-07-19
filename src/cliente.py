import pygame
from conexao import Conexao

class Cliente:
    def __init__(self, Titulo="Sistema") -> None:
        self._Fundo = (255, 255, 255)
        self._Tamanho = (1024, 900)
        self._Titulo = Titulo
        self.Rodando = False
        self._Tela = None
        self.conexao = None

    def Iniciar(self):
        pygame.init()
        self._Tela = pygame.display.set_mode(self._Tamanho)
        self.conexao = Conexao('herbario', '127.0.0.1')
        if not self.conexao.Iniciar():
            print("Não foi possível conectar!")
            return False
        pygame.display.set_caption(self._Titulo)
        self.Rodando = True
        self._Tela.fill(self._Fundo)
        return True

    def Encerrar(self):
        if self.conexao:
            self.conexao.Fechar()
        pygame.quit()
        print("Aplicação encerrada.")

    def GetTela(self):
        return self._Tela

