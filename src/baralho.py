import random

from src.carta import Carta


class Baralho:
    """Cria e organiza as cartas de uma partida."""

    def __init__(self):
        """Monta quatro pares contextualizados e embaralha as cartas."""
        self._cartas = []

        pares = [
            (
                1,
                "Um assistente inventa um artigo científico e um DOI para um trabalho.",
                "Confira a referência em uma base acadêmica antes de citá-la.",
                "Modelos de IA podem apresentar fontes inexistentes com segurança. "
                "Confirme a referência em uma fonte confiável.",
            ),
            (
                2,
                "Um aplicativo de IA pede acesso aos contatos para criar um avatar.",
                "Negue permissões que não sejam necessárias para a função.",
                "Compartilhar dados sem necessidade aumenta o risco à privacidade. "
                "Permita somente o acesso indispensável.",
            ),
            (
                3,
                "Uma IA de recrutamento reduz a nota de pessoas com pausas na carreira.",
                "Investigue vieses e peça revisão humana das avaliações.",
                "Dados históricos podem reproduzir desigualdades. "
                "Verifique os impactos e permita revisão.",
            ),
            (
                4,
                "Uma voz clonada do chefe pede uma transferência urgente.",
                "Confirme o pedido por um canal conhecido antes de agir.",
                "Uma voz convincente pode ser falsificada. "
                "A verificação independente ajuda a evitar golpes.",
            ),
        ]

        for identificador, situacao, principio, explicacao in pares:
            self._cartas.append(
                Carta(identificador, "Caso", situacao, explicacao)
            )
            self._cartas.append(
                Carta(identificador, "Ação responsável", principio, explicacao)
            )

        self.embaralhar()

    def embaralhar(self):
        """Altera a ordem das cartas aleatoriamente."""
        random.shuffle(self._cartas)

    def obter_cartas(self):
        """Retorna a lista de cartas do baralho."""
        return list(self._cartas)
