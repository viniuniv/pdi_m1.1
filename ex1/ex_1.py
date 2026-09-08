from PIL import Image

def pixel_maior_frequencia(img):
    ## recebe a path da imagem
    img = Image.open(img).convert("RGB") 
    ## carrega a imagem e a converte para o formato RGB
    pixels = img.load()


    frequencias = {} 
    ## registra a ocorrência de cada valor RGB
    w, h = img.size
    for x in range(w):
        for y in range(h):
            r, g, b = pixels[x, y]
            rgb = (r, g, b) ## gera uma chave RGB com base no pixel da posição
            if not rgb in frequencias:
                ## se o valor RGB ainda não estiver registrado
                ## cria uma nova chave no dicionário e a inicializa como 1
                frequencias[rgb] = 1
            else:
                ## se já estiver registrada, aumenta o valor em 1
                frequencias[rgb] += 1
    maior_freq = max(frequencias, key=frequencias.get)


    # print("Valor RGB com maior incidência: ", rgb, " total de pixels: ", frequencias[maior_freq])
    return maior_freq
    ## retorna o RGB correspondente ao maior valor numérico do dicionário de frequências
    
def mergeImage(fg, bg, nome_saida):
    fundo_fg = pixel_maior_frequencia(fg)
    ## define a cor de fundo com a função desenvolvida no exercício 1

    img = Image.open(fg).convert("RGB")
    w, h = img.size
    pixels = img.load()

    img_bg = Image.open(bg).convert("RGB")

    saida_w, saida_h = img_bg.size;

    if saida_w != w or saida_h != h:
        ## força a imagem de fundo a ter uma resloução 
        ## compatível com fg
        img_bg = img_bg.resize((w, h))

    img_saida = img_bg.load();

    pixels_fg = []
    for x in range(w):
        for y in range(h):
            r, g, b = pixels[x, y]
            rgb = (r, g, b)
            if rgb != fundo_fg:
                ## se o pixel não for da cor de fundo, adiciona-o ao Array pixels_fg
                pixels_fg.append((x, y))

    for x, y in pixels_fg:
        img_saida[x, y] = pixels[x, y]
    
    
    img_bg.save(rf"\output\{nome_saida}.jpg")


mergeImage("./dataset/fg.jpg", "./dataset/bg.jpg", "merge 1")
mergeImage("./dataset/fg.jpg", "./dataset/bg1.jpg", "merge 2")
mergeImage("./dataset/fg1.jpg", "./dataset/part1.png", "merge 3")
