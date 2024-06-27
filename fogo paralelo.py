import cv2
import numpy as np
import matplotlib.pyplot as plt
import threading
import time

# Caminho da imagem
caminho_imagem = r'c:\\users\\paulo\\downloads\\y.tiff'

# Carrega a imagem
try:
    start_time = time.time()
    imagem = cv2.imread(caminho_imagem)
    print("Imagem carregada com sucesso.")
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")
    imagem = None

def filtrar_pixels(imagem_hsv, mascara_vermelho, mascara_branco, limite_inferior_vermelho, limite_superior_vermelho, limite_inferior_branco, limite_superior_branco):
    mascara_vermelho[:] = cv2.inRange(imagem_hsv, limite_inferior_vermelho, limite_superior_vermelho)
    mascara_branco[:] = cv2.inRange(imagem_hsv, limite_inferior_branco, limite_superior_branco)

if imagem is not None:
    # Número de threads desejado
    num_threads = 8 # Ajuste este valor conforme necessário

    # Divide a imagem em blocos de acordo com o número de threads
    step = imagem.shape[0] // num_threads
    blocos_imagem = [imagem[i * step:(i + 1) * step if i != num_threads - 1 else imagem.shape[0]] for i in range(num_threads)]

    # Converte os blocos para o formato HSV
    blocos_hsv = [cv2.cvtColor(bloco, cv2.COLOR_BGR2HSV) for bloco in blocos_imagem]
    print(f"Imagem convertida para HSV em {time.time() - start_time:.2f} segundos.")

    # Define os limites inferior e superior para a cor vermelha e branca no espaço HSV
    limite_inferior_vermelho = np.array([0, 100, 100])
    limite_superior_vermelho = np.array([10, 255, 255])
    limite_inferior_branco = np.array([0, 0, 200])
    limite_superior_branco = np.array([180, 25, 255])

    # Cria máscaras para vermelho e branco
    mascaras_vermelho = [np.zeros(bloco.shape[:2], dtype=np.uint8) for bloco in blocos_hsv]
    mascaras_branco = [np.zeros(bloco.shape[:2], dtype=np.uint8) for bloco in blocos_hsv]

    # Função para criar e iniciar threads
    def criar_threads(func, blocos_hsv, mascaras_vermelho, mascaras_branco, limite_inferior_vermelho, limite_superior_vermelho, limite_inferior_branco, limite_superior_branco):
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=func, args=(blocos_hsv[i], mascaras_vermelho[i], mascaras_branco[i], limite_inferior_vermelho, limite_superior_vermelho, limite_inferior_branco, limite_superior_branco))
            threads.append(thread)
            thread.start()
        return threads

    # Cria e inicia threads para filtrar pixels vermelhos e brancos
    threads = criar_threads(filtrar_pixels, blocos_hsv, mascaras_vermelho, mascaras_branco, limite_inferior_vermelho, limite_superior_vermelho, limite_inferior_branco, limite_superior_branco)

    # Espera as threads terminarem
    for thread in threads:
        thread.join()
    print(f"Pixels filtrados em {time.time() - start_time:.2f} segundos.")

    # Une as máscaras
    mascara_vermelho = np.vstack(mascaras_vermelho)
    mascara_branco = np.vstack(mascaras_branco)

    # Cria uma cópia da imagem para desenhar contornos
    imagem_contornos = imagem.copy()

    # Desenha contornos vermelhos e brancos na imagem
    imagem_contornos[mascara_vermelho > 0] = [0, 0, 255]
    imagem_contornos[mascara_branco > 0] = [255, 255, 255]

    # Converte a imagem de BGR para RGB para exibição com matplotlib
    imagem_contornos = cv2.cvtColor(imagem_contornos, cv2.COLOR_BGR2RGB)

    # Mostra a imagem resultante usando matplotlib
    plt.imshow(imagem_contornos)
    plt.axis('off')
    plt.show()
    print(f"Imagem exibida em {time.time() - start_time:.2f} segundos.")
