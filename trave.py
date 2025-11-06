import tkinter as tk
from PIL import Image, ImageTk

# ===========================
# Janela principal
# ===========================
root = tk.Tk()  # Cria a janela principal do Tkinter
root.title("Chute no Gol")  # Título da janela
root.geometry("700x400")  # Tamanho da janela (largura x altura)
root.configure(bg="#0b132b")  # Cor de fundo da janela

# ===========================
# Canvas do campo
# ===========================
# O Canvas é onde vamos desenhar o gol, jogador e bola
canvas = tk.Canvas(root, width=700, height=400, bg="#1c2541", highlightthickness=0)
canvas.pack()  # Adiciona o Canvas na janela

# ===========================
# Carregar imagens
# ===========================
# Gol
gol_img = Image.open("assets/imagens/gol.png").resize((1000, 750))  # Redimensiona a imagem do gol
gol_photo = ImageTk.PhotoImage(gol_img)  # Converte a imagem para formato que o Tkinter entende
gol_item = canvas.create_image(350, 150, image=gol_photo)  # Desenha o gol no Canvas, posição centralizada (x=350, y=150)

# Jogador
jogador_img = Image.open("assets/animacoes/jogador.png").resize((80, 120))  # Redimensiona a imagem do jogador
jogador_photo = ImageTk.PhotoImage(jogador_img)
jogador_item = canvas.create_image(350, 300, image=jogador_photo)  # Desenha o jogador na frente do gol

# Bola
bola_img = Image.open("assets/animacoes/bola.png").resize((40, 40))  # Redimensiona a bola
bola_photo = ImageTk.PhotoImage(bola_img)
bola_item = canvas.create_image(400, 330, image=bola_photo)  # Coloca a bola na frente do jogador

# ===========================
# Status
# ===========================
# Label para mostrar mensagens, como quando o jogador faz gol
status = tk.Label(root, text="", font=("Arial", 16), bg="#0b132b", fg="white")
status.pack(pady=10)  # Adiciona a Label abaixo do Canvas

# ===========================
# Função de chute trave
# ===========================
def chutar():
    """
    Função que anima o chute da bola em direção ao gol.
    A bola sobe até y=100 e permanece lá.
    """
    x, y = 400, 330  # Posição inicial da bola (na frente do jogador)
    velocidade_y = -16  # Valor negativo para subir
    velocidade_x = 3    # Movimento horizontal da bola em direção ao gol
    altura_max = 25     # Altura máxima que a bola deve alcançar

    def mover_bola():
        nonlocal x, y

        # Se a bola ainda não atingiu a altura máxima e não passou do gol
        if y + velocidade_y > altura_max and x < 700:
            y += velocidade_y  # sobe
            x += velocidade_x  # move horizontalmente
            canvas.coords(bola_item, x, y)
            root.after(50, mover_bola)  # continua a animação
        else:
            # Bola atingiu a altura máxima ou chegou ao gol
            canvas.coords(bola_item, x, max(y, altura_max))  # garante que não passe do limite
            status.config(text="⚽ GOL!")  # mensagem final

    mover_bola()  # Inicia a animação
# ===========================
# Botão de chute
# ===========================
btn_chutar = tk.Button(
    root,
    text="Chutar ⚽",  # Texto do botão
    font=("Arial", 14, "bold"),  # Fonte e tamanho
    command=chutar,  # Quando o botão for clicado, chama a função chutar()
    bg="#fca311",  # Cor de fundo do botão
    fg="black"  # Cor do texto
)
btn_chutar.pack(pady=10)  # Posiciona o botão na janela

# ===========================
# Inicia o loop principal
# ===========================
root.mainloop()  # Mantém a janela aberta e atualiza a interface continuamente
