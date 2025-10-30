import tkinter as tk
from gui import FIFA_GUI_PLUS  # importa a interface principal


class FIFA_RPG:
    def __init__(self, root):
        self.root = root
        self.root.title("⚽Batalha das Lendas RPG⚽")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#0b132b")

        self.criar_tela_inicial()

    def criar_tela_inicial(self):
        """Cria a tela inicial com o mesmo padrão visual da GUI principal."""
        frame = tk.Frame(self.root, bg="#1c2541", bd=6, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        # ====== Título ======
        titulo = tk.Label(
            frame,
            text="⚽Batalha das Lendas RPG⚽",
            font=("Comic Sans MS", 22, "bold"),
            fg="#f0a500",
            bg="#1c2541"
        )
        titulo.pack(pady=25)

        # ====== Texto de introdução ======
        info = tk.Label(
            frame,
            text=(
                "Bem-vindo à Batalha das Lendas!\n"
                "Enfrente craques lendários, role o dado\n"
                "e prove que é o maior do futebol RPG!"
            ),
            font=("Comic Sans MS", 14),
            fg="white",
            bg="#1c2541",
            justify="center"
        )
        info.pack(pady=10)

        # ====== Botão principal ======
        btn_jogar = tk.Button(
            frame,
            text="🏆 Iniciar Partida",
            font=("Comic Sans MS", 15, "bold"),
            bg="#f0a500",
            fg="black",
            activebackground="#f4b942",
            activeforeground="black",
            relief="raised",
            bd=4,
            width=18,
            height=1,
            command=self.iniciar_jogo
        )
        btn_jogar.pack(pady=30)

        # ====== Rodapé ======
        footer = tk.Label(
            frame,
            text="Desenvolvido por João Wesley D. Kind, Cristian Andrade e Nycollas Augusto",
            font=("Comic Sans MS", 10, "italic"),
            fg="#5bc0be",
            bg="#1c2541"
        )
        footer.pack(side="bottom", pady=10)

    def iniciar_jogo(self):
        """Fecha a tela inicial e abre o jogo principal."""
        self.root.destroy()  # Fecha a tela inicial

        nova_janela = tk.Tk()
        app = FIFA_GUI_PLUS(nova_janela)
        nova_janela.mainloop()


# ====== Ponto de entrada ======
if __name__ == "__main__":
    root = tk.Tk()
    FIFA_RPG(root)
    root.mainloop()
