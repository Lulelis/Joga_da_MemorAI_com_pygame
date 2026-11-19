import pygame

from src.config import ALTURA_TELA, FPS, LARGURA_TELA
from src.partida import Partida

COR_FUNDO = (24, 32, 48)
COR_CARTA_FECHADA = (54, 75, 110)
COR_CARTA_ABERTA = (236, 239, 244)
COR_PAR_ENCONTRADO = (67, 135, 105)
COR_TEXTO = (245, 245, 245)
COR_TEXTO_CARTA = (30, 38, 52)
COR_DESTAQUE = (255, 205, 92)
PAUSA_ERRO_MS = 900
TEMPO_PARTIDA_SEGUNDOS = 120


def quebrar_texto(texto, fonte, largura_maxima):
    """Divide um texto em linhas que cabem na largura indicada."""
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        tentativa = f"{linha_atual} {palavra}".strip()

        if fonte.size(tentativa)[0] <= largura_maxima:
            linha_atual = tentativa
        else:
            if linha_atual:
                linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    return linhas


def desenhar_carta(tela, carta, retangulo, fonte, fonte_pequena):
    """Desenha uma carta fechada ou mostra seu conteúdo quando revelada."""
    if carta.encontrada:
        cor = COR_PAR_ENCONTRADO
    elif carta.revelada:
        cor = COR_CARTA_ABERTA
    else:
        cor = COR_CARTA_FECHADA

    pygame.draw.rect(tela, cor, retangulo, border_radius=12)
    pygame.draw.rect(
        tela,
        COR_DESTAQUE,
        retangulo,
        width=2,
        border_radius=12,
    )

    if not carta.revelada and not carta.encontrada:
        texto = fonte.render("MemorAI", True, COR_TEXTO)
        tela.blit(texto, texto.get_rect(center=retangulo.center))
        return

    cor_texto = COR_TEXTO if carta.encontrada else COR_TEXTO_CARTA
    categoria = fonte_pequena.render(carta.categoria, True, cor_texto)
    tela.blit(categoria, (retangulo.x + 10, retangulo.y + 12))

    linhas = quebrar_texto(carta.texto, fonte_pequena, retangulo.width - 20)
    posicao_y = retangulo.y + 50

    for linha in linhas:
        texto = fonte_pequena.render(linha, True, cor_texto)
        tela.blit(texto, (retangulo.x + 10, posicao_y))
        posicao_y += texto.get_height() + 4


def executar_jogo():
    """Abre a janela e executa a primeira versão gráfica do MemorAI."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("MemorAI | Central de Auditoria")

    relogio = pygame.time.Clock()
    fonte = pygame.font.Font(None, 30)
    fonte_pequena = pygame.font.Font(None, 23)

    partida = Partida()
    cartas = partida.obter_cartas()

    largura_carta = 170
    altura_carta = 165
    espacamento_x = 20
    espacamento_y = 22
    margem_x = 20
    inicio_y = 155

    retangulos = []

    for indice in range(len(cartas)):
        coluna = indice % 4
        linha = indice // 4

        x = margem_x + coluna * (largura_carta + espacamento_x)
        y = inicio_y + linha * (altura_carta + espacamento_y)

        retangulos.append(
            pygame.Rect(x, y, largura_carta, altura_carta)
        )

    inicio_partida = pygame.time.get_ticks()
    instante_erro = None
    rodando = True

    while rodando:
        agora = pygame.time.get_ticks()
        tempo_decorrido = (agora - inicio_partida) // 1000
        tempo_restante = max(
            0,
            TEMPO_PARTIDA_SEGUNDOS - tempo_decorrido,
        )

        if instante_erro is not None:
            if agora - instante_erro >= PAUSA_ERRO_MS:
                partida.ocultar_par_incorreto()
                instante_erro = None

        if tempo_restante == 0 and not partida.jogador_venceu():
            rodando = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if instante_erro is None and not partida.jogador_venceu():
                    for indice, retangulo in enumerate(retangulos):
                        if retangulo.collidepoint(evento.pos):
                            resultado = partida.selecionar_carta(indice)

                            if resultado == "erro":
                                instante_erro = pygame.time.get_ticks()

                            break

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

        tela.fill(COR_FUNDO)

        titulo = fonte.render(
            "MemorAI | Missão: auditar casos de IA",
            True,
            COR_TEXTO,
        )
        tela.blit(titulo, (20, 20))

        instrucoes = fonte_pequena.render(
            "Encontre a solução responsável para cada problema.",
            True,
            COR_DESTAQUE,
        )
        tela.blit(instrucoes, (20, 65))

        status = (
            f"Tempo: {tempo_restante}s   "
            f"Pares: {partida.obter_pares_encontrados()}/4   "
            f"Tentativas: {partida.obter_tentativas()}   "
            f"Erros: {partida.obter_erros()}"
        )
        texto_status = fonte_pequena.render(status, True, COR_TEXTO)
        tela.blit(texto_status, (20, 105))

        for indice, carta in enumerate(cartas):
            desenhar_carta(
                tela,
                carta,
                retangulos[indice],
                fonte,
                fonte_pequena,
            )

        if partida.jogador_venceu():
            mensagem = fonte.render(
                "Auditoria concluída! Pressione Esc para sair.",
                True,
                COR_DESTAQUE,
            )
            tela.blit(mensagem, (20, 555))

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()