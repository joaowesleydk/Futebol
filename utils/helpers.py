import pygame
import os
import requests
import threading

# ==============================
# 🎧 CONFIGURAÇÃO E INICIALIZAÇÃO DO MIXER
# ==============================

try:
    # Preconfiguração com buffer e frequência otimizados
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.set_num_channels(16)  # permite vários sons simultâneos
    print(f"[DEBUG] Mixer iniciado com sucesso: {pygame.mixer.get_init()}")
except Exception as e:
    print(f"[AVISO] Falha ao inicializar mixer: {e}")

# Caminho base do projeto e da pasta de sons
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SONS_DIR = os.path.join(BASE_DIR, "assets", "sons")

# ==============================
# 🔊 FUNÇÕES DE SOM
# ==============================

def tocar_som(nome_arquivo, volume=1.0):
    """Toca um som curto (efeito)."""
    caminho = os.path.join(SONS_DIR, nome_arquivo)

    if not os.path.exists(caminho):
        print(f"[AVISO] Som não encontrado: {caminho}")
        return

    try:
        som = pygame.mixer.Sound(caminho)
        som.set_volume(volume)
        som.play(maxtime=7000)  # evita travamento de sons longos
        print(f"[DEBUG] Tocando som: {nome_arquivo}")
    except Exception as e:
        print(f"[ERRO] Falha ao tocar som {nome_arquivo}: {e}")


def tocar_musica_fundo(nome_arquivo, volume=0.3):
    """Toca música de fundo em loop (sem interferir nos efeitos)."""
    caminho = os.path.join(SONS_DIR, nome_arquivo)

    if not os.path.exists(caminho):
        print(f"[AVISO] Música de fundo não encontrada: {caminho}")
        return

    try:
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
        print(f"[DEBUG] Música de fundo iniciada: {nome_arquivo}")
    except Exception as e:
        print(f"[ERRO] Falha ao tocar música de fundo ({nome_arquivo}): {e}")


def parar_musica_fundo():
    """Para a música de fundo."""
    try:
        pygame.mixer.music.stop()
        print("[DEBUG] Música de fundo parada.")
    except Exception as e:
        print(f"[ERRO] Falha ao parar música de fundo: {e}")

# ==============================
# 🧠 NARRAÇÃO (IA ElevenLabs)
# ==============================

ELEVEN_API_KEY = "sk_c318413ae68d0c0d1f3be8be497d1004401d2e43c5ce3b19"
ELEVEN_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

def narrar_texto(texto):
    """Gera e toca narração com voz da ElevenLabs sem interromper a música de fundo."""
    def narrar():
        try:
            print("[DEBUG] Gerando narração via ElevenLabs...")
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"

            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVEN_API_KEY
            }

            data = {
                "text": texto,
                "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}
            }

            resposta = requests.post(url, headers=headers, json=data)

            if resposta.status_code == 200:
                caminho_audio = os.path.join(SONS_DIR, "narracao_temp.mp3")
                with open(caminho_audio, "wb") as f:
                    f.write(resposta.content)
                print("[DEBUG] Narração gerada com sucesso!")

                # Tocar a narração em um canal separado
                canal = pygame.mixer.find_channel(True)
                som = pygame.mixer.Sound(caminho_audio)
                som.set_volume(0.9)
                canal.play(som)
                print("[DEBUG] Narração sendo reproduzida...")

            else:
                print(f"[ERRO] Falha ao gerar voz ({resposta.status_code}): {resposta.text}")

        except Exception as e:
            print(f"[ERRO] Falha na narração: {e}")

    threading.Thread(target=narrar, daemon=True).start()
