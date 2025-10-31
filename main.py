import tkinter as tk
from tkinter import messagebox
import traceback
from gui import FIFA_GUI_PLUS  # importa a interface principal


class FIFA_RPG:
    def __init__(self, root):
        self.root = root
        self.root.title("⚽Batalha das Lendas RPG⚽")
        self.root.attributes("-fullscreen", True)  # ✅ fullscreen inicial
        self.root.configure(bg="#0b132b")

        # permite sair do fullscreen com ESC
        self.root.bind("<Escape>", self.sair_tela_cheia)

        # Começa mostrando a primeira história
        self.mostrar_primeira_historia()

    # ====== FUNÇÃO PARA SAIR DO FULLSCREEN ======
    def sair_tela_cheia(self, event=None):
        """Sai do modo tela cheia."""
        self.root.attributes("-fullscreen", False)

    def voltar_fullscreen(self, event=None):
        """Retorna ao modo tela cheia."""
        self.root.attributes("-fullscreen", True)

    # ====== PRIMEIRA HISTÓRIA ======
    def mostrar_primeira_historia(self):
        self.janela1 = tk.Toplevel(self.root)
        self.janela1.title("🏆 A Honra Perdida 🏆")
        self.janela1.attributes("-fullscreen", True)
        self.janela1.configure(bg="#1c2541")

        # ESC também sai do fullscreen
        self.janela1.bind("<Escape>", lambda e: self.janela1.attributes("-fullscreen", False))

        historia1 = (
            "Há muito tempo, o futebol era mais que um esporte — era a alma de uma nação.\n"
            "Craques lendários encantavam multidões e partidas se tornavam lendas.\n\n"
            "Mas um dia, um mal misterioso começou a se espalhar pelo mundo dos gramados.\n"
            "Times foram corrompidos, craques desapareceram, e a honra do futebol foi perdida.\n\n"
            "O espírito do jogo, outrora brilhante e puro, caiu na escuridão.\n\n"
            "Agora, somente um jogador escolhido pode restaurar a glória e trazer de volta os dias de ouro!"
        )

        texto1 = tk.Label(
            self.janela1,
            text=historia1,
            font=("Comic Sans MS", 18),
            fg="white",
            bg="#1c2541",
            justify="center",
            wraplength=1000
        )
        texto1.pack(expand=True)

        btn_continuar1 = tk.Button(
            self.janela1,
            text="➡️ Continuar",
            font=("Comic Sans MS", 18, "bold"),
            bg="#f0a500",
            fg="black",
            relief="raised",
            bd=4,
            width=18,
            command=self.mostrar_segunda_historia
        )
        btn_continuar1.pack(pady=40)

        # botão sair fullscreen
        btn_sair_full = tk.Button(
            self.janela1,
            text="⤫ Sair da Tela Cheia",
            font=("Comic Sans MS", 12, "bold"),
            bg="#e63946",
            fg="white",
            command=lambda: self.janela1.attributes("-fullscreen", False)
        )
        btn_sair_full.place(relx=0.98, rely=0.02, anchor="ne")

    # ====== SEGUNDA HISTÓRIA ======
    def mostrar_segunda_historia(self):
        try:
            self.janela1.destroy()
        except Exception:
            pass

        self.janela2 = tk.Toplevel(self.root)
        self.janela2.title("🏆 A Lenda Começa 🏆")
        self.janela2.attributes("-fullscreen", True)
        self.janela2.configure(bg="#1c2541")
        self.janela2.bind("<Escape>", lambda e: self.janela2.attributes("-fullscreen", False))

        historia2 = (
            "Em um mundo onde o futebol ultrapassa os limites do campo,\n"
            "craques lendários retornam em forma de espíritos poderosos.\n\n"
            "Cada jogador carrega a essência de um herói do passado —\n"
            "com habilidades únicas e golpes especiais capazes de mudar o destino do jogo.\n\n"
            "Você é o escolhido para restaurar a honra do futebol\n"
            "e conquistar a taça das lendas.\n\n"
            "Treine, lute e prove que é digno do título de Campeão Supremo!"
        )

        texto2 = tk.Label(
            self.janela2,
            text=historia2,
            font=("Comic Sans MS", 18),
            fg="white",
            bg="#1c2541",
            justify="center",
            wraplength=1000
        )
        texto2.pack(expand=True)

        btn_continuar2 = tk.Button(
            self.janela2,
            text="➡️ Continuar",
            font=("Comic Sans MS", 18, "bold"),
            bg="#f0a500",
            fg="black",
            relief="raised",
            bd=4,
            width=18,
            command=self.mostrar_tela_inicial
        )
        btn_continuar2.pack(pady=40)

        btn_sair_full = tk.Button(
            self.janela2,
            text="⤫ Sair da Tela Cheia",
            font=("Comic Sans MS", 12, "bold"),
            bg="#e63946",
            fg="white",
            command=lambda: self.janela2.attributes("-fullscreen", False)
        )
        btn_sair_full.place(relx=0.98, rely=0.02, anchor="ne")

    # ====== TELA INICIAL ======
    def mostrar_tela_inicial(self):
        try:
            self.janela2.destroy()
        except Exception:
            pass
        self.criar_tela_inicial()

    def criar_tela_inicial(self):
        self.root.deiconify()
        self.root.attributes("-fullscreen", True)

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#1c2541", bd=6, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=500)

        titulo = tk.Label(
            frame,
            text="⚽Batalha das Lendas RPG⚽",
            font=("Comic Sans MS", 26, "bold"),
            fg="#f0a500",
            bg="#1c2541"
        )
        titulo.pack(pady=25)

        info = tk.Label(
            frame,
            text=(
                "Bem-vindo à Batalha das Lendas!\n"
                "Enfrente craques lendários, role o dado\n"
                "e prove que é o maior do futebol RPG!"
            ),
            font=("Comic Sans MS", 18),
            fg="white",
            bg="#1c2541",
            justify="center"
        )
        info.pack(pady=10)

        btn_jogar = tk.Button(
            frame,
            text="🏆 Iniciar Partida",
            font=("Comic Sans MS", 20, "bold"),
            bg="#f0a500",
            fg="black",
            relief="raised",
            bd=4,
            width=20,
            height=1,
            command=self.iniciar_jogo
        )
        btn_jogar.pack(pady=40)

        footer = tk.Label(
            frame,
            text="Desenvolvido por João Wesley D. Kind, Cristian Andrade e Nycollas Augusto",
            font=("Comic Sans MS", 12, "italic"),
            fg="#5bc0be",
            bg="#1c2541"
        )
        footer.pack(side="bottom", pady=10)

        # botão sair fullscreen
        btn_sair_full = tk.Button(
            self.root,
            text="⤫ Sair da Tela Cheia",
            font=("Comic Sans MS", 12, "bold"),
            bg="#e63946",
            fg="white",
            command=lambda: self.root.attributes("-fullscreen", False)
        )
        btn_sair_full.place(relx=0.98, rely=0.02, anchor="ne")

    # ====== INICIAR JOGO ======
    def iniciar_jogo(self):
        try:
            self.root.withdraw()
        except Exception:
            pass

        toplevel = tk.Toplevel(self.root)
        toplevel.title("⚽ Batalha das Lendas - Modo Jogo ⚽")
        toplevel.attributes("-fullscreen", True)
        toplevel.configure(bg="#0b132b")

        # ESC sai do fullscreen
        toplevel.bind("<Escape>", lambda e: toplevel.attributes("-fullscreen", False))

        # botão sair fullscreen
        btn_sair_full = tk.Button(
            toplevel,
            text="⤫ Sair da Tela Cheia",
            font=("Comic Sans MS", 12, "bold"),
            bg="#e63946",
            fg="white",
            command=lambda: toplevel.attributes("-fullscreen", False)
        )
        btn_sair_full.place(relx=0.98, rely=0.02, anchor="ne")

        try:
            app = FIFA_GUI_PLUS(toplevel)

            def ao_fechar():
                try:
                    toplevel.destroy()
                    self.root.destroy()
                except Exception:
                    pass

            toplevel.protocol("WM_DELETE_WINDOW", ao_fechar)

        except Exception as e:
            tb = traceback.format_exc()
            print("Erro ao iniciar FIFA_GUI_PLUS:\n", tb)
            messagebox.showerror("Erro", tb[:2000])


# ====== Ponto de entrada ======
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = FIFA_RPG(root)
    root.mainloop()
