from PIL import Image
import numpy as np

def gerar_histograma(img:Image):
    ## gera o histograma da imagem
    hist = [0] * 256
    ## inicializa o histograma com 0 para todos os níveis de intensidade
    w, h = img.size
    pixels = img.convert("HSV").load()
    for x in range(w):
        for y in range(h):
            hue, s, v = pixels[x, y]
            hist[v] += 1
            ## incrementa o valor do histograma correspondente à intensidade do pixel
    return hist
    

def histEqualization(img, nome_arquivo_saida):
    img = Image.open(img)
    w, h = img.size
    total_pixels = w * h

    histograma = gerar_histograma(img)
    cs = np.cumsum(histograma)

    cs_min = 0
    for i in cs:
        ## encontra o menor valor do histograma
        if i != 0:
            cs_min = i
            break

  

    lookup = [0] * 256
    ## inicializa o novo histograma
    for i in range(256):
        if cs[i] != 0:
            v = (cs[i] - cs_min) * 255
            v = v //(total_pixels - cs_min)
            ## aplica a fórmula de equalização
            if v < 0:
                ## enquadra os valores extrapolantes de volta
                ## para o alcance de 0-255
                v = 0
            if v > 255:
                v = 255
            lookup[i] = v
            ## adiciona o valor equalizado ao histograma final

    pixels = img.convert("L").load()
    output = Image.new("HSV", (w * 2, h))
    output.paste(img.convert("L"))
    ## inicializa a imagem de saída com a imagem original
    ## e um espaço vazio para a imagem equalizada
    img_equalizada = Image.new("HSV", (w, h))
    eq_pixels = img_equalizada.load()
    
    for x in range(w):
        for y in range(h):
            eq_pixels[x, y] = (0, 0, lookup[pixels[x, y]])
            ## converte o valor original do pixel para o valor equalizado
            ## da tabela lookup
    output.paste(img_equalizada, (w, 0))
    if nome_arquivo_saida != "":
        output.convert("RGB").save(rf"\output\{nome_arquivo_saida}.jpg")
    return img_equalizada

histEqualization("./dataset/lena.jpg", "equalizado")
histEqualization("./dataset/lena2.jpg", "equalizado1")
histEqualization("./dataset/bell.jpg", "equalizado2")
## aplicando a equalização em múltiplas imagens de entrada é notavel que
## o efeito realça o intervalo de cor das imagens, tornando suas formas mais visíveis
## mas pode ter um efeito de comprometer a definição da imagem devido à redução 
## da quantidade de valores de intensidade únicos causados pelo histograma equalizado


def normalizar_histograma(hist):
    
    total = sum(hist)

    cumul = [0] * 256
    r = 0
    for i in range(256):
        r += hist[i]
        cumul[i] = r/total
    return cumul

def lookupMatching(cdf_in, cdf_ref):
    ## gera a tabela lookup do histograma da imagem de referência
    lookup = [0] * 256

    for s in range(256):
        bt = 0
        bt_erro = abs(cdf_in[s] - cdf_ref[0])

        for t in range(1, 256):
            erro = abs(cdf_in[s] - cdf_ref[t])
            if erro < bt_erro:
                bt_erro = erro
                bt = t
        lookup[s] = bt
    return lookup


def histMatching(img_in, img_ref, nome_arquivo_saida):
    img_in = Image.open(img_in).convert("L")
    img_ref = Image.open(img_ref).convert("L")

    hist_in = gerar_histograma(img_in)
    hist_ref = gerar_histograma(img_ref)

    cdf_in = normalizar_histograma(hist_in)
    cdf_ref = normalizar_histograma(hist_ref)

    lookup = lookupMatching(cdf_in, cdf_ref)

    pixels = img_in.load()
    w, h = img_in.size
    for x in range(w):
        for y in range(h):
            v = pixels[x, y]
            print(v, lookup[v])
            pixels[x, y] = lookup[v]
            

    return img_in

histMatching("./dataset/eye.png", "./dataset/eyeref.png", "matching")


def recuperar_canyon():
    ## para recuperar a imagem do canyon, foi aplicado o método
    ## histMatching em todos os quadrantes do canyon usando o 
    ## histograma do canyon original como referência
    ## então foram postos lado a lado a foto 
    ## original, os quadrantes antes da equalização
    ## e os quadrantes depois da equalização
    ## é notável como, apesar de ter tornado os quadrantes muito
    ## mais próximos da foto original, ainda são perceptíveis as deformações
    canyon = "./dataset/canyon.png"
    canyon_img = Image.open(canyon)
    w, h = canyon_img.size
    qw = int(w/2)
    qh = int(h/2)

    q1 = "./dataset/part1.png"
    q2 = "./dataset/part2.png"
    q3 = "./dataset/part3.png"
    q4 = "./dataset/part4.png"



    output = Image.new("L", (w * 3, h))
    output.paste(canyon_img)

    output.paste(Image.open(q1), (w, 0))
    output.paste(Image.open(q2), (w + qw, 0))
    output.paste(Image.open(q3), (w, qh))
    output.paste(Image.open(q4), (w + qw, qh))


    eq_q1 = histMatching(q1, canyon, "")
    eq_q2 = histMatching(q2, canyon, "")
    eq_q3 = histMatching(q3, canyon, "")
    eq_q4 = histMatching(q4, canyon, "")

    output.paste(eq_q1, (w * 2, 0))
    output.paste(eq_q2, (w * 2 + qw, 0))
    output.paste(eq_q3, (w * 2, qh))
    output.paste(eq_q4, (w * 2 + qw, qh))
    output.save(rf"\output\rec_canyon.jpg")
    
recuperar_canyon()