from skimage import io, color
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np
import time

# Caminho da imagem
caminho_imagem = r'c:\\users\\paulo\\downloads\\a.tiff'

# Carrega a imagem
try:
    start_time = time.time()
    imagem = io.imread(caminho_imagem)
    print("Imagem carregada com sucesso.")
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")
    imagem = None

def filtrar_pixels(imagem_hsv, limite_inferior, limite_superior):
    return ((imagem_hsv >= limite_inferior) & (imagem_hsv <= limite_superior)).all(axis=-1)

if imagem is not None:
    # Reduz o tamanho da imagem para economizar memória
    # Escolha uma dimensão que sua memória suporte, aqui usamos 1/4 do tamanho original
    escala_reducao = 2
    altura_reduzida = imagem.shape[0] // escala_reducao
    largura_reduzida = imagem.shape[1] // escala_reducao
    imagem_reduzida = resize(imagem, (altura_reduzida, largura_reduzida), anti_aliasing=True)
    print(f"Tamanho da imagem reduzido em {time.time() - start_time:.2f} segundos.")

    # Converte a imagem para o formato HSV
    imagem_hsv = color.rgb2hsv(imagem_reduzida)
    print(f"Imagem convertida para HSV em {time.time() - start_time:.2f} segundos.")

    # Define os limites inferior e superior para a cor vermelha e branca no espaço HSV
    limite_inferior_vermelho = np.array([0, 0.4, 0.4])
    limite_superior_vermelho = np.array([0.05, 1.0, 1.0])
    limite_inferior_branco = np.array([0, 0, 0.8])
    limite_superior_branco = np.array([1, 0.2, 1])

    # Filtra pixels vermelhos e brancos
    mascara_vermelho = filtrar_pixels(imagem_hsv, limite_inferior_vermelho, limite_superior_vermelho)
    mascara_branco = filtrar_pixels(imagem_hsv, limite_inferior_branco, limite_superior_branco)
    print(f"Pixels filtrados em {time.time() - start_time:.2f} segundos.")

    # Cria uma cópia da imagem reduzida para desenhar contornos
    imagem_contornos = imagem_reduzida.copy()

    # Desenha contornos vermelhos e brancos na imagem
    imagem_contornos[mascara_vermelho] = [255, 0, 0]
    imagem_contornos[mascara_branco] = [255, 255, 255]

    # Mostra a imagem resultante usando matplotlib
    plt.imshow(imagem_contornos)
    plt.axis('off')
    plt.show()
    print(f"Imagem exibida em {time.time() - start_time:.2f} segundos.")
