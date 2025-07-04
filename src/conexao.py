import  pymysql
from    pymysql import Error

class Conexao:
    def __init__(self, db, host):
        self.__Db__ = db
        self.__Host__ = host
        self.Conexao = None
        self.Cursor = None

    def Iniciar(self):
        try:
            self.Conexao = pymysql.connect(
                host=self.__Host__,
                port=3306,
                user='root',
                password='',
                database=self.__Db__
            )
            self.Cursor = self.Conexao.cursor()
            print("Conexão ao MySQL estabelecida com sucesso")
            return True
        except Error as erro:
            print(f"Não foi possível conectar ao MySQL: {erro}")
            return False

    def Executar(self, cmd):
        if self.Conexao and self.Cursor:
            self.Cursor.execute(cmd)
            return self.Cursor.fetchall()
        else:
            print("Conexão não foi iniciada")
            return None

    def Fechar(self):
        if self.Conexao:
            self.Conexao.close()
            print("Conexão ao MySQL encerrada")
