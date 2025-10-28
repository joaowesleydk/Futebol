# models/adversario.py
class Adversario:
    def __init__(self, nome, nivel):
        self.nome = nome
        self.nivel = nivel
        self.energia_max = 100
        self.energia = 100
        self.status_buff = {"defesa_reduzida": False}
