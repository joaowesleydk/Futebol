import tkinter as tk
from PIL import Image, ImageTk

# ===========================
# Janela principal
# ===========================
root = tk.Tk()
root.title("Chute no Gol")
root.geometry("700x400")
root.configure(bg="#0b132b")

# Canvas do campo
canvas = tk.Canvas(root, width=700, height=400, bg="#1c2541", highlightthickness=0)
canvas.pack()

# ===========================
# Carregar imagens
# ===========================
gol_img = Image.open("assets/imagens/gol.png").resize((300, 200))
gol_photo = ImageTk.PhotoImage(gol_img)
gol_item = canvas.create_image(350, 150, image=gol_photo)

jogador_img = Image.open("assets/animacoes/jogador.png").resize((80, 120))
jogador_photo = ImageTk.PhotoImage(jogador_img)
jogador_item = canvas.create_image(350, 300, image=jogador_photo)

bola_img = Image.open("assets/animacoes/bola.png").resize((40, 40))
bola_photo = ImageTk.PhotoImage(bola_img)
bola_item = canvas.create_image(350, 270, image=bola_photo)

# ===========================
# Status
# ===========================
status = tk.Label(root, text="", font=("Arial", 16), bg="#0b132b", fg="white")
status.pack(pady=10)

# ===========================
# Função de chute com subida
# ===========================
def chutar():
    x, y = 350, 270  # posição inicial da bola

    def mover_bola():
        nonlocal x, y
        if x < 550:  # posição final X
            x += 10  # velocidade horizontal
            if y > 100:  # sobe até y=100
                y -= 5  # velocidade vertical
            canvas.coords(bola_item, x, y)
            root.after(50, mover_bola)
        else:
            status.config(text="⚽ GOL!")

    mover_bola()

# ===========================
# Botão de chute
# ===========================
btn_chutar = tk.Button(root, text="Chutar ⚽", font=("Arial", 14, "bold"),
                       command=chutar, bg="#fca311", fg="black")
btn_chutar.pack(pady=10)

root.mainloop()
