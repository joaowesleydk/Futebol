import random
import time
from utils.helpers import rolar_dado, tocar_som


class Batalha:
    def __init__(self, jogador, adversario):
        self.jogador = jogador
        self.adversario = adversario
        self.turno_atual = "jogador"

    # ---------------------------
    # Execução de um turno
    # ---------------------------
    def turno(self, acao_jogador):
        logs = []

        # Jogador age primeiro
        logs.append(f"{self.jogador.nome} decide {acao_jogador.upper()}!")

        if acao_jogador == "chutar":
            logs.append(self.acao_chutar(self.jogador, self.adversario))
        elif acao_jogador == "defender":
            logs.append(self.acao_defender(self.jogador))
        elif acao_jogador == "boost":
            logs.append(self.acao_boost(self.jogador))
        else:
            logs.append("⚠️ Ação inválida!")

        # Verifica se o jogo acabou
        if self.terminou():
            return "\n".join(logs)

        time.sleep(1)

        # Adversário joga
        acao_adv = random.choice(["chutar", "defender", "boost"])
        logs.append(f"{self.adversario.nome} decide {acao_adv.upper()}!")

        if acao_adv == "chutar":
            logs.append(self.acao_chutar(self.adversario, self.jogador))
        elif acao_adv == "defender":
            logs.append(self.acao_defender(self.adversario))
        elif acao_adv == "boost":
            logs.append(self.acao_boost(self.adversario))

        return "\n".join(logs)

    # ---------------------------
    # Ações do jogo
    # ---------------------------
    def acao_chutar(self, atacante, defensor):
        dado = rolar_dado(20)
        dano_base = 15 + atacante.nivel * 3
        if dado >= 18:
            dano = dano_base * 2
            texto = f"💥 GOLAAAAÇO! {atacante.nome} acerta um chute incrível!"
            tocar_som("assets/sons/chute_forte.wav", 0.6)
        elif dado >= 10:
            dano = dano_base
            texto = f"⚽ {atacante.nome} acerta o gol com um belo chute!"
            tocar_som("assets/sons/chute.wav", 0.5)
        else:
            dano = 0
            texto = f"😬 {atacante.nome} chutou pra fora!"
            tocar_som("assets/sons/erro.wav", 0.5)

        # Defesa pode reduzir dano
        if defensor.buffs.get("defesa_turns", 0) > 0:
            dano = int(dano * 0.5)
            texto += f" 🧤 {defensor.nome} defendeu parte do chute!"

        defensor.energia = max(0, defensor.energia - dano)
        atacante.buffs["boost_turns"] = max(0, atacante.buffs.get("boost_turns", 0) - 1)
        defensor.buffs["defesa_turns"] = max(0, defensor.buffs.get("defesa_turns", 0) - 1)

        return texto

    def acao_defender(self, jogador):
        jogador.buffs["defesa_turns"] = 2
        tocar_som("assets/sons/defesa.wav", 0.6)
        return f"🧤 {jogador.nome} prepara uma defesa sólida!"

    def acao_boost(self, jogador):
        if jogador.buffs.get("boost_turns", 0) > 0:
            return f"⚡ {jogador.nome} já está com energia máxima!"
        jogador.buffs["boost_turns"] = 3
        tocar_som("assets/sons/boost.wav", 0.6)
        return f"💨 {jogador.nome} ativa o BOOST! Seus chutes ficam mais fortes!"

    # ---------------------------
    # Verificações
    # ---------------------------
    def terminou(self):
        return self.jogador.energia <= 0 or self.adversario.energia <= 0

    def vencedor(self):
        if self.jogador.energia > 0 and self.adversario.energia <= 0:
            return self.jogador.nome
        elif self.adversario.energia > 0 and self.jogador.energia <= 0:
            return self.adversario.nome
        return None
