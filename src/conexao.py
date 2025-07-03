import pymysql
from pymysql import Error
def conecta():
    try:
        conexao = pymysql.connect(
            host= '127.0.0.1',
            port=3306,
            user='root',
            password='',
            database='herbario'
        )
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM plantas")
        
        resultado = cursor.fetchall()
        for tabela in resultado:
            print(tabela)
    except Error as erro:
        print(f"Não foi possível conectar ao MySQL: {erro}")
    
    finally:
        conexao.close()
        print("Conexão ao MySQL encerrada")

conecta()