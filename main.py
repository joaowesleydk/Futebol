import tkinter as tk
from gui import FIFA_GUI_PLUS  # importa a interface principal


class FIFA_RPG:
    def __init__(self, root):
        self.root = root
        self.root.title("⚽Batalha das Lendas RPG⚽")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#0b132b")

        # Começa mostrando a primeira história
        self.mostrar_primeira_historia()

    # ====== PRIMEIRA HISTÓRIA ======
    def mostrar_primeira_historia(self):
        """Primeira janela de história sobre a honra do futebol."""
        self.janela1 = tk.Toplevel(self.root)
        self.janela1.title("🏆 A Honra Perdida 🏆")
        self.janela1.geometry("800x600")
        self.janela1.configure(bg="#1c2541")
        self.janela1.resizable(True, True)

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
            font=("Comic Sans MS", 13),
            fg="white",
            bg="#1c2541",
            justify="center",
            wraplength=700
        )
        texto1.pack(pady=50)

        btn_continuar1 = tk.Button(
            self.janela1,
            text="➡️ Continuar",
            font=("Comic Sans MS", 14, "bold"),
            bg="#f0a500",
            fg="black",
            activebackground="#f4b942",
            activeforeground="black",
            relief="raised",
            bd=4,
            width=15,
            command=self.mostrar_segunda_historia
        )
        btn_continuar1.pack(pady=20)

    # ====== SEGUNDA HISTÓRIA ======
    def mostrar_segunda_historia(self):
        """Segunda janela de história sobre craques lendários e habilidades."""
        self.janela1.destroy()  # fecha a primeira história

        self.janela2 = tk.Toplevel(self.root)
        self.janela2.title("🏆 A Lenda Começa 🏆")
        self.janela2.geometry("800x600")
        self.janela2.configure(bg="#1c2541")
        self.janela2.resizable(True, True)

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
            font=("Comic Sans MS", 13),
            fg="white",
            bg="#1c2541",
            justify="center",
            wraplength=700
        )
        texto2.pack(pady=50)

        btn_continuar2 = tk.Button(
            self.janela2,
            text="➡️ Continuar",
            font=("Comic Sans MS", 14, "bold"),
            bg="#f0a500",
            fg="black",
            activebackground="#f4b942",
            activeforeground="black",
            relief="raised",
            bd=4,
            width=15,
            command=self.mostrar_tela_inicial
        )
        btn_continuar2.pack(pady=20)

    # ====== TELA INICIAL ======
    def mostrar_tela_inicial(self):
        """Fecha a segunda história e mostra a tela inicial."""
        self.janela2.destroy()
        self.criar_tela_inicial()

    def criar_tela_inicial(self):
        """Cria a tela inicial com o mesmo padrão visual da GUI principal."""
        self.root.resizable(False, False)

        frame = tk.Frame(self.root, bg="#1c2541", bd=6, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        titulo = tk.Label(
            frame,
            text="⚽Batalha das Lendas RPG⚽",
            font=("Comic Sans MS", 22, "bold"),
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
            font=("Comic Sans MS", 14),
            fg="white",
            bg="#1c2541",
            justify="center"
        )
        info.pack(pady=10)

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
        self.root.destroy()
        nova_janela = tk.Tk()
        app = FIFA_GUI_PLUS(nova_janela)
        nova_janela.mainloop()


# ====== Ponto de entrada ======
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # oculta a janela principal até o menu
    FIFA_RPG(root)
    root.mainloop()
