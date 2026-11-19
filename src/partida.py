from src.baralho import Baralho


class Partida:
    """Controla as regras e o progresso de uma partida."""

    def __init__(self):
        """Cria um baralho e prepara os contadores da partida."""
        self._baralho = Baralho()
        self._cartas = self._baralho.obter_cartas()
        self._primeira_carta = None
        self._segunda_carta = None
        self._tentativas = 0
        self._erros = 0
        self._pares_encontrados = 0

    def selecionar_carta(self, indice):
        """Revela a carta selecionada e informa o resultado da jogada."""
        if indice < 0 or indice >= len(self._cartas):
            return "invalida"

        if self._segunda_carta is not None:
            return "aguardando"

        carta = self._cartas[indice]

        if carta.revelada or carta.encontrada:
            return "invalida"

        carta.revelar()

        if self._primeira_carta is None:
            self._primeira_carta = carta
            return "primeira"

        self._segunda_carta = carta
        self._tentativas += 1

        if self._primeira_carta.combina_com(self._segunda_carta):
            self._primeira_carta.marcar_encontrada()
            self._segunda_carta.marcar_encontrada()
            self._pares_encontrados += 1
            self._limpar_selecao()
            return "acerto"

        self._erros += 1
        return "erro"

    def ocultar_par_incorreto(self):
        """Vira para baixo as duas cartas após uma combinação incorreta."""
        if self._primeira_carta is not None:
            self._primeira_carta.ocultar()

        if self._segunda_carta is not None:
            self._segunda_carta.ocultar()

        self._limpar_selecao()

    def _limpar_selecao(self):
        """Limpa as referências às cartas da jogada atual."""
        self._primeira_carta = None
        self._segunda_carta = None

    def jogador_venceu(self):
        """Indica se todos os pares do baralho foram encontrados."""
        return self._pares_encontrados == len(self._cartas) // 2

    def obter_cartas(self):
        """Retorna as cartas da partida para a interface desenhar."""
        return list(self._cartas)

    def obter_tentativas(self):
        """Retorna a quantidade de tentativas realizadas."""
        return self._tentativas

    def obter_erros(self):
        """Retorna a quantidade de combinações incorretas."""
        return self._erros

    def obter_pares_encontrados(self):
        """Retorna quantos pares corretos o jogador encontrou."""
        return self._pares_encontrados

    ### obter_Cartas() devolve uma cópia da lista de, mas as cartas continuam sendo os mesmo objetos.Assim a interface poderá desenhá--las e consultar se estão reveladas ou encontradas, as regras permanece na classe Partida!!!!
    