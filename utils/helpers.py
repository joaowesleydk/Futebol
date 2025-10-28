import random
import time
import threading
import os
import tkinter as tk  # ✅ necessário para animações de barra e piscar

# ---------------------------------
# SISTEMA DE SONS (com pygame)
# ---------------------------------
try:
    import pygame
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except Exception:
    SOUND_AVAILABLE = False
    print("[AVISO] Sons desativados (pygame não encontrado ou não inicializado).")


# ---------------------------------
# FUNÇÕES DE SOM
# ---------------------------------
def tocar_som(path, volume=0.6):
    """Toca um som curto (efeito)."""
    if not SOUND_AVAILABLE:
        print(f"[⚠️ Som ignorado] pygame indisponível → {path}")
        return
    if not os.path.exists(path):
        print(f"[⚠️ Som não encontrado]: {path}")
        return

    try:
        som = pygame.mixer.Sound(path)
        som.set_volume(volume)
        som.play()
    except Exception as e:
        print(f"[Erro ao tocar som]: {e}")

def tocar_musica_fundo(path, volume=0.25, loop=True):
    """Toca uma música de fundo em loop."""
    if not SOUND_AVAILABLE:
        print(f"[⚠️ Música ignorada] pygame indisponível → {path}")
        return
    if not os.path.exists(path):
        print(f"[⚠️ Música não encontrada]: {path}")
        return

    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1 if loop else 0)
    except Exception as e:
        print(f"[Erro ao tocar música]: {e}")

def parar_musica_fundo():
    """Para a música de fundo."""
    if not SOUND_AVAILABLE:
        return
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass

# ---------------------------------
# FUNÇÕES DE LÓGICA AUXILIAR
# ---------------------------------
def rolar_dado(sides=20):
    """Retorna um valor aleatório de 1 até o número de lados."""
    return random.randint(1, sides)

# ---------------------------------
# ANIMAÇÃO DE BARRA (ENERGIA)
# ---------------------------------
def anima_bar(progressbar, start, end, duration=0.3, steps=15):
    """
    Faz uma animação suave da barra de energia.
    start -> valor inicial
    end -> valor final
    """
    delta = (end - start) / steps
    delay = duration / steps

    def runner():
        val = start
        for _ in range(steps):
            val += delta
            try:
                progressbar["value"] = max(0, min(100, val))
            except tk.TclError:
                break  # caso o widget seja destruído
            time.sleep(delay)

    threading.Thread(target=runner, daemon=True).start()

# ---------------------------------
# EFEITOS VISUAIS (OPCIONAL)
# ---------------------------------
def piscar_widget(widget, cor_original, cor_flash="#ffff66", vezes=2, intervalo=0.15):
    """
    Faz o widget piscar (efeito visual divertido).
    Ideal para quando marca gol, toma dano ou vence batalha.
    """
    def animacao():
        for _ in range(vezes):
            try:
                widget.config(bg=cor_flash)
                time.sleep(intervalo)
                widget.config(bg=cor_original)
                time.sleep(intervalo)
            except tk.TclError:
                break

    threading.Thread(target=animacao, daemon=True).start()
