from PIL import Image, ImageDraw, ImageFont


def sub_laplace(img:Image):
    output = Image.new("L", img.size)
    out_pixels = output.load()

    w, h = img.size
    img = img.convert("L")
    pixels = img.load()
    ## filtro de aguçamento: 
    ##  0 -1  0
    ## -1  4 -1
    ##  0 -1  0
    
    for x in range(1, w -1):
        ## itera por todos os pixels
        ## menos os que estão nos cantos da imagem
        for y in range(1, h - 1): 
            laplace = (
                4 * pixels[x, y] ## pixel alvo
                - pixels[x - 1, y] ## pixel à esquerda
                - pixels[x + 1, y] ## pixel à direita
                - pixels[x, y-1] ## pixel acima
                - pixels[x, y+1] ## pixel abaixo
            )
            intensidade_final = pixels[x, y] - laplace
            intensidade_final = max(0, min(255, intensidade_final))
            out_pixels[x, y] = intensidade_final
    return output

def box_blur(img):
    ## efeito de box-blur de 2 pixels de alcance para 
    ## gerar a máscara a ser subtraída no unsharp masking
    w, h = img.size
    output = img.convert("L")
    pixels = output.load()

    for x in range(2, w - 2):
        for y in range(2, h - 2):
            total = 0

            for x1 in range(-2, 3):
                for y1 in range(-2, 3):
                    total += pixels[x + x1, y + y1]

            pixels[x, y] = total//25
    return output

def gerar_matriz_unsharp(img, target):
    w, h = img.size
    output = img.convert("L")
    pixels = output.load()

    target_pixels = target.convert("L").load()
    matriz = [[0 for _ in range(w)] for _ in range(h)]
    for x in range(w):
        for y in range(h):
            matriz[x][y] = pixels[x, y] - target_pixels[x, y]
    return matriz

def unsharp_masking(img, matriz, k=.5):
    w, h = img.size
    output = img.convert("L")
    pixels = output.load()


    for x in range(w):
        for y in range(h):
            pixels[x, y] = int(pixels[x, y] + k * (pixels[x, y] - matriz[x][y]))
    return output


def comp_laplace_unsharp(img, nome_arquivo_saida):
    img = Image.open(img)
    w, h = img.size
    output = Image.new("L", (w*2, h*2))
    ## cria uma imagem de saída com espaço para a imagem original
    ## e as duas versões modificadas a serem comparadas
    filtrada_laplace = sub_laplace(img)

    filtrada_blur = box_blur(img)
    matriz = gerar_matriz_unsharp(img, filtrada_blur)
    filtrada_mask = unsharp_masking(img, matriz)

    output.paste(img)
    output.paste(filtrada_laplace, (w, 0))
    output.paste(filtrada_mask, (w, h))
    output.paste(filtrada_blur, (0, h))
    ## adiciona as amostras à imagem de saída

    draw = ImageDraw.Draw(output)
    font = ImageFont.truetype("arial.ttf", 48)
    draw.text((0, 10), "NORMAL", fill="black", font=font)
    draw.text((w, 10), "LAPLACE", fill="black", font=font)
    draw.text((0, h+10), "MASCARA BLUR", fill="black", font=font)
    draw.text((w, h+10), "UNSHARP MASKING", fill="black", font=font)
    ## ao aplicar os diferentes filtros, enquanto a imagem de saída não ficou
    ## tão visualmente similar nos filtros laplace e unsharp masking,
    ## ambas produziram o mesmo efeito de realçamento das bordas dos objetos da imagem

    output.save(rf"\output\{nome_arquivo_saida}.jpg")
    
comp_laplace_unsharp("./dataset/lena.jpg", "comparacao")