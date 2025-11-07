# ===================================================================
# BATALHA DAS LENDAS RPG - ARQUIVO PRINCIPAL
# ===================================================================
# Desenvolvido por: João Wesley D. Kind, Cristian Andrade, Nycollas Augusto
# Descrição: Jogo de RPG de futebol com lendas do esporte
# ===================================================================

# Importações necessárias
import tkinter as tk
from tkinter import messagebox
import traceback
from gui_simple import FIFA_GUI_PLUS  # Importa a interface principal do jogo
from utils.helpers import tocar_musica_fundo, parar_musica_fundo, narrar_texto


class FIFA_RPG:
    """Classe principal do jogo FIFA RPG"""
    
    def __init__(self, root):
        """Inicializa a aplicação principal
        
        Args:
            root: Janela principal do Tkinter
        """
        # Configuração da janela principal
        self.root = root
        self.root.title("⚽Batalha das Lendas RPG⚽")
        self.root.attributes("-fullscreen", True)  # Inicia em tela cheia
        self.root.configure(bg="#0b132b")  # Cor de fundo azul escuro

        # Bind para sair da tela cheia com ESC
        self.root.bind("<Escape>", self.sair_tela_cheia)

        # Container principal que será reutilizado em todas as telas
        self.container = tk.Frame(self.root, bg="#1c2541")
        self.container.pack(fill="both", expand=True)
        
        # Inicia música de fundo do menu principal
        tocar_musica_fundo("tema_main.mp3", volume=0.6)

        # Começa o jogo mostrando a primeira história
        self.mostrar_primeira_historia()

    # ====== FUNÇÕES DE CONTROLE DE TELA ======
    
    def sair_tela_cheia(self, event=None):
        """Sai do modo tela cheia quando ESC é pressionado"""
        self.root.attributes("-fullscreen", False)

    def voltar_fullscreen(self, event=None):
        """Volta para o modo tela cheia"""
        self.root.attributes("-fullscreen", True)

    def limpar_tela(self):
        """Remove todos os widgets do container, preparando para nova tela"""
        for widget in self.container.winfo_children():
            widget.destroy()

    def adicionar_botao_sair_full(self):
        """Adiciona botão no canto superior direito para sair do fullscreen"""
        btn_sair_full = tk.Button(
            self.container,
            text="⤫ Sair da Tela Cheia",
            font=("Comic Sans MS", 12, "bold"),
            bg="#e63946",  # Vermelho
            fg="white",
            command=lambda: self.root.attributes("-fullscreen", False)
        )
        # Posiciona no canto superior direito
        btn_sair_full.place(relx=0.98, rely=0.02, anchor="ne")

    # ====== TELAS DE HISTÓRIA ======
    
    def mostrar_primeira_historia(self):
        """Exibe a primeira história do jogo com narração por IA"""
        self.limpar_tela()
        self.container.configure(bg="#1c2541")
    
        # Texto da primeira história - contexto sobre a queda do futebol
        historia1 = (
            "Há muito tempo, o futebol era mais que um esporte — era a alma de uma nação.\n"
            "Craques lendários encantavam multidões e partidas se tornavam lendárias.\n\n"
            "Mas um dia, um mal misterioso começou a se espalhar pelo mundo dos gramados.\n"
            "Times foram corrompidos, craques desapareceram, e a honra do futebol foi perdida.\n\n"
            "O espírito do jogo, outrora brilhante e puro, caiu na escuridão.\n\n"
            "Agora, somente um jogador escolhido pode restaurar a glória e trazer de volta os dias de ouro!"
        )
        
        # Inicia narração por IA usando API ElevenLabs
        narrar_texto(historia1)

        # Label com o texto da história
        texto = tk.Label(
            self.container,
            text=historia1,
            font=("Comic Sans MS", 18),
            fg="white",
            bg="#1c2541",
            justify="center",
            wraplength=1000  # Quebra de linha automática
        )
        texto.pack(expand=True)

        # Botão para continuar para a segunda história
        btn_continuar = tk.Button(
            self.container,
            text="➡️ Continuar",
            font=("Comic Sans MS", 18, "bold"),
            bg="#f0a500",  # Amarelo/dourado
            fg="black",
            relief="raised",
            bd=4,
            width=18,
            command=self.mostrar_segunda_historia
        )
        btn_continuar.pack(pady=40)

        # Adiciona botão para sair da tela cheia
        self.adicionar_botao_sair_full()

    def mostrar_segunda_historia(self):
        """Exibe a segunda história do jogo com narração por IA"""
        self.limpar_tela()
        self.container.configure(bg="#1c2541")

        # Texto da segunda história - sobre o retorno das lendas
        historia2 = (
            "Em um mundo onde o futebol ultrapassa os limites do campo,\n"
            "craques lendários retornam em forma de espíritos poderosos.\n\n"
            "Cada jogador carrega a essência de um herói do passado —\n"
            "com habilidades únicas e golpes especiais capazes de mudar o destino do jogo.\n\n"
            "Você é o escolhido para restaurar a honra do futebol\n"
            "e conquistar a taça das lendas.\n\n"
            "Treine, lute e prove que é digno do título de Campeão Supremo!"
        )
        
        # Inicia narração da segunda história
        narrar_texto(historia2)

        # Label com o texto da segunda história
        texto = tk.Label(
            self.container,
            text=historia2,
            font=("Comic Sans MS", 18),
            fg="white",
            bg="#1c2541",
            justify="center",
            wraplength=1000
        )
        texto.pack(expand=True)

        # Botão para ir para a tela inicial do jogo
        btn_continuar = tk.Button(
            self.container,
            text="➡️ Continuar",
            font=("Comic Sans MS", 18, "bold"),
            bg="#f0a500",
            fg="black",
            relief="raised",
            bd=4,
            width=18,
            command=self.mostrar_tela_inicial
        )
        btn_continuar.pack(pady=40)

        self.adicionar_botao_sair_full()

    # ====== TELA INICIAL DO JOGO ======
    
    def mostrar_tela_inicial(self):
        """Exibe a tela inicial com informações do jogo e botão para iniciar"""
        self.limpar_tela()
        self.container.configure(bg="#1c2541")

        # Frame centralizado para organizar os elementos
        frame = tk.Frame(self.container, bg="#1c2541", bd=6, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=500)

        # Título principal do jogo
        titulo = tk.Label(
            frame,
            text="⚽Batalha das Lendas RPG⚽",
            font=("Comic Sans MS", 26, "bold"),
            fg="#f0a500",  # Dourado
            bg="#1c2541"
        )
        titulo.pack(pady=25)

        # Informações sobre o jogo
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

        # Botão principal para iniciar o jogo
        btn_jogar = tk.Button(
            frame,
            text="🏆 Iniciar Partida",
            font=("Comic Sans MS", 20, "bold"),
            bg="#f0a500",
            fg="black",
            relief="raised",
            bd=4,
            width=20,
            command=self.iniciar_jogo
        )
        btn_jogar.pack(pady=40)

        # Créditos dos desenvolvedores
        footer = tk.Label(
            frame,
            text="Desenvolvido por João Wesley D. Kind, Cristian Andrade e Nycollas Augusto",
            font=("Comic Sans MS", 12, "italic"),
            fg="#5bc0be",  # Azul claro
            bg="#1c2541"
        )
        footer.pack(side="bottom", pady=10)

        self.adicionar_botao_sair_full()

    # ====== INICIALIZAÇÃO DO JOGO ======
    
    def iniciar_jogo(self):
        """Inicia o jogo propriamente dito, abrindo a interface de batalha"""
        try:
            # Esconde a janela principal (menu)
            self.root.withdraw()
        except Exception:
            pass

        # Cria nova janela para o jogo
        toplevel = tk.Toplevel(self.root)
        toplevel.title("⚽ Batalha das Lendas - Modo Jogo ⚽")
        toplevel.attributes("-fullscreen", True)
        toplevel.configure(bg="#0b132b")

        # Botão para sair da tela cheia na janela do jogo
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
            # Inicializa a interface principal do jogo
            app = FIFA_GUI_PLUS(toplevel)

            def ao_fechar():
                """Função chamada quando a janela é fechada"""
                try:
                    toplevel.destroy()
                    self.root.destroy()
                except Exception:
                    pass

            # Define o que acontece quando a janela é fechada
            toplevel.protocol("WM_DELETE_WINDOW", ao_fechar)

        except Exception as e:
            # Tratamento de erro caso a interface não carregue
            tb = traceback.format_exc()
            print("Erro ao iniciar FIFA_GUI_PLUS:\n", tb)
            messagebox.showerror("Erro", tb[:2000])


# ====== PONTO DE ENTRADA DO PROGRAMA ======
if __name__ == "__main__":
    """Executa o programa quando o arquivo é executado diretamente"""
    # Cria a janela principal do Tkinter
    root = tk.Tk()
    
    # Inicializa a aplicação FIFA RPG
    app = FIFA_RPG(root)
    
    # Inicia o loop principal da interface gráfica
    root.mainloop()
