import random

class Jogador:
    def __init__(self, nome: str, energia: int, chute: int, defesa: int, precisao: int):
        self.nome = nome
        self.energia = energia
        self.energia_max = energia
        self.chute = chute
        self.defesa = defesa
        self.precisao = precisao
        self.gols = 0

    def chutar(self, adversario):
        """Tenta fazer um gol no adversário."""
        if self.energia <= 0:
            return f"{self.nome} está exausto e não conseguiu chutar!"

        chance_gol = random.randint(1, 100)
        forca_chute = self.chute + random.randint(-3, 3)
        defesa_adversario = adversario.defesa + random.randint(-3, 3)

        self.energia = max(0, self.energia - 10)  # gasta energia ao chutar

        if chance_gol <= self.precisao and forca_chute > defesa_adversario:
            self.gols += 1
            return f"⚽ {self.nome} chutou com força e marcou um GOL!"
        else:
            return f"❌ {self.nome} chutou, mas o goleiro defendeu!"

    def descansar(self):
        """Recupera energia."""
        ganho = random.randint(8, 15)
        self.energia = min(self.energia + ganho, self.energia_max)
        return f"💤 {self.nome} descansou e recuperou {ganho} de energia!"

    def esta_exausto(self):
        return self.energia <= 0


class Adversario:
    def __init__(self, nome: str, energia: int, chute: int, defesa: int, precisao: int):
        self.nome = nome
        self.energia = energia
        self.energia_max = energia
        self.chute = chute
        self.defesa = defesa
        self.precisao = precisao
        self.gols = 0

    def agir(self, jogador):
        """Decide automaticamente o que o adversário vai fazer (chutar ou descansar)."""
        if self.energia < 15:
            return self.descansar()
        else:
            return self.chutar(jogador)

    def chutar(self, jogador):
        if self.energia <= 0:
            return f"{self.nome} está exausto e não conseguiu chutar!"

        chance_gol = random.randint(1, 100)
        forca_chute = self.chute + random.randint(-3, 3)
        defesa_jogador = jogador.defesa + random.randint(-3, 3)

        self.energia = max(0, self.energia - 10)

        if chance_gol <= self.precisao and forca_chute > defesa_jogador:
            self.gols += 1
            return f"🥅 {self.nome} chutou e marcou um gol!"
        else:
            return f"🧤 {self.nome} chutou, mas {jogador.nome} defendeu!"

    def descansar(self):
        ganho = random.randint(8, 15)
        self.energia = min(self.energia + ganho, self.energia_max)
        return f"😴 {self.nome} descansou e recuperou {ganho} de energia!"
