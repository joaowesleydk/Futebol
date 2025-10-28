import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading

from models import Jogador, Adversario
from game_logic import Batalha
from utils.helpers import tocar_som, tocar_musica_fundo, parar_musica_fundo, anima_bar


class FIFA_GUI_PLUS:
    def __init__(self, root):
        self.root = root
        self.root.title("⚽ FIFA RPG Cartoon Edition ⚽")
        self.root.geometry("780x540")
        self.root.config(bg="#e8f4fa")
        self.root.resizable(False, False)

        tocar_musica_fundo("assets/sons/menu.mp3")

        self.jogador = None
        self.adversario = None
        self.batalha = None

        self.criar_tela_inicial()

    # -------------------------------
    # TELA INICIAL
    # -------------------------------
    def criar_tela_inicial(self):
        for w in self.root.winfo_children():
            w.destroy()

        frame = tk.Frame(self.root, bg="#e8f4fa")
        frame.pack(expand=True, fill="both")

        titulo = tk.Label(
            frame,
            text="🏆 FIFA RPG CARTOON 🏆",
            font=("Comic Sans MS", 28, "bold"),
            fg="#0055aa",
            bg="#e8f4fa",
        )
        titulo.pack(pady=30)

        nome_label = tk.Label(frame, text="Digite seu nome:", font=("Comic Sans MS", 16), bg="#e8f4fa")
        nome_label.pack(pady=10)

        self.nome_entry = tk.Entry(frame, font=("Comic Sans MS", 16), justify="center")
        self.nome_entry.pack(pady=5)

        start_btn = tk.Button(
            frame,
            text="COMEÇAR ⚽",
            font=("Comic Sans MS", 18, "bold"),
            bg="#009933",
            fg="white",
            width=15,
            command=self.iniciar_jogo,
        )
        start_btn.pack(pady=30)

        creditos = tk.Label(
            frame,
            text="by Cristian Studios 💡",
            font=("Comic Sans MS", 12, "italic"),
            fg="#555",
            bg="#e8f4fa",
        )
        creditos.pack(side="bottom", pady=10)

    # -------------------------------
    # INICIAR JOGO
    # -------------------------------
    def iniciar_jogo(self):
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showwarning("Ops!", "Digite um nome antes de começar.")
            return

        parar_musica_fundo()
        tocar_musica_fundo("assets/sons/batalha.mp3")

        self.jogador = Jogador(nome)
        self.adversario = self.gerar_adversario_inicial()
        self.batalha = Batalha(self.jogador, self.adversario)

        self.exibir_batalha()

    # -------------------------------
    # BATALHA
    # -------------------------------
    def exibir_batalha(self):
        for w in self.root.winfo_children():
            w.destroy()

        frame = tk.Frame(self.root, bg="#dff5ff")
        frame.pack(expand=True, fill="both")

        titulo = tk.Label(
            frame,
            text=f"{self.jogador.nome} 🇧🇷 VS {self.adversario.nome}",
            font=("Comic Sans MS", 22, "bold"),
            bg="#dff5ff",
            fg="#004488",
        )
        titulo.pack(pady=20)

        # ---- ENERGIA ----
        self.barra_jogador = ttk.Progressbar(frame, length=250, maximum=100)
        self.barra_adversario = ttk.Progressbar(frame, length=250, maximum=100)

        tk.Label(frame, text=f"{self.jogador.nome}", bg="#dff5ff", font=("Comic Sans MS", 14)).pack()
        self.barra_jogador.pack(pady=5)

        tk.Label(frame, text=f"{self.adversario.nome}", bg="#dff5ff", font=("Comic Sans MS", 14)).pack()
        self.barra_adversario.pack(pady=5)

        # ---- BOTÕES ----
        botoes_frame = tk.Frame(frame, bg="#dff5ff")
        botoes_frame.pack(pady=30)

        tk.Button(botoes_frame, text="⚽ Chutar", width=12, font=("Comic Sans MS", 14),
                  command=lambda: self.jogar_turno("chutar")).grid(row=0, column=0, padx=8)
        tk.Button(botoes_frame, text="🧤 Defender", width=12, font=("Comic Sans MS", 14),
                  command=lambda: self.jogar_turno("defender")).grid(row=0, column=1, padx=8)
        tk.Button(botoes_frame, text="💨 Boost", width=12, font=("Comic Sans MS", 14),
                  command=lambda: self.jogar_turno("boost")).grid(row=0, column=2, padx=8)

        self.log_text = tk.Text(frame, height=10, width=70, font=("Comic Sans MS", 12))
        self.log_text.pack(pady=20)
        self.log_text.insert("end", f"🏁 Começa o jogo entre {self.jogador.nome} e {self.adversario.nome}!\n")

        self.atualizar_barras()

    # -------------------------------
    # TURNO
    # -------------------------------
    def jogar_turno(self, acao):
        threading.Thread(target=self._turno_thread, args=(acao,), daemon=True).start()

    def _turno_thread(self, acao):
        resultado = self.batalha.turno(acao)
        self.log_text.insert("end", resultado + "\n")
        self.log_text.see("end")

        self.atualizar_barras()
        self.root.update_idletasks()

        if self.batalha.terminou():
            self.final_batalha()

    # -------------------------------
    # ATUALIZAR INTERFACE
    # -------------------------------
    def atualizar_barras(self):
        anima_bar(self.barra_jogador, self.barra_jogador["value"], self.jogador.energia)
        anima_bar(self.barra_adversario, self.barra_adversario["value"], self.adversario.energia)

    # -------------------------------
    # FINAL DE BATALHA
    # -------------------------------
        # -------------------------------
    # FINAL DE BATALHA (ANIMADO)
    # -------------------------------
    def final_batalha(self):
        vencedor = self.batalha.vencedor()

        if vencedor == self.jogador.nome:
            tocar_som("assets/sons/vitoria.wav", 0.8)
            self.animacao_vitoria()  # 🌟 chama animação divertida
            self.jogador.ganhar_xp(50)

            self.root.after(3000, self.proxima_batalha)  # 3 seg de celebração

        else:
            tocar_som("assets/sons/derrota.wav", 0.8)
            self.animacao_derrota()  # 😵 efeito visual para derrota
            parar_musica_fundo()
            tocar_musica_fundo("assets/sons/menu.mp3")

            self.root.after(3000, self.criar_tela_inicial)  # volta ao menu


        # -------------------------------
    # ANIMAÇÕES DE VITÓRIA E DERROTA
    # -------------------------------
    def animacao_vitoria(self):
        """Faz a tela piscar e mostra texto de comemoração."""
        from utils.helpers import piscar_widget
        frame = tk.Frame(self.root, bg="#00ff88")
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        titulo = tk.Label(
            frame,
            text="🏆 VITÓÓÓRIA!!! 🏆",
            font=("Comic Sans MS", 34, "bold"),
            bg="#00ff88",
            fg="#003300",
        )
        titulo.place(relx=0.5, rely=0.5, anchor="center")

        # pisca o fundo com verde vibrante
        piscar_widget(frame, "#00ff88", "#66ffcc", vezes=6, intervalo=0.2)

        def limpar():
            frame.destroy()
        self.root.after(2800, limpar)

    def animacao_derrota(self):
        """Tela pisca vermelho quando o jogador perde."""
        from utils.helpers import piscar_widget
        frame = tk.Frame(self.root, bg="#ff5555")
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        titulo = tk.Label(
            frame,
            text="💀 DERROTA... 💀",
            font=("Comic Sans MS", 32, "bold"),
            bg="#ff5555",
            fg="#330000",
        )
        titulo.place(relx=0.5, rely=0.5, anchor="center")

        # pisca vermelho intenso
        piscar_widget(frame, "#ff5555", "#ff9999", vezes=6, intervalo=0.2)

        def limpar():
            frame.destroy()
        self.root.after(2800, limpar)

    # -------------------------------
    # PRÓXIMA FASE / ADVERSÁRIO
    # -------------------------------
    def proxima_batalha(self):
        nomes = ["Alemanha", "França", "Espanha", "Portugal", "Senegal", "Japão", "Croácia", "Dinamarca"]
        novo_nome = random.choice(nomes)
        self.adversario = Adversario(novo_nome, random.randint(2, 6))
        self.jogador.energia = self.jogador.energia_max
        self.batalha = Batalha(self.jogador, self.adversario)
        self.exibir_batalha()

    def gerar_adversario_inicial(self):
        times = ["Argentina", "Itália", "Inglaterra", "Holanda"]
        return Adversario(random.choice(times), nivel=random.randint(1, 3))
