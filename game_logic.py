from models import Jogador, Adversario
import random
import time

class Partida:
    """
    Controla a lógica da partida:
    - alterna turnos (jogador e adversário)
    - registra placar
    - verifica fim de jogo (sem empate)
    - aumenta dificuldade e energia máxima a cada vitória
    """

    def __init__(self, jogador: Jogador, nivel=1, rodadas_max=5):
        self.jogador = jogador
        self.nivel = nivel
        self.adversario = self.gerar_adversario(nivel)
        self.rodadas_max = rodadas_max
        self.rodada_atual = 1
        self.turno_jogador = True
        self.mensagem = f"🏁 Nível {nivel}: {self.adversario.nome} entrou em campo!"
        self.finalizada = False

    def gerar_adversario(self, nivel):
        """Cria adversários reais com dificuldade progressiva."""
        lista_adversarios = [
            ("Gabriel Barbosa", 80, 8, 7, 60),
            ("Vinícius Jr", 90, 9, 8, 65),
            ("Rodrygo Goes", 95, 10, 8, 68),
            ("Mohamed Salah", 100, 11, 9, 72),
            ("Kylian Mbappé", 105, 12, 9, 75),
            ("Cristiano Ronaldo", 110, 13, 10, 80),
            ("Lionel Messi", 115, 14, 10, 85),
            ("Ronaldinho Gaúcho", 120, 15, 10, 88),
            ("Zinedine Zidane", 125, 15, 11, 90),
            ("Diego Maradona", 130, 16, 11, 93),
            ("Pelé", 140, 17, 12, 97),  # Chefão final
        ]

        if nivel > len(lista_adversarios):
            nivel = len(lista_adversarios)

        nome, energia, chute, defesa, precisao = lista_adversarios[nivel - 1]

        # Dificuldade aleatória leve (para variar um pouco)
        energia += random.randint(-5, 10)
        chute += random.choice([0, 1])
        defesa += random.choice([0, 1])
        precisao += random.choice([-3, 3])

        return Adversario(nome, energia, chute, defesa, precisao)

    def turno(self, acao=None):
        """Executa o turno do jogador ou do adversário."""
        if self.finalizada:
            return self.mensagem

        if self.rodada_atual > self.rodadas_max:
            return self.fim_partida()

        if self.turno_jogador:
            if acao == "chutar":
                self.mensagem = self.jogador.chutar(self.adversario)
            elif acao == "descansar":
                self.mensagem = self.jogador.descansar()
            else:
                self.mensagem = "Ação inválida!"
            self.turno_jogador = False
        else:
            self.mensagem = self.adversario.agir(self.jogador)
            self.turno_jogador = True
            self.rodada_atual += 1

        return self.mensagem

    def placar(self):
        return f"{self.jogador.nome} {self.jogador.gols} x {self.adversario.gols} {self.adversario.nome}"

    def energia_restante(self):
        return f"⚡ {self.jogador.nome}: {self.jogador.energia} | 🤖 {self.adversario.nome}: {self.adversario.energia}"

    def fim_partida(self):
        """Determina o vencedor — nunca empata."""
        if self.jogador.gols > self.adversario.gols:
            self.finalizada = True
            # ✅ Recupera energia total e aumenta o máximo
            self.jogador.energia_max += 10
            self.jogador.energia = self.jogador.energia_max
            return f"🏆 Você venceu {self.adversario.nome} por {self.placar()}!\nSua energia máxima aumentou para {self.jogador.energia_max}!"
        elif self.adversario.gols > self.jogador.gols:
            self.finalizada = True
            return f"💀 Você foi derrotado por {self.adversario.nome}! Fim de jogo!"
        else:
            vencedor = self.disputa_penaltis()
            self.finalizada = True
            if vencedor == "jogador":
                self.jogador.energia_max += 10
                self.jogador.energia = self.jogador.energia_max
                return f"⚽ Empate no tempo normal!\nNos pênaltis, {self.jogador.nome} venceu {self.adversario.nome}!"
            else:
                return f"💔 Empate no tempo normal!\nNos pênaltis, {self.adversario.nome} venceu {self.jogador.nome}!"

    def disputa_penaltis(self):
        """Decide o vencedor por pênaltis (influenciado pela precisão)."""
        chance_jogador = random.randint(1, 100) + self.jogador.precisao
        chance_adversario = random.randint(1, 100) + self.adversario.precisao
        return "jogador" if chance_jogador >= chance_adversario else "adversario"

    def proximo_nivel(self):
        """Cria uma nova partida com nível mais difícil."""
        if self.finalizada and self.jogador.gols >= self.adversario.gols:
            self.jogador.gols = 0
            return Partida(self.jogador, self.nivel + 1)
        return None
