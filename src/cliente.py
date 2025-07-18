import pygame
from conexao import Conexao

class Cliente:
    def __init__(self, Titulo) -> None:
        self.__Fundo__ = (255, 255, 255)
        self.__Tamanho__ = (1024, 900)
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
        self.Rodando = True
        self.__Tela__.fill(self.__Fundo__)
        return True

    def Encerrar(self):
        if self.conexao:
            self.conexao.Fechar()
        pygame.quit()
        print("Aplicação encerrada.")

tela = Cliente("Projeto Integrador")

if tela.Iniciar():
    print("Iniciando!")

    resultado = tela.conexao.Executar("SELECT COUNT(*) FROM plantas")
    if not resultado:
        print("Erro ao obter número de plantas")
        exit()

    tablelen = resultado[0][0]
    print(f"Total de plantas: {tablelen}")

    while tela.Rodando:
        tela.__Tela__.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tela.Rodando = False

        for i in range(1, tablelen + 1):
            dados = tela.conexao.Executar(f"SELECT imagem_url FROM plantas WHERE ID = {i}")
            if dados:
                caminho = dados[0][0]  
                try:
                    imagem = pygame.image.load(caminho)
                    tela.__Tela__.blit(imagem, ((i - 1) * 64, 50))  
                except Exception as e:
                    print(f"Erro ao carregar imagem do ID {i}: {e}")

        pygame.display.flip()

    tela.Encerrar()

