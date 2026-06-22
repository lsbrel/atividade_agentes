from time import sleep
from typing import Any

from maspy import Admin, Agent, Belief, Goal, gain, pl, broadcast, achieve, tell

INTERVALO = 5  # segundos entre cada evento da partida
JANELA_PROPOSTAS = 3  # segundos esperando os reservas mandarem proposta
NUM_LANCES = 12  # quantos eventos a partida gera antes de terminar

class Treinador(Agent):
    """Agente tecnico. Monitora a partida e, quando um titular cai de
    rendimento, abre uma negociacao Contract-Net com os reservas para
    decidir quem entra no lugar.

    Papel no Contract-Net: INICIADOR (manager).
    """

    def __init__(self, agent_name="Treinador"):
        super().__init__(agent_name, read_all_mail=True, max_intentions=10)
        self.propostas = []  # propostas recebidas na negociacao atual
        # objetivo inicial que dispara o loop da partida
        self.add(Goal("apitar_inicio"))

    # ------- Loop da partida (gera os eventos aleatorios) -------
    @pl(gain, Goal("apitar_inicio"))
    def acompanhar_partida(self, src):
        # Roda 12 eventos na partida
        for lance in range(1, NUM_LANCES + 1):
            if not self.running:
                return
            
            sleep(INTERVALO)

            self.print(f"--- minuto {lance * 5}' ---")

            resultado = self.sortear_evento() # qual evento foi escolhido nesse lance

            if resultado is None:
                continue

            nome, posicao, motivo = resultado

            # precisa trocar esse jogador -> abre a negociacao
            self.add(Goal("abrir_vaga", (nome, posicao, motivo)))

        sleep(JANELA_PROPOSTAS + 1)  # deixa a ultima negociacao terminar

        self.print("Apito final! Encerrando a partida.")
        
        Admin().stop_system()

    # ------- Contract-Net: recebe as propostas dos reservas -------
    @pl(gain, Belief("proposta", (Any, Any, Any)))
    def receber_proposta(self, src, dados):
        self.propostas.append(dados)  # dados = (nome, lance, posicao)

    # ------- Contract-Net: CFP + escolha do vencedor -------
    @pl(gain, Goal("abrir_vaga", (Any, Any, Any)))
    def negociar_substituicao(self, src, dados):
        # com 2+ valores o MASPY entrega a tupla inteira em um unico argumento
        jogador, posicao, motivo = dados
        self.print(f"Preciso substituir {jogador} ({motivo}). Abrindo vaga para um {posicao}.")

        # CFP: chama todos os reservas para se candidatarem a vaga
        self.propostas = []
        self.send(broadcast, achieve, Goal("avaliar_vaga", (posicao,)))

        # espera as propostas chegarem
        sleep(JANELA_PROPOSTAS)

        if not self.propostas:
            self.print(f"Nenhum reserva disponivel para {posicao}. Vaga de {jogador} segue aberta.")
            return

        # escolhe o melhor lance
        vencedor, lance, _ = max(self.propostas, key=lambda p: p[1])
        self.print(f"Recebi {len(self.propostas)} proposta(s). Melhor lance: {vencedor.split('_')[0]} ({lance}).")

        # Contract-Net: aceita o vencedor, recusa os demais
        self.send(vencedor, achieve, Goal("entrar_em_campo"))
        for nome, _, _ in self.propostas:
            if nome != vencedor:
                self.send(nome, tell, Belief("recusado"))

        # efetiva a troca no campo
        self.substituir(jogador, vencedor, posicao)
