from PIL import Image
import numpy as np
import colorsys

q = 8
def quantificar(i):
    ## aplica a quantificação nos pixels já negativados
    return np.round(i * (q - 1)/255) * (255/(q-1))

def negativo_imagem(img, int_maxima, nome_arquivo_saida):
    img = Image.open(img).convert("RGB")

    w, h = img.size
    pixels = img.load()

    mult_intensidade = int_maxima/255

    for x in range(w):
        for y in range(h):
            r, g, b = pixels[x, y]
            ## inverte os pixels e aplica a quantificação
            r = int(quantificar((255 - r) * mult_intensidade))
            g = int(quantificar((255 - g) * mult_intensidade))
            b = int(quantificar((255 - b) * mult_intensidade))

            pixels[x, y] = (r, g, b);

    img.save(rf"\output\{nome_arquivo_saida}.jpg")


negativo_imagem("./dataset/lena.jpg", 255, "negativo")

def tranformacao_gama(img, y_gama, nome_arquivo_saida):
    img = Image.open(img).convert("RGB")
    w, h = img.size
    pixels = img.convert("HSV").load()
    output_img = img.load()

    for x in range(w):
        for y in range(h):
            hue, s, v = pixels[x, y]
            v_normalizado = v/255
            novo_v = v_normalizado ** y_gama
            novo_v = int(novo_v * 255)

            novo_rgb = colorsys.hsv_to_rgb(hue, s, novo_v)
            output_img[x, y] = novo_rgb

    img.save(rf"\output\{nome_arquivo_saida}.png")


for i in np.arange(0, 1, .1):
    tranformacao_gama("./dataset/gamma-corr.png", i, "gamma_0"+str(int(i * 10)))
    ## ao aplicar diferentes valores Y para transformações de gama,
    ## é notável que, quanto menor o valor Y, mais esmaecida 
    ## e de menor contraste se torna a imagem
