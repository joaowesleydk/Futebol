from models import Jogador, Adversario
import random
from utils.helpers import tocar_som, tocar_musica_fundo, parar_musica_fundo

class Partida:
    def __init__(self, jogador: Jogador, nivel=1, rodadas_max=5):
        self.jogador = jogador
        self.nivel = max(1, int(nivel))
        self.rodadas_max = max(1, int(rodadas_max))
        self.rodada_atual = 1
        self.turno_jogador = True
        self.finalizada = False
        self.mensagem = ""
        
        if not hasattr(self.jogador, "inventario") or self.jogador.inventario is None:
            self.jogador.inventario = {}

        self.adversario = self.gerar_adversario(self.nivel)
        self.mensagem = f"🏁 Nível {self.nivel}: {self.adversario.nome} entrou em campo!"

        try:
            tocar_musica_fundo("tema_batalha.mp3")
        except Exception:
            pass

    def gerar_adversario(self, nivel):
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

        if nivel > len(referencia):
            extra = nivel - len(referencia)
            energia += int(extra * 6 + random.randint(-3, 6))
            chute += int(extra * 0.5)
            defesa += int(extra * 0.4)
            precisao += int(extra * 0.6)

        energia += random.randint(-5, 8)
        chute += random.choice([0, 1])
        defesa += random.choice([0, 1])
        precisao += random.choice([-3, 3])

        energia = max(20, energia)
        chute = max(1, chute)
        defesa = max(1, defesa)
        precisao = min(100, max(10, precisao))

        return Adversario(nome, energia, chute, defesa, precisao)

    def turno(self, acao=None):
        if self.finalizada:
            return self.mensagem

        if self.rodada_atual > self.rodadas_max:
            return self.fim_partida()

        som_a_tocar = None
        
        if self.turno_jogador:
            if acao == "chutar":
                resultado = self.jogador.chutar(self.adversario)
                self.mensagem = resultado
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

            self.turno_jogador = False
        else:
            resultado_adv = self.adversario.agir(self.jogador)
            self.mensagem = resultado_adv
            if "gol" in resultado_adv.lower() or "marcou" in resultado_adv.lower():
                som_a_tocar = "adv_gol.mp3"
            elif "errou" in resultado_adv.lower():
                som_a_tocar = "erro.mp3"
            else:
                som_a_tocar = "adv_chute.mp3"

            self.turno_jogador = True
            self.rodada_atual += 1

        try:
            if som_a_tocar:
                tocar_som(som_a_tocar)
        except Exception:
            print(f"[WARN] falha ao tocar som {som_a_tocar}")

        return self.mensagem

    def placar(self):
        return f"{self.jogador.nome} {self.jogador.gols} x {self.adversario.gols} {self.adversario.nome}"

    def energia_restante(self):
        return f"⚡ {self.jogador.nome}: {self.jogador.energia} | 🤖 {self.adversario.nome}: {self.adversario.energia}"

    def fim_partida(self):
        try:
            parar_musica_fundo()
        except Exception:
            pass

        if self.jogador.gols > self.adversario.gols:
            try:
                tocar_som("vitoria.mp3")
            except Exception:
                pass
            self.finalizada = True
            self.jogador.energia_max = getattr(self.jogador, "energia_max", self.jogador.energia) + 10
            self.jogador.energia = self.jogador.energia_max
            item, raridade = self.baú_premio()
            return (f"🏆 Você venceu {self.adversario.nome} por {self.placar()}!\n"
                    f"🎁 Baú desbloqueado: {item} ({raridade})\nDificuldade ajustada automaticamente! ⚙️")
        elif self.adversario.gols > self.jogador.gols:
            try:
                tocar_som("derrota.mp3")
            except Exception:
                pass
            self.finalizada = True
            return f"💀 Você foi derrotado por {self.adversario.nome}! O jogo ficará um pouco mais fácil. 😅"
        else:
            vencedor = self.disputa_penaltis()
            self.finalizada = True
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

    def disputa_penaltis(self):
        try:
            tocar_som("dado.mp3")
        except Exception:
            pass

        chance_jogador = random.randint(1, 100) + getattr(self.jogador, "precisao", 0)
        chance_adversario = random.randint(1, 100) + getattr(self.adversario, "precisao", 0)
        return "jogador" if chance_jogador >= chance_adversario else "adversario"

    def baú_premio(self):
        itens = [
            ("⚡ Energético", "comum"),
            ("🔥 Chute Especial", "raro"),
            ("🛡️ Escudo", "comum"),
            ("💎 Escudo Divino", "lendário")
        ]

        roll = random.random()
        if roll < 0.6:
            item, raridade = itens[0]
        elif roll < 0.85:
            item, raridade = itens[1]
        elif roll < 0.98:
            item, raridade = itens[2]
        else:
            item, raridade = itens[3]

        inv = getattr(self.jogador, "inventario", None)
        if inv is None:
            self.jogador.inventario = {}
            inv = self.jogador.inventario

        inv[item] = inv.get(item, 0) + 1
        print(f"🎁 Baú: {item} ({raridade}) adicionado ao inventário.")
        return item, raridade

    def proximo_nivel(self):
        if not self.finalizada:
            return None

        self.jogador.gols = 0
        novo_nivel = self.nivel + 1
        nova_partida = Partida(self.jogador, nivel=novo_nivel, rodadas_max=self.rodadas_max)
        return nova_partida