import pygame
pygame.mixer.init()
pygame.mixer.music.load("assets/sons/teste.mp3")  # usa qualquer mp3 pra testar
pygame.mixer.music.play()
input("Pressione ENTER para parar...")
pygame.mixer.music.stop()
