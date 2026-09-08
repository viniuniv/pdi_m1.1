from PIL import Image

def convoluir_matriz(img:Image):
    matriz = [
        [0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0]
    ] 
    ## utilizando a matriz laplaceana, as transições de cores são acentuadas
    ## e outro detalhes são removidos


    w, h = img.size
    output = Image.new("L", img.size)
    pixels = img.convert("L").load()
    out_pixels = output.load()
    divisor = sum([sum(r) for r in matriz])
    if divisor == 0:
        divisor = 1

    for x in range(1, w - 1):
        for y in range(1, h - 1):
            total = 0

            for x1 in range(-1, 2):
                for y1 in range(-1, 2):
                    total += pixels[x + x1, y + y1] * matriz[x1][y1]

            out_pixels[x, y] = total//divisor
    return output


def convolucao(img, nome_arq_saida):
    img = Image.open(img)
    w,h = img.size
    convoluido = convoluir_matriz(img)

    output = Image.new("L", (w*2, h))
    output.paste(img)
    output.paste(convoluido, (w, 0))
    output.save(rf"\output\{nome_arq_saida}.jpg")
    ## ao aplicar o filtro convolutivo em várias imagens, 
    ## é mostrado que o filtro remove qualquer outro detalhe da imagem, deixando apenas
    ## as linhas de transição entre tons claros e escuros
    
    


convolucao("./dataset/box.png", "linha_box")
convolucao("./dataset/lena.jpg", "bordas_lena")