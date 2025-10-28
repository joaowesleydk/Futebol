# utils/energybar.py

from tkinter import Canvas

class BarraEnergia:
    def __init__(self, master, x, y, largura=200, altura=25):
        self.master = master
        self.largura = largura
        self.altura = altura
        self.canvas = Canvas(master, width=largura, height=altura, highlightthickness=0, bg="#eeeeee")
        self.canvas.place(x=x, y=y)
        self.barra = self.canvas.create_rectangle(0, 0, largura, altura, fill="lime", width=0)

    def atualizar(self, valor):
        valor = max(0, min(100, valor))
        nova_largura = (valor / 100) * self.largura
        cor = "lime" if valor > 60 else "yellow" if valor > 30 else "red"
        self.canvas.coords(self.barra, 0, 0, nova_largura, self.altura)
        self.canvas.itemconfig(self.barra, fill=cor)
