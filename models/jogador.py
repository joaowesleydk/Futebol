# models/jogador.py
from utils.helpers import tocar_som

class Jogador:
    def __init__(self, nome, selecao="Brasil"):
        self.nome = nome
        self.selecao = selecao
        self.nivel = 3
        self.xp = 0
        self.energia_max = 100
        self.energia = 100
        self.fama = 0
        self.trofeus = 0
        self.itens = {"Curativo": 2, "Boost": 1}
        self.buffs = {"boost_turns": 0, "defesa_turns": 0}

    def descansar(self):
        self.energia = self.energia_max
        tocar_som("assets/sons/torcida.mp3", 0.4)

    def ganhar_xp(self, amount):
        self.xp += amount
        while self.xp >= 100:
            self.xp -= 100
            self.nivel += 1
            self.energia = min(self.energia_max, self.energia + 20)
            tocar_som("assets/sons/vitoria.wav", 0.5)

    def usar_item(self, item):
        if self.itens.get(item, 0) <= 0:
            return False
        self.itens[item] -= 1
        if item == "Curativo":
            self.energia = min(self.energia_max, self.energia + 40)
        elif item == "Boost":
            self.buffs["boost_turns"] = 3
        return True
