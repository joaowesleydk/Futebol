import tkinter as tk
from tkinter import messagebox
import random
from models import Jogador
from game_logic import Partida


class FIFA_GUI_PLUS:
    def __init__(self, root):
        self.root = root
        self.root.title("⚽ FIFA RPG Cartoon Edition ⚽")
        self.root.geometry("800x600")
        self.root.configure(bg="#0b132b")

        self.partida = None
        self.jogador = None
        self.turno_jogador = True
        self.itens = {"⚡ Energético": 2, "🔥 Chute Especial": 1, "🛡️ Escudo": 1}
        self.defendendo = False
        self.nivel = 1

        self.tela_inicial()

    # ======== TELA INICIAL ========
    def tela_inicial(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#1c2541", bd=4, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=300)

        titulo = tk.Label(frame, text="⚽ FIFA RPG Cartoon Edition ⚽",
                          font=("Comic Sans MS", 20, "bold"),
                          fg="#f0a500", bg="#1c2541")
        titulo.pack(pady=20)

        lbl_nome = tk.Label(frame, text="Digite seu nome:",
                            font=("Comic Sans MS", 14),
                            fg="white", bg="#1c2541")
        lbl_nome.pack(pady=10)

        self.nome_entry = tk.Entry(frame, font=("Comic Sans MS", 14), justify="center")
        self.nome_entry.pack(pady=5)

        btn_iniciar = tk.Button(frame, text="Começar Jogo ⚡",
                                font=("Comic Sans MS", 14, "bold"),
                                bg="#f0a500", fg="black",
                                relief="raised", bd=3,
                                command=self.iniciar_jogo)
        btn_iniciar.pack(pady=20)

        self.root.bind("<Return>", lambda event: self.iniciar_jogo())

    # ======== INICIAR PARTIDA (modificado) ========
    def iniciar_jogo(self):
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Digite seu nome para começar!")
            return

        # Cria jogador
        self.jogador = Jogador(nome, energia=100, chute=10, defesa=8, precisao=70)
        # Cria partida usando a classe Partida
        self.partida = Partida(self.jogador, nivel=self.nivel)
        # Pega adversário da partida
        self.adversario = self.partida.adversario
        self.adversario_nome = self.adversario.nome

        # Inicializa HP e energia
        self.jogador_hp = self.jogador.energia
        self.jogador_energia = self.jogador.energia
        self.adversario_hp = self.adversario.energia
        self.adversario_energia = self.adversario.energia

        # Define HP máximo para as barras
        self.hp_max = max(self.jogador_hp, self.adversario_hp)

        # Inicia a tela do jogo
        self.tela_jogo()

    # ======== TELA DO JOGO ========
    def tela_jogo(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.frame_jogo = tk.Frame(self.root, bg="#0b132b")
        self.frame_jogo.pack(fill="both", expand=True)

        self.lbl_status = tk.Label(self.frame_jogo, text=f"⚔️ Nível {self.nivel} - Partida iniciada!",
                                   font=("Comic Sans MS", 16, "bold"),
                                   fg="#f0a500", bg="#0b132b")
        self.lbl_status.pack(pady=20)

        # ===== Barras =====
        self.criar_barras()

        # ===== Dado =====
        self.label_dado = tk.Label(self.frame_jogo, text="🎲", font=("Arial", 30),
                                   bg="#0b132b", fg="white")
        self.label_dado.pack(pady=20)

        # ===== Botões =====
        frame_botoes = tk.Frame(self.frame_jogo, bg="#0b132b")
        frame_botoes.pack(pady=20)

        self.btn_chutar = tk.Button(frame_botoes, text="⚽ Chutar", font=("Comic Sans MS", 14, "bold"),
                                    bg="#f0a500", fg="black", width=12,
                                    command=lambda: self.jogar_turno("chutar"))
        self.btn_chutar.grid(row=0, column=0, padx=15)

        self.btn_defender = tk.Button(frame_botoes, text="🛡️ Defender", font=("Comic Sans MS", 14, "bold"),
                                      bg="#5bc0be", fg="black", width=12,
                                      command=lambda: self.jogar_turno("defender"))
        self.btn_defender.grid(row=0, column=1, padx=15)

        self.btn_item = tk.Button(frame_botoes, text="🎒 Itens", font=("Comic Sans MS", 14, "bold"),
                                  bg="#f0a500", fg="black", width=12,
                                  command=self.usar_item)
        self.btn_item.grid(row=0, column=2, padx=15)

    # ======== BARRAS ========
    def criar_barras(self):
        # Jogador
        frame_jogador = tk.Frame(self.frame_jogo, bg="#0b132b")
        frame_jogador.pack(pady=(0, 10))

        self.lbl_hp_jogador = tk.Label(frame_jogador,
                                       text=f"{self.jogador.nome} ❤️ {self.jogador_hp}/{self.hp_max}",
                                       font=("Comic Sans MS", 14, "bold"),
                                       fg="#5bc0be", bg="#0b132b")
        self.lbl_hp_jogador.pack()

        self.canvas_hp_jogador = tk.Canvas(frame_jogador, width=300, height=20, bg="gray")
        self.canvas_hp_jogador.pack(pady=3)
        self.barra_hp_jogador = self.canvas_hp_jogador.create_rectangle(0, 0, 300, 20, fill="#00ff66")

        frame_energia_j = tk.Frame(frame_jogador, bg="#0b132b")
        frame_energia_j.pack(pady=(0, 10))
        tk.Label(frame_energia_j, text="⚡", font=("Comic Sans MS", 14, "bold"),
                 fg="#0099ff", bg="#0b132b").grid(row=0, column=0, padx=5)
        self.canvas_energy_jogador = tk.Canvas(frame_energia_j, width=240, height=6, bg="gray", highlightthickness=0)
        self.canvas_energy_jogador.grid(row=0, column=1)
        self.barra_energy_jogador = self.canvas_energy_jogador.create_rectangle(0, 0, 240, 6, fill="#0099ff")

        # Adversário
        frame_adv = tk.Frame(self.frame_jogo, bg="#0b132b")
        frame_adv.pack(pady=(10, 10))

        self.lbl_hp_adversario = tk.Label(frame_adv,
                                          text=f"{self.adversario_nome} ❤️ {self.adversario_hp}/{self.hp_max}",
                                          font=("Comic Sans MS", 14, "bold"),
                                          fg="#ff5f40", bg="#0b132b")
        self.lbl_hp_adversario.pack()

        self.canvas_hp_adversario = tk.Canvas(frame_adv, width=300, height=20, bg="gray")
        self.canvas_hp_adversario.pack(pady=3)
        self.barra_hp_adversario = self.canvas_hp_adversario.create_rectangle(0, 0, 300, 20, fill="#ff4040")

        frame_energia_a = tk.Frame(frame_adv, bg="#0b132b")
        frame_energia_a.pack(pady=(0, 15))
        tk.Label(frame_energia_a, text="⚡", font=("Comic Sans MS", 14, "bold"),
                 fg="#0099ff", bg="#0b132b").grid(row=0, column=0, padx=5)
        self.canvas_energy_adversario = tk.Canvas(frame_energia_a, width=240, height=6, bg="gray", highlightthickness=0)
        self.canvas_energy_adversario.grid(row=0, column=1)
        self.barra_energy_adversario = self.canvas_energy_adversario.create_rectangle(0, 0, 240, 6, fill="#0099ff")

    # ======== ANIMAÇÃO ENERGIA ========
    def animar_barra_energia(self, canvas, barra, cor="#0099ff"):
        def brilho():
            canvas.itemconfig(barra, fill="#66ccff")
            canvas.after(150, lambda: canvas.itemconfig(barra, fill=cor))
        brilho()

    # ======== ROLAR DADO ========
    def rolar_dado(self, callback):
        resultado_final = random.randint(1, 20)
        def animar(cont=0):
            if cont < 15:
                self.label_dado.config(text=f"🎲 {random.randint(1,20)}")
                self.root.after(60, animar, cont + 1)
            else:
                self.label_dado.config(text=f"🎲 {resultado_final}")
                callback(resultado_final)
        animar()

    # ======== AÇÕES DO JOGADOR ========
    def jogar_turno(self, acao):
        if not self.turno_jogador:
            return
        self.turno_jogador = False
        for btn in [self.btn_chutar, self.btn_defender, self.btn_item]:
            btn.config(state="disabled")
        self.rolar_dado(lambda dado: self.resolver_jogador(acao, dado))

    def resolver_jogador(self, acao, dado):
        self.defendendo = False
        if acao == "chutar":
            self.jogador_energia = max(0, self.jogador_energia - 10)
            dano = 0
            if dado == 20:
                msg = "🌀 GOL DE BICICLETA! Golpe crítico!"
                dano = 40
            elif dado >= 15:
                msg = "🚀 Chute fortíssimo! Golaço!"
                dano = 30
            elif dado >= 10:
                msg = "⚽ Chute certeiro! Gol normal."
                dano = 20
            elif dado >= 5:
                msg = "🥅 Bateu fraco, o goleiro quase pegou!"
                dano = 10
            else:
                msg = "❌ Errou feio! Chutou pra fora."
                dano = 0
            self.adversario_hp = max(self.adversario_hp - dano, 0)
            self.lbl_status.config(text=f"{msg} (D20: {dado})")
        elif acao == "defender":
            self.defendendo = True
            self.lbl_status.config(text="🛡️ Você se prepara para defender o próximo ataque!")
        self.atualizar_interface()
        if self.adversario_hp <= 0:
            self.encerrar_partida(derrota=False)
        else:
            self.root.after(1500, self.turno_adversario)

    # ======== TURNO DO ADVERSÁRIO ========
    def turno_adversario(self):
        self.lbl_status.config(text="🤖 O adversário está atacando...")
        self.rolar_dado(self.resolver_adversario)

    def resolver_adversario(self, dado):
        dano = 0
        if dado == 20:
            msg = "💥 O adversário deu uma bicicleta MONSTRUOSA!"
            dano = 35
        elif dado >= 15:
            msg = "🔥 O adversário chutou no ângulo!"
            dano = 25
        elif dado >= 10:
            msg = "⚽ O adversário marcou um gol normal."
            dano = 15
        elif dado >= 5:
            msg = "😅 A bola desviou e entrou devagarzinho..."
            dano = 8
        else:
            msg = "🙅‍♂️ Você defendeu o chute!"
            dano = 0
        if self.defendendo:
            dano = int(dano * 0.5)
            msg += " 🛡️ Defesa eficaz!"
        self.adversario_energia = max(0, self.adversario_energia - 10)
        self.jogador_hp = max(self.jogador_hp - dano, 0)
        self.lbl_status.config(text=f"{msg} (D20: {dado})")
        self.atualizar_interface()
        if self.jogador_hp <= 0:
            self.encerrar_partida(derrota=True)
        else:
            self.root.after(1500, self.liberar_turno)

    def liberar_turno(self):
        self.turno_jogador = True
        for btn in [self.btn_chutar, self.btn_defender, self.btn_item]:
            btn.config(state="normal")
        self.lbl_status.config(text="⚽ Sua vez!")

    # ======== ITENS ========
    def usar_item(self):
        itens_disponiveis = [f"{k} ({v}x)" for k, v in self.itens.items() if v > 0]
        if not itens_disponiveis:
            messagebox.showinfo("🎒 Mochila", "Você não tem itens disponíveis!")
            return
        item_nome = random.choice(list(self.itens.keys()))
        if item_nome == "⚡ Energético":
            self.jogador_hp = min(self.jogador_hp + 30, self.hp_max)
            self.lbl_status.config(text="⚡ Você bebeu um energético! +30 HP!")
        elif item_nome == "🔥 Chute Especial":
            self.adversario_hp = max(self.adversario_hp - 25, 0)
            self.lbl_status.config(text="🔥 Chute Especial! -25 HP no adversário!")
        elif item_nome == "🛡️ Escudo":
            self.defendendo = True
            self.lbl_status.config(text="🛡️ Escudo ativado! Próximo ataque reduzido!")
        self.itens[item_nome] -= 1
        self.atualizar_interface()
        self.root.after(1500, self.turno_adversario)

    # ======== ATUALIZAR INTERFACE ========
    def atualizar_interface(self):
        self.canvas_hp_jogador.coords(self.barra_hp_jogador, 0, 0, 300 * (self.jogador_hp / self.hp_max), 20)
        self.canvas_hp_adversario.coords(self.barra_hp_adversario, 0, 0, 300 * (self.adversario_hp / self.hp_max), 20)
        self.canvas_energy_jogador.coords(self.barra_energy_jogador, 0, 0, 240 * (self.jogador_energia / 100), 6)
        self.canvas_energy_adversario.coords(self.barra_energy_adversario, 0, 0, 240 * (self.adversario_energia / 100), 6)
        self.lbl_hp_jogador.config(text=f"{self.jogador.nome} ❤️ {self.jogador_hp}/{self.hp_max}")
        self.lbl_hp_adversario.config(text=f"{self.adversario_nome} ❤️ {self.adversario_hp}/{self.hp_max}")
        self.animar_barra_energia(self.canvas_energy_jogador, self.barra_energy_jogador)
        self.animar_barra_energia(self.canvas_energy_adversario, self.barra_energy_adversario)

    # ======== ENCERRAR PARTIDA ========
    def encerrar_partida(self, derrota=False):
        if derrota:
            messagebox.showinfo("💀", "Você foi derrotado! Tente novamente.")
            self.nivel = 1
            self.tela_inicial()
        else:
            messagebox.showinfo("🏆", f"Você venceu o nível {self.nivel}! Indo para o próximo!")
            self.nivel += 1
            self.iniciar_jogo()


if __name__ == "__main__":
    root = tk.Tk()
    app = FIFA_GUI_PLUS(root)
    root.mainloop()
