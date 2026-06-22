import random

from maspy import Environment

# Eventos do sorteio
EVENTOS = [
    ("queda_rendimento", "baixo rendimento"),
    ("cansaco", "muito cansado"),
    ("lesao", "lesionado"),
]

class CampoFutebol(Environment):
    def __init__(self):
        super().__init__()

        self.titulares = {
            "Neymar":     {"posicao": "ATA", "cansaco": 30, "rendimento": 75},
            "Messi":      {"posicao": "ATA", "cansaco": 20, "rendimento": 85},
            "Casemiro":   {"posicao": "MEI", "cansaco": 40, "rendimento": 70},
            "Marquinhos": {"posicao": "ZAG", "cansaco": 25, "rendimento": 65},
        }

        self.print("Partida iniciada com 11 em campo (titulares monitorados):")

        for nome, s in self.titulares.items():
            self.print(f"   {nome} ({s['posicao']}) - rendimento {s['rendimento']}, cansaco {s['cansaco']}")

    def sortear_evento(self, agt):
        """Sorteia um evento aleatorio e o aplica a um titular."""
        if not self.titulares:
            return None

        nome = random.choice(list(self.titulares))
        status = self.titulares[nome]
        tipo, descricao = random.choice(EVENTOS)

        if tipo == "queda_rendimento":
            status["rendimento"] = max(0, status["rendimento"] - random.randint(10, 30))
        elif tipo == "cansaco":
            status["cansaco"] = min(100, status["cansaco"] + random.randint(10, 30))
        elif tipo == "lesao":
            status["rendimento"] = 0  # lesionado nao tem mais condicao de jogo

        self.print(f"EVENTO: {nome} ficou {descricao} " f"(rendimento {status['rendimento']}, cansaco {status['cansaco']})")

        # Regras para decidir substituição
        precisa = (tipo == "lesao" or status["rendimento"] < 40 or status["cansaco"] > 80)

        if precisa:
            # deleta o titular para ele não sofrer novos eventos
            del self.titulares[nome]
            return (nome, status["posicao"], descricao)
        return None

    def substituir(self, agt, sai, entra, posicao):
        nome = entra.split("_")[0] # jogador entrando

        # o reserva entra zerado de cansaço e bom rendimento
        self.titulares[nome] = {"posicao": posicao, "cansaco": 0, "rendimento": 75}
        self.print(f"SUBSTITUIÇÃO EFETUADA: sai {sai}, entra {nome} ({posicao})")
