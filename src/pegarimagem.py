import pyautogui as auto
import time
import os
import cv2
import numpy as np
from PIL import Image
from conexao import Conexao


pasta_destino = r"C:\Users\LEONARDOMEDEIROSHUNT\Desktop\Projeto_Integrador\dados\img"
os.makedirs(pasta_destino, exist_ok=True)

def obter_nomes_do_banco():
    conexao = Conexao(db='herbario', host='127.0.0.1')
    if conexao.Iniciar():
        resultado = conexao.Executar("SELECT nome FROM plantas")
        conexao.Fechar()
        return [linha[0] for linha in resultado if linha]
    else:
        print("Erro ao conectar ao banco.")
        return []

def detectar_e_salvar_area_verde(contador, nome):
    screenshot = auto.screenshot()
    frame = np.array(screenshot)
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        print("Nenhuma área verde detectada.")
        return

    maior = max(contornos, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(maior)

    centro_x, centro_y = x + w // 2, y + h // 2
    auto.moveTo(centro_x, centro_y)
    auto.click()
    time.sleep(2)

    planta = frame[y:y+h, x:x+w]
    imagem = Image.fromarray(planta)
    caminho = os.path.join(pasta_destino, f"{contador}.jpg")
    imagem.save(caminho)
    print(f"Imagem salva em: {caminho}")
    time.sleep(2)

def buscar_e_salvar_imagem(nome, contador):
    print(f"\nBuscando imagem de {nome}...")

    auto.press("win")
    time.sleep(0.5)
    auto.write("chrome")
    auto.press("enter")
    time.sleep(3)

    auto.write("https://www.google.com/imghp")
    auto.press("enter")
    time.sleep(3)

    auto.write(f"{nome} planta medicinal")
    auto.press("enter")
    time.sleep(4)

    detectar_e_salvar_area_verde(contador, nome)
 
    auto.hotkey("alt", "f4")
    time.sleep(1)

if __name__ == "__main__":
    nomes = obter_nomes_do_banco()
    
    
    if not nomes:
        print("Nenhum nome encontrado no banco.")
        exit()

    for i, nome in enumerate(nomes, start=1):
        buscar_e_salvar_imagem(nome, i)
    
    print("\nProcesso concluído!")