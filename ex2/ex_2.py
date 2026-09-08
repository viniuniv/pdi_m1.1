from PIL import Image
import colorsys

def intervaloContraste(img):
    ## retorna um array [min, max]
    ## correspondendo ao menor e ao maior valor de intensidade dos pixels da imagem
    
    max = 0
    min = 255
    ## inicializa os valores min e max
    w, h = img.size;
    pixels = img.load();
    for x in range(w):
        for y in range(h):
            hue, s, v = pixels[x, y];
            if v > max:
                max = v
            if v < min:
                min = v


    return [min, max]
    
def clamp(n, min_val, max_val):
    return int(max(min_val, min(n, max_val)))


def linContrastStretching(img, a, b, nome_arquivo_saida):
    ## a = intensidade mínima alvo
    ## b = intensidade máxima alvo
    img_file = Image.open(img);
    w, h = img_file.size

    altura_barra_cores = int(h/20)
    ## define a altura das barras de cores de modo a sempre ocuparem
    ## a mesma fração do espaço na imagem


    output = Image.new("RGB", (w * 2, h + altura_barra_cores),(255, 255, 255))
    ## gera a imagem de saída, com espaço para a imagem antes, a 
    ## imagem depois e as barras de cores

    img = img_file.convert("HSV")
    minv, maxv = intervaloContraste(img)
    ## calcula os valores mínimo e máximo 
    ## de intensidade da imagem original
    


    output.paste(img, (0, altura_barra_cores))
    ## cola a imagem original na saída

    output_img = output.load()
    ## prepara a imagem para receber pixels gerados por código

    passo_barra_antes = (maxv - minv)/w
    passo_barra_depois = (b - a)/w
    ## passo no valor de intensidade dos pixels das barras

    for x in range(w):
        rgb_antes = colorsys.hsv_to_rgb(0, 0, int(passo_barra_antes * x));
        rgb_depois = colorsys.hsv_to_rgb(0, 0, int(passo_barra_depois * x))
        for y in range(altura_barra_cores):
            ## gera as barra lado-a-lado
            output_img[x, y] = rgb_antes;
            output_img[x + w, y] = rgb_depois


    pixels = img.load()
    for x in range(w):
        for y in range(h):
            hue, s, v = pixels[x, y]
            normalized = (v-minv)/(maxv-minv);
            ## normaliza o valor de intensidade
            new_v = a + normalized * (b-a)
            ## aplica o desvio para a nova curva
            rgb = colorsys.hsv_to_rgb(hue, s, int(new_v))
            ## converte o valor para RGB
            output_img[x + w, y + altura_barra_cores] = rgb
            ## coloca o pixel na imagem de saída
            ## ao lado da imagem original

    output.save(rf"\output\{nome_arquivo_saida}.jpg")
    return img

## TESTE COM DIFERENTES AMOSTRAS
## imagens disponíveis no arquivo output

linContrastStretching("./dataset/lena.jpg", 30, 160, "lena1")
## na amostra 1, o contraste é reduzido devido aos valores a e b
## colocados serem mais próximos dos valores minv e maxv encontrados na imagem ./dataset/lena.jpg

linContrastStretching("./dataset/lena.jpg", 0, 255, "lena1_alto_contraste")
## na amostra 2, o contraste é ampliado para o máximo possível pelo método linear,

linContrastStretching("./dataset/lena1.jpg", 20, 100, "lena2")
## na amostra 3, onde a imagem de entrada é de máximo contraste, 
## o contraste é drasticamente reduzido, e como os pixels originais
## são apenas de intensidade 0 ou 255, todos são transformados
## diretamente nos valores a e b, respectivamente
