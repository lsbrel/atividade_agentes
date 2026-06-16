from agents.treinador import Treinador
from agents.reserva import Reserva
from environments.campo_futebol import CampoFutebol
from maspy import Admin


def main():
    campo = CampoFutebol()

    treinador = Treinador()

    # banco de reserva varios agentes
    reservas = [
        Reserva("Endrick", posicao="ATA", rendimento=80, cansaco=5),
        Reserva("Rodrygo", posicao="ATA", rendimento=78, cansaco=10),
        Reserva("Bruno",   posicao="MEI", rendimento=72, cansaco=15),
        Reserva("Bremer",  posicao="ZAG", rendimento=74, cansaco=8),
    ]

    # conecta todos os agentes ao ambiente
    Admin().connect_to(agents=[treinador, *reservas], targets=campo)
    Admin().start_system()


if __name__ == "__main__":
    main()
