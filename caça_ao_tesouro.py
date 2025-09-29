import pygame
import random
from sys import exit

def main():
    pygame.init()

    preto = (0,0,0)
    branco = (255, 255, 255)
    vermelho = (255, 0, 0)
    verde_grama = (124, 252, 0)
    verde_grama_escuro = (62, 176, 0)
    fonte = pygame.font.SysFont('8-bit Madness', 30)

    musica_fundo = pygame.mixer.music.load('musica_de_fundo.mp3')
    pygame.mixer.music.play(-1)


    tam_celula = 100
    xlinhas = 6

    #tela (são 4 linhas de celulas, e cada celula tem 50 pixeis, o +1 é pra ter um espaço vazio embaixo)
    tela = pygame.display.set_mode( (xlinhas * tam_celula, (xlinhas+1) * tam_celula ))
    pygame.display.set_caption('Treasure Hunt')

    tela.fill(verde_grama)

    #desenho do tabuleiro (coordenada x e y, largura e altura do retangulo, o número no final é a grossura)
    for i in range(xlinhas):
        for j in range(xlinhas):
            pygame.draw.rect(tela, verde_grama_escuro, (tam_celula*i, tam_celula*j, tam_celula, tam_celula), 1)

            grama = pygame.image.load('grama.png')

            grama = pygame.transform.scale(grama, (tam_celula-2, tam_celula-2))

            tela.blit(grama, (tam_celula*i, tam_celula*j))

    #tabuleiro
    conteudo_celula = [[None for i in range(xlinhas)] for j in range(xlinhas)]

    #marcar os tesouros no tabuleiro 
    num_tesouros = 0
    while(num_tesouros < 0.20 * (xlinhas **2) +1):
        i = random.randint(0, xlinhas - 1)
        j = random.randint(0, xlinhas - 1)

        if (conteudo_celula[i][j] == None):
            conteudo_celula[i][j] = 'X'
            num_tesouros += 1

    #marcar o numero de buracos no tabuleiro
    num_buracos = 0
    while num_buracos < 0.10 * (xlinhas**2)+1:
        i = random.randint(0, xlinhas - 1)
        j = random.randint(0, xlinhas-1)

        if conteudo_celula[i][j] == None:
            conteudo_celula[i][j] = 'Y'
            num_buracos += 1

    #calcular o numero de tesouros ao redor da celula

    for i in range(xlinhas):
        for j in range(xlinhas):
                
            if conteudo_celula[i][j] != 'X' and conteudo_celula[i][j] != 'Y':
                tvizinhos = 0

                if i > 0 and conteudo_celula[i-1][j] == 'X':
                    tvizinhos += 1

                if i < xlinhas - 1 and conteudo_celula[i+1][j] == 'X':
                    tvizinhos += 1 

                if j > 0 and conteudo_celula[i][j-1] ==  'X':
                    tvizinhos +=1

                if j < xlinhas - 1 and conteudo_celula[i][j+1] == 'X':
                    tvizinhos += 1

                conteudo_celula[i][j] = str(tvizinhos)

    # matriz para controlar a visualização do conteudo das celulas
    celula_revelada = [[False for i in range(xlinhas)] for j in range(xlinhas)]

        
    jogo_acabou = False
    num_celulas_abertas = 0
    jogador1 = 0
    jogador2 = 0
    turno = 1
    tesouros_abertos = 0


    while True:

        for evento in pygame.event.get():
            if (evento.type == pygame.QUIT):
                pygame.quit()
                exit()                

            # se o jogo terminar as instruções abaixo não serão mais executadas
            if jogo_acabou:
                continue

            # tela so sera atualizada quando tela_mudou for true
            tela_mudou = False

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 :
                # pega as coordenadas do clique para calcular a celula
                mouse_x, mouse_y = evento.pos

                print(f'x = {mouse_x}, y = {mouse_y}')

                celula_x = mouse_x // tam_celula
                celula_y = mouse_y // tam_celula

                # entra no if se a celula foi clicada pela primeira vez
                if not celula_revelada[celula_x][celula_y]:
                    tela_mudou = True
                    num_celulas_abertas += 1
                    celula_revelada[celula_x][celula_y] = True

                    if conteudo_celula[celula_x][celula_y] == 'X':
                        tesouros_abertos += 1
                        if turno == 1:
                            jogador1 += 100
                        else:
                            jogador2 += 100
            

 
                    elif conteudo_celula[celula_x][celula_y] == 'Y':
                        if turno == 1 and jogador1 > 0:
                            jogador1 -= 50
                        elif turno == 2 and jogador2 > 0:
                            jogador2 -= 50

                    if turno == 1:
                        turno = 2
                    else:
                        turno = 1

                    if tesouros_abertos == num_tesouros: 
                        jogo_acabou = True

                        pygame.draw.rect(tela, verde_grama, (0, tam_celula*xlinhas, xlinhas*tam_celula, tam_celula))
                        print(f'jogador um: {jogador1}, jogador dois: {jogador2}')





            if tela_mudou:
                i, j = celula_x, celula_y
                pygame.draw.rect(tela, verde_grama, (0, tam_celula*xlinhas, xlinhas*tam_celula, tam_celula))
                placar = fonte.render(f'jogador 1: {jogador1} | jogador 2: {jogador2}| vez do jogador {turno}', True, preto)
                tela.blit(placar, (tam_celula/2, tam_celula*xlinhas))


                if conteudo_celula[i][j] == 'X':
                    tesouro = pygame.image.load('tesouro1.png')

                    tesouro = pygame.transform.scale(tesouro, (tam_celula - 2, tam_celula - 2))

                    tela.blit(tesouro, (tam_celula*i + 1, tam_celula*j + 1))


                elif conteudo_celula[i][j] == 'Y':
                    buraco = pygame.image.load('buraco1.png')

                    buraco = pygame.transform.scale(buraco, (tam_celula - 2, tam_celula - 2))

                    tela.blit(buraco,(tam_celula*i +1, tam_celula*j +1) )

                else:
                    texto = fonte.render(conteudo_celula[i][j], True, preto)
                    tela.blit(texto, (tam_celula*i + 0.4*tam_celula, tam_celula*j + 0.4*tam_celula))

               
                if jogo_acabou:
                    if jogador1 > jogador2:
                        pygame.draw.rect(tela, verde_grama, (0, tam_celula*xlinhas, xlinhas*tam_celula, tam_celula))
                        texto = fonte.render(f'jogador 1: {jogador1} | jogador 2: {jogador2} | O jogador 1 ganhou.', True, preto)
                        tela.blit(texto, (tam_celula/2, tam_celula*xlinhas))

                    else:
                        pygame.draw.rect(tela, verde_grama, (0, tam_celula*xlinhas, xlinhas*tam_celula, tam_celula))
                        texto = fonte.render(f'jogador 1: {jogador1} | jogador 2: {jogador2} | O jogador 2 ganhou.', True, preto)
                        tela.blit(texto, (tam_celula/2, tam_celula*xlinhas))


            
        pygame.display.update()


if __name__ == '__main__':
    main()