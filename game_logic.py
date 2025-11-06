from models import Jogador, Adversario
import random
import numpy as np
from sklearn.linear_model import LinearRegression
from utils.helpers import tocar_som, tocar_musica_fundo, parar_musica_fundo

class Partida:
    """
    Lógica da partida — refatorada:
    - treina um modelo ML simples (regressão linear) para ajustar dificuldade
    - garante sons consistentes
    - retorna o item ganho em baú para a GUI exibir/animar em tela cheia
    - aplica proteções (clamp) ao ajustar atributos do adversário
    """

    modelo_ml = None
    _RANDOM_SEED = 42

    def __init__(self, jogador: Jogador, nivel=1, rodadas_max=5):
        self.jogador = jogador
        self.nivel = max(1, int(nivel))
        self.rodadas_max = max(1, int(rodadas_max))
        self.rodada_atual = 1
        self.turno_jogador = True
        self.finalizada = False
        self.mensagem = ""
        # garante inventário no jogador (compatibilidade com modelos antigos)
        if not hasattr(self.jogador, "inventario") or self.jogador.inventario is None:
            self.jogador.inventario = {}

        # gera adversário
        self.adversario = self.gerar_adversario(self.nivel)
        self.mensagem = f"🏁 Nível {self.nivel}: {self.adversario.nome} entrou em campo!"

        # inicia música de fundo (se quiser que Partida controle música)
        try:
            tocar_musica_fundo("tema_batalha.mp3")
        except Exception:
            pass

        # treina modelo ML uma única vez (lazy)
        if Partida.modelo_ml is None:
            Partida.modelo_ml = self._treinar_modelo_ml()

    # ---------------- ML ----------------
    def _treinar_modelo_ml(self):
        """Treina um modelo simples e determinístico com dados simulados."""
        rng = np.random.RandomState(self._RANDOM_SEED)
        X = []
        y = []
        for _ in range(400):
            gols = int(rng.randint(0, 7))
            energia_restante = int(rng.randint(0, 151))
            nivel = int(rng.randint(1, 11))
            ajuste = (gols * 2) + (energia_restante / 20.0) + (nivel * 0.5) + rng.uniform(-2, 2)
            X.append([gols, energia_restante, nivel])
            y.append(float(ajuste))

        modelo = LinearRegression()
        modelo.fit(np.array(X), np.array(y))
        return modelo

    # ---------------- adversário ----------------
    def gerar_adversario(self, nivel):
        """
        Gera adversário baseado em uma lista de referências.
        Se o nível exceder a lista, escala os atributos gradualmente.
        """
        referencia = [
            ("Gabi Gol", 80, 8, 7, 60),
            ("Cristiano Ronaldo", 110, 13, 10, 80),
            ("Lionel Messi", 115, 14, 10, 85),
            ("Ronaldinho Gaúcho", 120, 15, 10, 88),
            ("Diego Maradona", 130, 16, 11, 93),
            ("Pelé", 140, 17, 12, 97),
        ]

        base_index = min(len(referencia) - 1, max(0, int(nivel) - 1))
        nome, energia, chute, defesa, precisao = referencia[base_index]

        # se nível maior que lista, faz escala suave por nível extra
        if nivel > len(referencia):
            extra = nivel - len(referencia)
            energia += int(extra * 6 + random.randint(-3, 6))
            chute += int(extra * 0.5)
            defesa += int(extra * 0.4)
            precisao += int(extra * 0.6)

        # pequenas variações aleatórias
        energia += random.randint(-5, 8)
        chute += random.choice([0, 1])
        defesa += random.choice([0, 1])
        precisao += random.choice([-3, 3])

        # garante limites razoáveis
        energia = max(20, energia)
        chute = max(1, chute)
        defesa = max(1, defesa)
        precisao = min(100, max(10, precisao))

        return Adversario(nome, energia, chute, defesa, precisao)

    # ---------------- turno principal ----------------
    def turno(self, acao=None):
        """
        Executa a ação do jogador (quando for o turno dele) ou faz o turno do adversário.
        Retorna a mensagem resultante e toca sons apropriados.
        """
        if self.finalizada:
            return self.mensagem

        if self.rodada_atual > self.rodadas_max:
            return self.fim_partida()

        som_a_tocar = None
        # turno do jogador
        if self.turno_jogador:
            if acao == "chutar":
                # jogador.chutar deve retornar string informativa e aplicar efeitos internos (gols/energia)
                resultado = self.jogador.chutar(self.adversario)
                self.mensagem = resultado
                # decide som com base na mensagem retornada
                if "errou" in resultado.lower() or "perdeu" in resultado.lower():
                    som_a_tocar = "erro.mp3"
                elif "gol" in resultado.lower() or "golaço" in resultado.lower():
                    som_a_tocar = "chute_gol.mp3"
                else:
                    som_a_tocar = "chute.mp3"
            elif acao == "descansar":
                self.mensagem = self.jogador.descansar()
                som_a_tocar = "descanso.mp3"
            else:
                self.mensagem = "Ação inválida!"
                som_a_tocar = "erro.mp3"

            # jogador realizou ação -> passa turno
            self.turno_jogador = False

        # turno do adversário
        else:
            resultado_adv = self.adversario.agir(self.jogador)
            self.mensagem = resultado_adv
            # som do adversário
            if "gol" in resultado_adv.lower() or "marcou" in resultado_adv.lower():
                som_a_tocar = "adv_gol.mp3"
            elif "errou" in resultado_adv.lower():
                som_a_tocar = "erro.mp3"
            else:
                som_a_tocar = "adv_chute.mp3"

            self.turno_jogador = True
            self.rodada_atual += 1

        # toca som decidido (tratamento seguro)
        try:
            if som_a_tocar:
                tocar_som(som_a_tocar)
        except Exception:
            # não devemos quebrar o fluxo por causa de áudio
            print(f"[WARN] falha ao tocar som {som_a_tocar}")

        return self.mensagem

    # ---------------- utilitários ----------------
    def placar(self):
        return f"{self.jogador.nome} {self.jogador.gols} x {self.adversario.gols} {self.adversario.nome}"

    def energia_restante(self):
        return f"⚡ {self.jogador.nome}: {self.jogador.energia} | 🤖 {self.adversario.nome}: {self.adversario.energia}"

    # ---------------- fim de partida ----------------
    def fim_partida(self):
        """Determina vencedor e executa rotinas de pós-jogo."""
        try:
            parar_musica_fundo()
        except Exception:
            pass

        # jogador vence
        if self.jogador.gols > self.adversario.gols:
            try:
                tocar_som("vitoria.mp3")
            except Exception:
                pass
            self.finalizada = True
            # melhora atributo do jogador (salva energia máxima)
            self.jogador.energia_max = getattr(self.jogador, "energia_max", self.jogador.energia) + 10
            self.jogador.energia = self.jogador.energia_max
            # ajusta dificuldade por ML
            self.ajustar_dificuldade(vitoria=True)
            # retorna item do baú (GUI pode exibir)
            item, raridade = self.baú_premio()
            return (f"🏆 Você venceu {self.adversario.nome} por {self.placar()}!\n"
                    f"🎁 Baú desbloqueado: {item} ({raridade})\nDificuldade ajustada automaticamente! ⚙️")
        # adversário vence
        elif self.adversario.gols > self.jogador.gols:
            try:
                tocar_som("derrota.mp3")
            except Exception:
                pass
            self.finalizada = True
            self.ajustar_dificuldade(vitoria=False)
            return f"💀 Você foi derrotado por {self.adversario.nome}! O jogo ficará um pouco mais fácil. 😅"
        # empate -> pênaltis
        else:
            vencedor = self.disputa_penaltis()
            self.finalizada = True
            self.ajustar_dificuldade(vitoria=(vencedor == "jogador"))
            if vencedor == "jogador":
                try:
                    tocar_som("vitoria.mp3")
                except Exception:
                    pass
                item, raridade = self.baú_premio()
                return (f"⚽ Empate no tempo normal!\nNos pênaltis, {self.jogador.nome} venceu {self.adversario.nome}!\n"
                        f"🎁 Baú desbloqueado: {item} ({raridade})")
            else:
                try:
                    tocar_som("derrota.mp3")
                except Exception:
                    pass
                return f"💔 Empate no tempo normal!\nNos pênaltis, {self.adversario.nome} venceu {self.jogador.nome}!"

    # ---------------- ajustar dificuldade (ML) ----------------
    def ajustar_dificuldade(self, vitoria: bool):
        """Usa o modelo ML para sugerir um ajuste; aplica clamps e salva no jogador."""
        if Partida.modelo_ml is None:
            return

        try:
            X_novo = np.array([[getattr(self.jogador, "gols", 0),
                                max(0, getattr(self.jogador, "energia", 0)),
                                self.nivel]], dtype=float)
            ajuste = float(Partida.modelo_ml.predict(X_novo)[0])
        except Exception as e:
            print("[WARN] ML predict falhou:", e)
            ajuste = 0.0

        # se perdeu, reduz (tornando adversários um pouco mais fracos)
        if not vitoria:
            ajuste *= -0.5

        # clamp para evitar ajustes extremos
        ajuste = max(-30.0, min(ajuste, 60.0))
        self.jogador.ajuste_dificuldade = ajuste
        print(f"📊 Ajuste de dificuldade calculado: {ajuste:.2f}")
        return ajuste

    # ---------------- pênaltis ----------------
    def disputa_penaltis(self):
        """Decide o vencedor por pênaltis (influenciado pela precisão)."""
        try:
            tocar_som("dado.mp3")
        except Exception:
            pass

        chance_jogador = random.randint(1, 100) + getattr(self.jogador, "precisao", 0)
        chance_adversario = random.randint(1, 100) + getattr(self.adversario, "precisao", 0)
        return "jogador" if chance_jogador >= chance_adversario else "adversario"

    # ---------------- baú / recompensas ----------------
    def baú_premio(self):
        """
        Gera um item de recompensa, adiciona ao inventário do jogador e retorna (item, raridade).
        Não toca som nem mostra popup — retorna para a GUI decidir como exibir (som/fullscreen).
        """
        itens = [
            ("⚡ Energético", "comum"),
            ("🔥 Chute Especial", "raro"),
            ("🛡️ Escudo", "comum"),
            ("💎 Escudo Divino", "lendário")
        ]

        # chance ponderada por raridade
        roll = random.random()
        if roll < 0.6:
            item, raridade = itens[0]  # energético (comum)
        elif roll < 0.85:
            item, raridade = itens[1]  # chute especial (raro)
        elif roll < 0.98:
            item, raridade = itens[2]  # escudo (comum)
        else:
            item, raridade = itens[3]  # lendário

        # adiciona ao inventário do jogador (seguro)
        inv = getattr(self.jogador, "inventario", None)
        if inv is None:
            self.jogador.inventario = {}
            inv = self.jogador.inventario

        inv[item] = inv.get(item, 0) + 1

        # retorna para que a GUI possa tocar som + exibir em fullscreen
        print(f"🎁 Baú: {item} ({raridade}) adicionado ao inventário.")
        return item, raridade

    # ---------------- criar próxima partida ----------------
    def proximo_nivel(self):
        """
        Cria uma nova Partida no nível seguinte, aplicando ajuste_dificuldade se existir.
        Retorna uma nova Partida ou None.
        """
        if not self.finalizada:
            return None

        # zera gols do jogador (prepara para próxima partida)
        self.jogador.gols = 0
        novo_nivel = self.nivel + 1
        nova_partida = Partida(self.jogador, nivel=novo_nivel, rodadas_max=self.rodadas_max)

        ajuste = getattr(self.jogador, "ajuste_dificuldade", 0.0)
        if ajuste:
            # aplica ajuste aos atributos do adversário de forma segura e com clamp
            nova_partida.adversario.energia = int(max(20, nova_partida.adversario.energia + ajuste))
            nova_partida.adversario.chute = int(max(1, nova_partida.adversario.chute + round(ajuste / 6.0)))
            nova_partida.adversario.defesa = int(max(1, nova_partida.adversario.defesa + round(ajuste / 8.0)))

        return nova_partida
