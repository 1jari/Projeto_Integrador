import  pymysql
from    pymysql import Error

class Conexao:
    def __init__(self, db, host, user='root', password=''):
        self.__Db__ = db
        self.__Host__ = host
        self.__User__ = user
        self.__Password__ = password
        self.Conexao = None
        self.Cursor = None
    def Iniciar(self):
        try:
            self.Conexao = pymysql.connect(
                host=self.__Host__,
                port=3306,
                user=self.__User__,
                password=self.__Password__,
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
            try:
                self.Cursor.execute(cmd)
                if cmd.strip().lower().startswith(("insert", "update", "delete")):
                    self.Conexao.commit()
                return self.Cursor.fetchall()
            except Error as erro:
                print(f"Erro ao executar comando SQL: {erro}")
                return None
        else:
            print("Conexão não foi iniciada")
            return None

    def Fechar(self):
        if self.Cursor:
            self.Cursor.close()
        if self.Conexao:
            self.Conexao.close()
            print("Conexão ao MySQL encerrada")
