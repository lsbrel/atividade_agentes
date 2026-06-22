from typing import Any
from maspy import Agent, Belief, Goal, gain, pl, tell

class Reserva(Agent):
    # Participante do protocolo contract net
    def __init__(self, agent_name, posicao, rendimento, cansaco):
        super().__init__(agent_name)
        self.posicao = posicao
        self.rendimento = rendimento
        self.cansaco = cansaco
        self.disponivel = True  # se tiver em campo eh false

    # Avalia criterios da vaga
    @pl(gain, Goal("avaliar_vaga", Any))
    def avaliar_vaga(self, src, posicao):
        # só concorre se joga na posicao pedida e ainda esta no banco
        if not self.disponivel or self.posicao != posicao:
            return
        # lance = o quanto ele rende descontando o cansaco
        lance = self.rendimento - self.cansaco
        self.print(f"Posso jogar de {posicao}! Minha proposta: lance {lance}.")
        self.send(src, tell, Belief("proposta", (self.my_name, lance, posicao)))

    # Resultado contract net
    @pl(gain, Goal("entrar_em_campo"))
    def entrar_em_campo(self, src):
        self.disponivel = False
        self.print("Fui escolhido, estou ENTRANDO em campo!")

    @pl(gain, Belief("recusado"))
    def recusado(self, src):
        self.print("Nao fui escolhido dessa vez, sigo no banco.")
