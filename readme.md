# Atividade: Agentes

# Proposta
Sistema multi-agentes (SMA) escrito com a biblioteca **MASPY-ml** (desenvolvida por
alunos de mestrado e IC da UTFPR-PG). O domínio é a **gestão em tempo real de uma
equipe de futebol durante a partida**: a cada poucos segundos um evento aleatório
altera o status de um atleta (cansaço, queda de rendimento ou lesão) e, quando
necessário, os agentes **negociam uma substituição** de forma totalmente autônoma
usando o protocolo **Contract-Net**.

## Objetivos
1. Acompanhar quais atletas estão em campo e seus status (rendimento e cansaço).
2. Receber, em tempo real, eventos que mudam a condição dos atletas
   (cansado, baixo rendimento, lesionado).
3. Tomar a decisão técnica cabível — substituir o atleta — escolhendo o reserva
   por meio de uma negociação Contract-Net, sem nenhuma intervenção humana.

## Tipos de agentes
1. **Treinador** (`src/agents/treinador.py`) — agente técnico. Acompanha a partida,
   detecta quem precisa sair e atua como **iniciador** do Contract-Net (abre a vaga,
   recebe as propostas, escolhe o melhor reserva e efetua a troca).
2. **Reserva** (`src/agents/reserva.py`) — vários agentes no banco rodando ao mesmo
   tempo. Cada um atua como **participante** do Contract-Net: ao receber a chamada
   (CFP), decide se concorre à vaga e envia sua proposta (lance).

O **ambiente** `CampoFutebol` (`src/environments/campo_futebol.py`) guarda os
titulares e sorteia os eventos da partida.

## O protocolo Contract-Net (resumo)
1. **CFP** – o Treinador anuncia a vaga (posição) para todos os reservas.
2. **Propostas** – cada reserva apto à posição responde com um lance
   (`rendimento - cansaço`).
3. **Escolha** – o Treinador seleciona o maior lance.
4. **Aceite/Recusa** – aceita o vencedor e recusa os demais.
5. **Execução** – o reserva escolhido entra em campo.

# Bibliotecas
* MASPY-ml: https://github.com/laca-is/MASPY

# Como rodar (Windows / PowerShell)
> Requer Python 3.12+ instalado (testado com Python 3.13).

```powershell
# 1. Criar o ambiente virtual
python -m venv .venv

# 2. Ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1
#   Se der erro de "execução de scripts desabilitada", rode uma vez:
#   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Executar o projeto
python src\main.py
```

# Como rodar (Linux / macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

> A partida dura `NUM_LANCES` lances (definido em `treinador.py`) e então o sistema
> encerra sozinho. Para interromper antes, use `Ctrl+C`.

# Como rodar via Docker
* Requer Docker e Docker Compose instalados (https://www.docker.com/).

```bash
docker compose up
```
