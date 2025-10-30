from models import Jogador, Adversario
import random
import time
import numpy as np
from sklearn.linear_model import LinearRegression

class Partida:
    """
    Controla a lógica da partida:
    - alterna turnos (jogador e adversário)
    - registra placar
    - verifica fim de jogo (sem empate)
    - aumenta dificuldade e energia máxima a cada vitória
    - ajusta dinamicamente a dificuldade com Machine Learning
    """

    # 🔹 Modelo global (treinado uma vez)
    modelo_ml = None

    def __init__(self, jogador: Jogador, nivel=1, rodadas_max=5):
        self.jogador = jogador
        self.nivel = nivel
        self.adversario = self.gerar_adversario(nivel)
        self.rodadas_max = rodadas_max
        self.rodada_atual = 1
        self.turno_jogador = True
        self.mensagem = f"🏁 Nível {nivel}: {self.adversario.nome} entrou em campo!"
        self.finalizada = False

        # 🔹 Treina o modelo na inicialização do jogo
        if Partida.modelo_ml is None:
            Partida.modelo_ml = self.treinar_modelo_ml()

    # --------------------------------------------------------------------
    def treinar_modelo_ml(self):
        """Treina um modelo simples de regressão linear com dados simulados."""
        X = []
        y = []

        # Gera dados simulados: [gols, energia_final, nivel]
        for _ in range(300):
            gols = random.randint(0, 6)
            energia_restante = random.randint(0, 150)
            nivel = random.randint(1, 10)
            # Alvo: ajuste de dificuldade (quanto aumentar atributos do adversário)
            ajuste = (gols * 2) + (energia_restante / 20) + (nivel * 0.5) + random.uniform(-2, 2)
            X.append([gols, energia_restante, nivel])
            y.append(ajuste)

        modelo = LinearRegression()
        modelo.fit(np.array(X), np.array(y))
        return modelo
    # --------------------------------------------------------------------

    def gerar_adversario(self, nivel):
        """Cria adversários reais com dificuldade progressiva."""
        lista_adversarios = [
            ("Gabi Gol", 80, 8, 7, 60),
            ("Kaio Jorge", 90, 9, 8, 65),
            ("Rodrygo Goes", 95, 10, 8, 68),
            ("Mohamed Salah", 100, 11, 9, 72),
            ("Vinícius Jr", 105, 12, 9, 75),
            ("Cristiano Ronaldo", 110, 13, 10, 80),
            ("Lionel Messi", 115, 14, 10, 85),
            ("Ronaldinho Gaúcho", 120, 15, 10, 88),
            ("Zinedine Zidane", 125, 15, 11, 90),
            ("Diego Maradona", 130, 16, 11, 93),
            ("Pelé", 140, 17, 12, 97),
        ]

        if nivel > len(lista_adversarios):
            nivel = len(lista_adversarios)

        nome, energia, chute, defesa, precisao = lista_adversarios[nivel - 1]

        # 🔹 Aplica variação leve e ajusta via ML se existir histórico
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
            self.jogador.energia_max += 10
            self.jogador.energia = self.jogador.energia_max
            self.ajustar_dificuldade(vitoria=True)
            return f"🏆 Você venceu {self.adversario.nome} por {self.placar()}!\nDificuldade ajustada automaticamente! ⚙️"
        elif self.adversario.gols > self.jogador.gols:
            self.finalizada = True
            self.ajustar_dificuldade(vitoria=False)
            return f"💀 Você foi derrotado por {self.adversario.nome}! O jogo ficará um pouco mais fácil. 😅"
        else:
            vencedor = self.disputa_penaltis()
            self.finalizada = True
            self.ajustar_dificuldade(vitoria=(vencedor == "jogador"))
            if vencedor == "jogador":
                return f"⚽ Empate no tempo normal!\nNos pênaltis, {self.jogador.nome} venceu {self.adversario.nome}!"
            else:
                return f"💔 Empate no tempo normal!\nNos pênaltis, {self.adversario.nome} venceu {self.jogador.nome}!"

    # --------------------------------------------------------------------
    def ajustar_dificuldade(self, vitoria: bool):
        """Usa ML para ajustar a dificuldade do próximo adversário."""
        if Partida.modelo_ml is None:
            return

        # Entrada do modelo: gols, energia restante, nível atual
        X_novo = np.array([[self.jogador.gols, self.jogador.energia, self.nivel]])
        ajuste = Partida.modelo_ml.predict(X_novo)[0]

        # Se perdeu, inverte o ajuste (deixa mais fácil)
        if not vitoria:
            ajuste *= -0.5

        # Aplica ajuste de dificuldade globalmente
        self.jogador.ajuste_dificuldade = ajuste
        print(f"📊 Ajuste de dificuldade para próxima partida: {ajuste:.2f}")
    # --------------------------------------------------------------------

    def disputa_penaltis(self):
        """Decide o vencedor por pênaltis (influenciado pela precisão)."""
        chance_jogador = random.randint(1, 100) + self.jogador.precisao
        chance_adversario = random.randint(1, 100) + self.adversario.precisao
        return "jogador" if chance_jogador >= chance_adversario else "adversario"

    def proximo_nivel(self):
        """Cria uma nova partida com nível mais difícil, ajustando conforme ML."""
        if self.finalizada and self.jogador.gols >= self.adversario.gols:
            self.jogador.gols = 0
            nova_partida = Partida(self.jogador, self.nivel + 1)

            # Se o modelo gerou ajuste, aplica no novo adversário
            ajuste = getattr(self.jogador, "ajuste_dificuldade", 0)
            if ajuste != 0:
                nova_partida.adversario.energia += ajuste
                nova_partida.adversario.chute += int(ajuste / 5)
                nova_partida.adversario.defesa += int(ajuste / 5)

            return nova_partida
        return None
