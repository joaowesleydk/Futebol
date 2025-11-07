# ===================================================================
# INTERFACE GRÁFICA DO JOGO - BATALHA DAS LENDAS RPG
# ===================================================================
# Arquivo: gui_simple.py
# Descrição: Interface principal do jogo com animações e batalhas
# Recursos: Sistema de batalha, animações, sons, easter eggs
# ===================================================================

# Importações necessárias
import tkinter as tk
from tkinter import messagebox
import random
from models import Jogador  # Classes dos personagens
from game_logic_simple import Partida  # Lógica de batalha
from utils.helpers import tocar_som, tocar_musica_fundo, parar_musica_fundo  # Sistema de áudio
import os
from PIL import Image, ImageTk  # Para carregar e redimensionar imagens

class FIFA_GUI_PLUS:
    """Classe principal da interface gráfica do jogo"""
    
    def __init__(self, root):
        """Inicializa a interface do jogo
        
        Args:
            root: Janela principal do Tkinter
        """
        # Configuração da janela
        self.root = root
        self.root.title("⚽ Batalha das Lendas RPG ⚽")
        self.root.geometry("800x600")
        self.root.configure(bg="#0b132b")  # Fundo azul escuro

        # Variáveis de estado do jogo
        self.partida = None  # Instância da partida atual
        self.jogador = None  # Jogador criado
        self.turno_jogador = True  # Controla de quem é a vez
        
        # Inventário inicial do jogador
        self.itens = {"⚡ Energético": 2, "🔥 Chute Especial": 1, "🛡️ Escudo": 1}
        
        # Estados de batalha
        self.defendendo = False  # Se o jogador está defendendo
        self.nivel = 1  # Nível atual (adversário)
        
        # Sistema de animações
        self.imagens_carregadas = False  # Flag para verificar se imagens foram carregadas
        self.imagens = {}  # Dicionário para armazenar as imagens

        # Inicia com a tela de criação de personagem
        self.tela_inicial()

    # ====== CONTROLES DE TELA CHEIA ======
    
    def create_fullscreen_controls(self):
        """Cria controles para gerenciar o modo tela cheia"""
        try:
            # Remove botão anterior se existir
            if hasattr(self, "btn_sair_full") and self.btn_sair_full.winfo_exists():
                self.btn_sair_full.destroy()
        except Exception:
            pass

        try:
            # Força modo tela cheia
            self.root.attributes("-fullscreen", True)
        except Exception:
            pass

        try:
            # Bind da tecla ESC para sair da tela cheia
            self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        except Exception:
            pass

        try:
            # Cria botão para sair da tela cheia
            self.btn_sair_full = tk.Button(
                self.root,
                text="⤫ Sair da Tela Cheia",
                font=("Comic Sans MS", 12, "bold"),
                bg="#e63946",  # Vermelho
                fg="white",
                relief="raised",
                bd=3,
                command=lambda: self.root.attributes("-fullscreen", False)
            )
            # Posiciona no canto superior direito
            self.btn_sair_full.place(relx=0.98, rely=0.02, anchor="ne")
        except Exception:
            pass

    # ====== TELA DE CRIAÇÃO DE PERSONAGEM ======
    
    def tela_inicial(self):
        """Tela onde o jogador digita seu nome para criar o personagem"""
        # Limpa todos os widgets da tela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame centralizado para organizar elementos
        frame = tk.Frame(self.root, bg="#1c2541", bd=4, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=300)

        # Título do jogo
        titulo = tk.Label(frame, text="⚽ Batalha das Lendas RPG ⚽",
                          font=("Comic Sans MS", 20, "bold"),
                          fg="#f0a500", bg="#1c2541")  # Dourado sobre azul
        titulo.pack(pady=20)

        # Label instrução
        lbl_nome = tk.Label(frame, text="Digite seu nome:",
                            font=("Comic Sans MS", 14),
                            fg="white", bg="#1c2541")
        lbl_nome.pack(pady=10)

        # Campo de entrada do nome (suporta easter egg "flamengo")
        self.nome_entry = tk.Entry(frame, font=("Comic Sans MS", 14), justify="center")
        self.nome_entry.pack(pady=5)

        # Botão para iniciar o jogo
        btn_iniciar = tk.Button(frame, text="Começar Jogo ⚡",
                                font=("Comic Sans MS", 14, "bold"),
                                bg="#f0a500", fg="black",
                                relief="raised", bd=3,
                                command=self.iniciar_jogo)
        btn_iniciar.pack(pady=20)

        # Permite iniciar com Enter
        self.root.bind("<Return>", lambda event: self.iniciar_jogo())
        
        # Configura tela cheia e inicia música de batalha
        self.create_fullscreen_controls()
        tocar_musica_fundo("tema_batalha.mp3")

    def iniciar_jogo(self):
        """Cria o jogador e inicia a primeira batalha"""
        tocar_som("click.mp3")  # Som de clique
        
        # Obtém o nome digitado
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Digite seu nome para começar!")
            return

        # ====== EASTER EGG: FLAMENGO ======
        # Se o nome for "flamengo", cria um jogador super forte
        if nome.lower() == "flamengo":
            self.jogador = Jogador(nome, energia=200, chute=20, defesa=15, precisao=100)
            self.jogador.easter_egg = True  # Flag para sempre tirar 20 no dado
        else:
            # Jogador normal
            self.jogador = Jogador(nome, energia=100, chute=10, defesa=8, precisao=70)
            self.jogador.easter_egg = False
            
        # Cria a primeira partida
        self.partida = Partida(self.jogador, nivel=self.nivel)
        self.adversario = self.partida.adversario
        self.adversario_nome = self.adversario.nome

        # Inicializa variáveis de HP e energia
        self.jogador_hp = self.jogador.energia
        self.jogador_energia = self.jogador.energia
        self.adversario_hp = self.adversario.energia
        self.adversario_energia = self.adversario.energia

        # Armazena HP máximo para cálculos de barra
        self.jogador_hp_max = self.jogador_hp
        self.adversario_hp_max = self.adversario_hp

        # Vai para a tela de batalha
        self.tela_jogo()

    def iniciar_proximo_nivel(self):
        self.jogador.energia_max = getattr(self.jogador, "energia_max", self.jogador.energia) + 5
        self.jogador.energia = self.jogador.energia_max

        self.partida = Partida(self.jogador, nivel=self.nivel)
        self.adversario = self.partida.adversario
        self.adversario_nome = self.adversario.nome

        self.adversario_hp = self.adversario.energia
        self.adversario_energia = self.adversario.energia
        self.jogador_hp = self.jogador.energia
        self.jogador_energia = self.jogador.energia

        self.jogador_hp_max = self.jogador_hp
        self.adversario_hp_max = self.adversario_hp

        self.turno_jogador = True
        self.defendendo = False

        self.tela_jogo()

        try:
            self.btn_chutar.config(state="normal")
            self.btn_defender.config(state="normal")
            self.btn_item.config(state="normal")
        except:
            pass

    def tela_jogo(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.frame_jogo = tk.Frame(self.root, bg="#0b132b")
        self.frame_jogo.pack(fill="both", expand=True)

        btn_sair = tk.Button(
            self.frame_jogo,
            text="🚪 Sair do Jogo",
            font=("Comic Sans MS", 12, "bold"),
            bg="#e63946",
            fg="white",
            relief="raised",
            bd=3,
            command=self.root.destroy
        )
        btn_sair.place(relx=0.98, rely=0.02, anchor="ne")

        self.lbl_status = tk.Label(self.frame_jogo, text=f"⚔️ Nível {self.nivel} - Partida iniciada!",
                                   font=("Comic Sans MS", 16, "bold"),
                                   fg="#f0a500", bg="#0b132b")
        self.lbl_status.pack(pady=20)

        self.criar_barras()

        self.label_dado = tk.Label(self.frame_jogo, text="🎲", font=("Arial", 30),
                                   bg="#0b132b", fg="white")
        self.label_dado.pack(pady=20)

        # Canvas para animação
        self.canvas_animacao = tk.Canvas(self.frame_jogo, width=800, height=300, bg="#0b132b", highlightthickness=0)
        self.canvas_animacao.pack(pady=5)

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
                          command=self.abrir_inventario)
        self.btn_item.grid(row=0, column=2, padx=15)

        self.lbl_status.config(text=f"⚽ Sua vez! Enfrente {self.adversario_nome}.")
        self.atualizar_interface()
        self.create_fullscreen_controls()
        self.carregar_imagens()
        self.iniciar_animacao_idle()

    # ====== SISTEMA DE ANIMAÇÕES ======
    
    def carregar_imagens(self):
        """Carrega todas as imagens necessárias para as animações"""
        try:
            # Caminho base para a pasta assets
            base_path = os.path.join(os.path.dirname(__file__), "assets")
            
            # Carrega imagens principais redimensionadas
            self.imagens['jogador'] = ImageTk.PhotoImage(
                Image.open(os.path.join(base_path, "animacoes", "jogador.png")).resize((80, 80))
            )
            self.imagens['bola'] = ImageTk.PhotoImage(
                Image.open(os.path.join(base_path, "animacoes", "bola.png")).resize((30, 30))
            )
            # Imagem do campo/gol como fundo da animação
            self.imagens['gol'] = ImageTk.PhotoImage(
                Image.open(os.path.join(base_path, "imagens", "gol.png")).resize((800, 300))
            )
            
            # Frames da animação de chute (3 frames)
            self.imagens['chute1'] = ImageTk.PhotoImage(
                Image.open(os.path.join(base_path, "animacoes", "chute", "frame1.png")).resize((80, 80))
            )
            self.imagens['chute2'] = ImageTk.PhotoImage(
                Image.open(os.path.join(base_path, "animacoes", "chute", "comp1.png")).resize((80, 80))
            )
            self.imagens['chute3'] = ImageTk.PhotoImage(
                Image.open(os.path.join(base_path, "animacoes", "chute", "comp3.png")).resize((80, 80))
            )
            
            # Marca que as imagens foram carregadas com sucesso
            self.imagens_carregadas = True
            
        except Exception as e:
            print(f"Erro ao carregar imagens: {e}")
            self.imagens_carregadas = False

    def iniciar_animacao_idle(self):
        if not self.imagens_carregadas:
            return
        
        self.canvas_animacao.delete("all")
        # Campo de fundo
        self.canvas_animacao.create_image(400, 150, image=self.imagens['gol'], tags="campo")
        # Jogador centralizado no campo
        self.canvas_animacao.create_image(400, 250, image=self.imagens['jogador'], tags="jogador")
        # Bola no pé do jogador
        self.canvas_animacao.create_image(430, 250, image=self.imagens['bola'], tags="bola")

    def animar_chute(self, resultado_dado):
        """Animação do chute baseada no resultado do dado
        
        Args:
            resultado_dado: Resultado do dado D20 (1-20)
        """
        if not self.imagens_carregadas:
            return  # Não anima se as imagens não carregaram
            
        def frame1():
            """Primeiro frame: jogador se preparando para chutar"""
            self.canvas_animacao.delete("all")
            # Desenha campo, jogador preparando e bola no pé
            self.canvas_animacao.create_image(400, 150, image=self.imagens['gol'], tags="campo")
            self.canvas_animacao.create_image(400, 250, image=self.imagens['chute1'], tags="jogador")
            self.canvas_animacao.create_image(430, 250, image=self.imagens['bola'], tags="bola")
            self.root.after(200, frame2)  # Próximo frame em 200ms
            
        def frame2():
            """Segundo frame: jogador no meio do chute"""
            self.canvas_animacao.delete("all")
            # Bola começa a se mover
            self.canvas_animacao.create_image(400, 150, image=self.imagens['gol'], tags="campo")
            self.canvas_animacao.create_image(400, 250, image=self.imagens['chute2'], tags="jogador")
            self.canvas_animacao.create_image(460, 200, image=self.imagens['bola'], tags="bola")
            self.root.after(200, frame3)
            
        def frame3():
            """Terceiro frame: jogador termina o chute, bola voa"""
            self.canvas_animacao.delete("all")
            self.canvas_animacao.create_image(400, 150, image=self.imagens['gol'], tags="campo")
            self.canvas_animacao.create_image(400, 250, image=self.imagens['chute3'], tags="jogador")
            
            # ====== DIREÇÃO DA BOLA BASEADA NO RESULTADO DO DADO ======
            if resultado_dado == 20:
                # Dado 20: Golaço no ângulo superior direito
                self.canvas_animacao.create_image(470, 80, image=self.imagens['bola'], tags="bola")
            elif resultado_dado >= 15:
                # Dado 15-19: Chute no ângulo
                self.canvas_animacao.create_image(440, 100, image=self.imagens['bola'], tags="bola")
            elif resultado_dado >= 10:
                # Dado 10-14: Gol comum no centro
                self.canvas_animacao.create_image(400, 120, image=self.imagens['bola'], tags="bola")
            elif resultado_dado >= 5:
                # Dado 5-9: Chute fraco na parte baixa
                self.canvas_animacao.create_image(370, 140, image=self.imagens['bola'], tags="bola")
            else:
                # Dado 1-4: Errou - bola vai para fora (acima do gol)
                self.canvas_animacao.create_image(400, 30, image=self.imagens['bola'], tags="bola")
                
            self.root.after(300, final)  # Frame final em 300ms
            
        def final():
            """Frame final: mostra resultado final por 1 segundo"""
            self.canvas_animacao.delete("all")
            self.canvas_animacao.create_image(400, 150, image=self.imagens['gol'], tags="campo")
            self.canvas_animacao.create_image(400, 250, image=self.imagens['jogador'], tags="jogador")
            
            # Posição final da bola (mesmo cálculo do frame3)
            if resultado_dado == 20:
                self.canvas_animacao.create_image(470, 80, image=self.imagens['bola'], tags="bola")
            elif resultado_dado >= 15:
                self.canvas_animacao.create_image(440, 100, image=self.imagens['bola'], tags="bola")
            elif resultado_dado >= 10:
                self.canvas_animacao.create_image(400, 120, image=self.imagens['bola'], tags="bola")
            elif resultado_dado >= 5:
                self.canvas_animacao.create_image(370, 140, image=self.imagens['bola'], tags="bola")
            else:
                self.canvas_animacao.create_image(400, 30, image=self.imagens['bola'], tags="bola")
                
            # Volta para animação idle após 1 segundo
            self.root.after(1000, self.iniciar_animacao_idle)
            
        frame1()  # Inicia a animação

    def abrir_inventario(self):
        inv = tk.Toplevel(self.root)
        inv.title("🎒 Mochila")
        inv.configure(bg="#1c2541")
        inv.geometry("420x360")
        inv.resizable(False, False)
        inv.grab_set()

        tk.Label(inv, text="🎒 Seus Itens", font=("Comic Sans MS", 18, "bold"),
                 fg="#f0a500", bg="#1c2541").pack(pady=10)

        frame_itens = tk.Frame(inv, bg="#1c2541")
        frame_itens.pack(pady=10)

        if all(qtd == 0 for qtd in self.itens.values()):
            tk.Label(frame_itens, text="(vazio)", font=("Comic Sans MS", 14),
                     fg="white", bg="#1c2541").pack(pady=20)
        else:
            cores = {
                "⚡ Energético": "#ffcc00",
                "🔥 Chute Especial": "#ff5733",
                "🛡️ Escudo": "#5bc0be"
            }
            for item_nome, qtd in self.itens.items():
                if qtd > 0:
                    linha = tk.Frame(frame_itens, bg="#1c2541")
                    linha.pack(pady=5)

                    cor = cores.get(item_nome, "white")
                    tk.Label(linha, text=f"{item_nome}  x{qtd}",
                             font=("Comic Sans MS", 14),
                             fg=cor, bg="#1c2541").pack(side="left", padx=10)

                    tk.Button(linha, text="Usar", font=("Comic Sans MS", 12, "bold"),
                              bg=cor, fg="black", width=6,
                              command=lambda nome=item_nome, win=inv: self.usar_item(nome, win)
                              ).pack(side="right", padx=10)

        tk.Button(inv, text="Fechar", font=("Comic Sans MS", 12, "bold"),
                  bg="#e63946", fg="white", width=10,
                  command=inv.destroy).pack(pady=20)

    def usar_item(self, item_nome, janela_inv=None):
        tocar_som("item.mp3")
        if self.itens.get(item_nome, 0) <= 0:
            messagebox.showinfo("🎒 Mochila", f"Você não tem mais {item_nome}!")
            return

        if item_nome == "⚡ Energético":
            self.jogador_hp = min(self.jogador_hp + 30, self.jogador_hp_max)
            self.lbl_status.config(text="⚡ Você bebeu um energético! +30 HP!")
        elif item_nome == "🔥 Chute Especial":
            self.adversario_hp = max(self.adversario_hp - 25, 0)
            self.lbl_status.config(text="🔥 Chute Especial! -25 HP no adversário!")
              
            if self.verificar_vitoria():
                return
        elif item_nome == "🛡️ Escudo":
            self.defendendo = True
            self.lbl_status.config(text="🛡️ Escudo ativado! Próximo ataque reduzido!")

        self.itens[item_nome] -= 1
        self.atualizar_interface()

        if janela_inv:
            janela_inv.destroy()

        self.root.after(1500, self.turno_adversario)

    def sortear_drop(self):
        chance_drop = random.random()
        if chance_drop <= 0.6:
            tocar_som("item.mp3")
            raridade = random.random()
            if raridade <= 0.7:
                item, tipo, cor = "⚡ Energético", "comum", "#ffcc00"
            elif raridade <= 0.95:
                item, tipo, cor = "🔥 Chute Especial", "raro", "#ff5733"
            else:
                item, tipo, cor = "💎 Escudo Divino", "lendário", "#5bc0be"

            self.itens[item] = self.itens.get(item, 0) + 1

            drop = tk.Toplevel(self.root)
            drop.configure(bg="#0b132b")
            drop.geometry("500x300")
            drop.title("🎁 Recompensa!")

            tk.Label(drop, text="🎉 Você ganhou um item!", font=("Comic Sans MS", 20, "bold"),
                     fg="#f0a500", bg="#0b132b").pack(pady=20)

            tk.Label(drop, text=f"{item}", font=("Comic Sans MS", 40, "bold"),
                     fg=cor, bg="#0b132b").pack(pady=20)

            tk.Label(drop, text=f"Item {tipo.upper()} encontrado!", font=("Comic Sans MS", 16),
                     fg="white", bg="#0b132b").pack(pady=10)

            tk.Button(drop, text="Continuar ⭐", font=("Comic Sans MS", 14, "bold"),
                      bg="#f0a500", fg="black", width=12,
                      command=lambda: [drop.destroy(), self.animar_subida_nivel()]).pack(pady=20)
        else:
            messagebox.showinfo("🎁 Recompensa!", "Nenhum item foi encontrado desta vez...")
            self.animar_subida_nivel()

    def criar_barras(self):
        frame_jogador = tk.Frame(self.frame_jogo, bg="#0b132b")
        frame_jogador.pack(pady=(0, 10))

        self.lbl_hp_jogador = tk.Label(frame_jogador,
                                       text=f"{self.jogador.nome} ❤️ {self.jogador_hp}/{self.jogador_hp_max}",
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

        frame_adv = tk.Frame(self.frame_jogo, bg="#0b132b")
        frame_adv.pack(pady=(10, 10))

        self.lbl_hp_adversario = tk.Label(frame_adv,
                                          text=f"{self.adversario_nome} ❤️ {self.adversario_hp}/{self.adversario_hp_max}",
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

    def animar_barra_energia(self, canvas, barra, cor="#0099ff"):
        def brilho():
            canvas.itemconfig(barra, fill="#66ccff")
            canvas.after(150, lambda: canvas.itemconfig(barra, fill=cor))
        brilho()

    # ====== SISTEMA DE DADOS ======
    
    def rolar_dado(self, callback):
        """Rola um dado D20 com animação visual
        
        Args:
            callback: Função a ser chamada com o resultado do dado
        """
        # ====== EASTER EGG: FLAMENGO SEMPRE TIRA 20 ======
        if hasattr(self.jogador, 'easter_egg') and self.jogador.easter_egg:
            resultado_final = 20  # Flamengo sempre tira crítico!
        else:
            resultado_final = random.randint(1, 20)  # Dado normal
            
        def animar(cont=0):
            """Animação do dado rolando"""
            if cont < 15:  # 15 frames de animação
                # Mostra números aleatórios durante a animação
                self.label_dado.config(text=f"🎲 {random.randint(1,20)}")
                self.root.after(60, animar, cont + 1)  # Próximo frame em 60ms
            else:
                # Mostra o resultado final
                self.label_dado.config(text=f"🎲 {resultado_final}")
                callback(resultado_final)  # Chama a função com o resultado
                
        animar()  # Inicia a animação

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
            tocar_som("chute.mp3")
            self.jogador_energia = max(0, self.jogador_energia - 10)
            dano = 0

            if dado == 20:
                msg = "🌀 GOL DE BICICLETA! Golpe crítico!"
                dano = 40
            elif dado >= 15:
                msg = "🚀 Chute no Ângulo! Golaço!"
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
            
            # Animação baseada no resultado
            self.animar_chute(dado)

            self.atualizar_interface()
            if not self.verificar_vitoria():
                self.root.after(500, self.turno_adversario)

        elif acao == "defender":
            tocar_som("defesa.mp3")
            self.defendendo = True
            self.lbl_status.config(text="🛡️ Você se prepara para defender o próximo ataque!")
            self.root.after(1500, self.turno_adversario)

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
            msg = "🙅♂️ Você defendeu o chute!"
            tocar_som("defesa.mp3")
            dano = 0
        
        if self.defendendo:
            dano = int(dano * 0.5)
            msg += " 🛡️ Defesa eficaz!"
            tocar_som("defesa.mp3")

        self.adversario_energia = max(0, self.adversario_energia - 10)
        self.jogador_hp = max(self.jogador_hp - dano, 0)
        self.lbl_status.config(text=f"{msg} (D20: {dado})")

        if self.verificar_vitoria():
            return

        self.atualizar_interface()
        self.root.after(1500, self.liberar_turno)

    def liberar_turno(self):
        self.turno_jogador = True
        for btn in [self.btn_chutar, self.btn_defender, self.btn_item]:
            btn.config(state="normal")
        self.lbl_status.config(text="⚽ Sua vez!")

    def verificar_vitoria(self):
        if self.adversario_hp <= 0:
            self.encerrar_partida(derrota=False)
            return True
        if self.jogador_hp <= 0:
            self.encerrar_partida(derrota=True)
            return True
        return False

    def atualizar_interface(self):
        hp_ratio_j = self.jogador_hp / self.jogador_hp_max
        hp_ratio_a = self.adversario_hp / self.adversario_hp_max
        energy_ratio_j = self.jogador_energia / 100
        energy_ratio_a = self.adversario_energia / 100

        self.canvas_hp_jogador.coords(self.barra_hp_jogador, 0, 0, 300 * hp_ratio_j, 20)
        self.canvas_hp_adversario.coords(self.barra_hp_adversario, 0, 0, 300 * hp_ratio_a, 20)
        self.canvas_energy_jogador.coords(self.barra_energy_jogador, 0, 0, 240 * energy_ratio_j, 6)
        self.canvas_energy_adversario.coords(self.barra_energy_adversario, 0, 0, 240 * energy_ratio_a, 6)

        self.lbl_hp_jogador.config(text=f"{self.jogador.nome} ❤️ {self.jogador_hp}/{self.jogador_hp_max}")
        self.lbl_hp_adversario.config(text=f"{self.adversario_nome} ❤️ {self.adversario_hp}/{self.adversario_hp_max}")

        self.animar_barra_energia(self.canvas_energy_jogador, self.barra_energy_jogador)
        self.animar_barra_energia(self.canvas_energy_adversario, self.barra_energy_adversario)

    def encerrar_partida(self, derrota=False):
        if derrota:
            messagebox.showinfo("💀", "Você foi derrotado! Tente novamente.")
            self.nivel = 1
            self.tela_inicial()
        else:
            # Verifica se derrotou o Pelé (boss final)
            if self.nivel == 6 and self.adversario_nome == "Pelé":
                self.tela_vitoria_final()
            else:
                self.sortear_drop()

    def animar_subida_nivel(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_anim = tk.Frame(self.root, bg="#0b132b")
        frame_anim.pack(fill="both", expand=True)

        label = tk.Label(frame_anim, text=f"⭐ {self.jogador.nome} Subiu para o Nível {self.nivel + 1}! ⭐",
                         font=("Comic Sans MS", 22, "bold"),
                         fg="#f0a500", bg="#0b132b")
        label.place(relx=0.5, rely=0.5, anchor="center")

        def piscar(c=0):
            if c < 8:
                label.config(fg="#f0a500" if c % 2 == 0 else "#ffffff")
                self.root.after(300, lambda: piscar(c + 1))
            else:
                self.nivel += 1
                self.iniciar_proximo_nivel()

        piscar()
        self.create_fullscreen_controls()

    # ====== TELA DE VITÓRIA FINAL ======
    
    def tela_vitoria_final(self):
        """Tela especial exibida quando o jogador derrota o Pelé (boss final)"""
        # Limpa toda a tela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal da tela de vitória
        frame_vitoria = tk.Frame(self.root, bg="#0b132b")
        frame_vitoria.pack(fill="both", expand=True)

        # Título de parabéns em dourado
        titulo = tk.Label(frame_vitoria, text="🏆 PARABÉNS! 🏆",
                         font=("Comic Sans MS", 36, "bold"),
                         fg="#f0a500", bg="#0b132b")  # Dourado
        titulo.pack(pady=30)

        # Mensagem principal da vitória
        mensagem = tk.Label(frame_vitoria, 
                           text="Você derrotou o lendário Pelé!\n\nO futebol foi restaurado!\n\nVocê é o novo Campeão Supremo!",
                           font=("Comic Sans MS", 24),
                           fg="white", bg="#0b132b",
                           justify="center")
        mensagem.pack(pady=20)

        # Troféu gigante (emoji)
        trofeu = tk.Label(frame_vitoria, text="🏆",
                         font=("Arial", 120),  # Tamanho gigante
                         bg="#0b132b")
        trofeu.pack(pady=30)

        # Botão para jogar novamente (reiniciar do nível 1)
        btn_novo_jogo = tk.Button(frame_vitoria, text="🎆 Jogar Novamente",
                                 font=("Comic Sans MS", 18, "bold"),
                                 bg="#f0a500", fg="black",
                                 relief="raised", bd=4,
                                 width=20,
                                 command=self.reiniciar_jogo)
        btn_novo_jogo.pack(pady=20)

        # Toca som de vitória épica
        tocar_som("vitoria.mp3")
        
        # Mantém controles de tela cheia
        self.create_fullscreen_controls()

    def reiniciar_jogo(self):
        """Reinicia o jogo do nível 1"""
        self.nivel = 1  # Volta para o primeiro nível
        self.tela_inicial()  # Volta para a tela de criação de personagem

if __name__ == "__main__":
    root = tk.Tk()
    app = FIFA_GUI_PLUS(root)
    root.mainloop()