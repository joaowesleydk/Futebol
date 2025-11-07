# ⚽ Batalha das Lendas RPG ⚽

Um jogo de RPG de futebol épico onde você enfrenta lendas do futebol mundial em batalhas emocionantes!

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![Status](https://img.shields.io/badge/Status-Completo-success.svg)

## 🎮 Sobre o Jogo

Batalha das Lendas RPG é um jogo onde você assume o papel de um jogador escolhido para restaurar a honra do futebol. Enfrente craques lendários como Cristiano Ronaldo, Messi, Ronaldinho, Maradona e o lendário Pelé em batalhas épicas baseadas em dados D20!

### 🌟 Características Principais

- **História Épica**: Duas histórias narradas por IA com vozes realistas
- **Sistema de Batalha**: Combate baseado em dados D20 com diferentes resultados
- **Animações Dinâmicas**: Animações de chute que mudam baseadas no resultado do dado
- **Progressão de Níveis**: Enfrente 6 lendas do futebol, cada uma mais forte que a anterior
- **Sistema de Itens**: Colete energéticos, chutes especiais e escudos
- **Efeitos Sonoros**: Sons imersivos para cada ação do jogo
- **Easter Egg Secreto**: Descubra o poder oculto do Flamengo! 🔥

## 🎯 Como Jogar

### Controles Básicos
- **⚽ Chutar**: Ataque principal - consome energia mas causa dano
- **🛡️ Defender**: Reduz o dano do próximo ataque inimigo
- **🎒 Itens**: Use itens coletados para se curar ou causar dano extra

### Sistema de Dados
- **Dado 20**: Golaço crítico no ângulo! 🌀
- **Dado 15-19**: Chute certeiro no ângulo 🚀
- **Dado 10-14**: Gol normal no centro ⚽
- **Dado 5-9**: Chute fraco que quase não entra 🥅
- **Dado 1-4**: Errou completamente! ❌

### Adversários
1. **Gabi Gol** - Iniciante amigável
2. **Cristiano Ronaldo** - O fenômeno português
3. **Lionel Messi** - O gênio argentino
4. **Ronaldinho Gaúcho** - O mago do futebol
5. **Diego Maradona** - A lenda argentina
6. **Pelé** - O Rei do Futebol (Boss Final)

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.7 ou superior
- Tkinter (geralmente incluído com Python)
- PIL/Pillow (para animações)

### Instalação Rápida

1. **Clone ou baixe o projeto**
```bash
git clone [seu-repositorio]
cd Futebol-main
```

2. **Instale as dependências**
```bash
python instalar_pillow.py
```

3. **Execute o jogo**
```bash
python main.py
```

### Instalação Manual das Dependências
```bash
pip install Pillow requests pygame
```

## 🎨 Recursos Visuais

### Animações
- **Jogador**: Sprites animados de chute com 3 frames
- **Bola**: Trajetória dinâmica baseada no resultado do dado
- **Campo**: Cenário de fundo com gol realista
- **Efeitos**: Animações suaves e responsivas

### Interface
- **Tela Cheia**: Experiência imersiva em fullscreen
- **Barras de Vida**: Visualização clara da energia dos jogadores
- **Inventário**: Sistema visual de itens coletados
- **Dados Animados**: Rolagem visual do D20

## 🎵 Sistema de Áudio

### Efeitos Sonoros
- **Chute**: Som realista de chute na bola
- **Defesa**: Som de defesa bem-sucedida
- **Itens**: Som especial ao ganhar/usar itens
- **Vitória/Derrota**: Fanfarras épicas
- **Cliques**: Feedback sonoro da interface

### Narração por IA
- **História 1**: Narração épica da queda do futebol
- **História 2**: Narração sobre o retorno das lendas
- **Tecnologia**: API ElevenLabs para vozes realistas

## 🔥 Easter Eggs

### Código Secreto: "Flamengo"
Digite "flamengo" como nome do jogador para ativar:
- **Energia**: 200 (dobro do normal)
- **Chute**: 20 (poder máximo)
- **Defesa**: 15 (quase invencível)
- **Precisão**: 100% (nunca erra)
- **Dado**: Sempre tira 20 (crítico garantido)

*"Uma vez Flamengo, sempre Flamengo!" 🔴⚫*

## 📁 Estrutura do Projeto

```
Futebol-main/
├── assets/
│   ├── animacoes/
│   │   ├── chute/          # Frames de animação
│   │   ├── bola.png        # Sprite da bola
│   │   └── jogador.png     # Sprite do jogador
│   ├── imagens/
│   │   └── gol.png         # Cenário do campo
│   └── sons/               # Efeitos sonoros
├── utils/
│   └── helpers_fixed.py    # Funções de áudio e narração
├── main.py                 # Arquivo principal
├── gui_simple.py          # Interface do jogo
├── game_logic_simple.py   # Lógica de batalha
├── models.py              # Classes dos personagens
└── README.md              # Este arquivo
```

## 🏆 Objetivos do Jogo

### Objetivo Principal
Derrote todas as 6 lendas do futebol para restaurar a honra do esporte e se tornar o **Campeão Supremo**!

### Objetivos Secundários
- Colete todos os tipos de itens
- Descubra o easter egg secreto
- Complete o jogo sem usar itens (Desafio Hardcore)
- Teste diferentes estratégias de batalha

## 🛠️ Tecnologias Utilizadas

- **Python 3.7+**: Linguagem principal
- **Tkinter**: Interface gráfica nativa
- **PIL/Pillow**: Processamento de imagens
- **Pygame**: Sistema de áudio
- **ElevenLabs API**: Narração por IA
- **Threading**: Processamento assíncrono de áudio

## 👥 Créditos

**Desenvolvido por:**
- João Wesley D. Kind
- Cristian Andrade  
- Nycollas Augusto

**Agradecimentos Especiais:**
- Comunidade Python
- Lendas do futebol que inspiraram o jogo
- Torcedores do Flamengo pelo easter egg 🔥

## 📝 Licença

Este projeto é open source e está disponível sob a licença MIT.

## 🐛 Suporte

Encontrou um bug ou tem uma sugestão? 
- Abra uma issue no repositório
- Entre em contato com os desenvolvedores

---

**⚽ Que a força do futebol esteja com você! ⚽**

*"O futebol é a única religião que não tem ateus." - Pelé*