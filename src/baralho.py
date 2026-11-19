import random

from src.carta import Carta


class Baralho:
    """Cria e organiza as cartas de uma partida."""

    def __init__(self):
        """Monta quatro pares temáticos e embaralha as cartas."""
        self._cartas = []

        pares = [
            (1, "IA inventou uma fonte", "Verifique fontes e evidências"),
            (2, "Sistema avaliou alguém injustamente", "Revise vieses e peça supervisão"),
            (3, "IA pediu dados pessoais", "Proteja informações privadas"),
            (4, "Usei texto gerado no trabalho", "Declare o uso e confira o conteúdo"),
        ]

        for identificador, situacao, principio in pares:
            self._cartas.append(
                Carta(identificador, "Situação", situacao)
            )
            self._cartas.append(
                Carta(identificador, "Princípio", principio)
            )

        self.embaralhar()

    def embaralhar(self):
        """Altera a ordem das cartas aleatoriamente."""
        random.shuffle(self._cartas)

    def obter_cartas(self):
        """Retorna a lista de cartas do baralho."""
        return list(self._cartas)