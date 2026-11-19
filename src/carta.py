class Carta:
    """Representa uma carta do jogo da memória."""

    def __init__(self, identificador, categoria, texto):
        """Guarda o par da carta, seu tipo e o texto mostrado ao jogador."""
        self.identificador = identificador
        self.categoria = categoria
        self.texto = texto
        self.revelada = False
        self.encontrada = False

    def revelar(self):
        """Deixa a carta visível."""
        self.revelada = True

    def ocultar(self):
        """Vira a carta para baixo, caso ela ainda não tenha sido encontrada."""
        if not self.encontrada:
            self.revelada = False

    def combina_com(self, outra_carta):
        """Retorna True se as cartas formam uma situação e seu princípio."""
        mesmo_par = self.identificador == outra_carta.identificador
        categorias_diferentes = self.categoria != outra_carta.categoria

        return mesmo_par and categorias_diferentes

    def marcar_encontrada(self):
        """Marca a carta como parte de um par encontrado."""
        self.encontrada = True
        self.revelada = True