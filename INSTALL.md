# 🚀 Guia de Instalação - Batalha das Lendas RPG

## 📋 Pré-requisitos

### Sistema Operacional
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+)

### Software Necessário
- **Python 3.7 ou superior**
- **pip** (gerenciador de pacotes Python)

## 🔧 Instalação Passo a Passo

### 1️⃣ Verificar Python
```bash
python --version
# ou
python3 --version
```
*Deve mostrar Python 3.7 ou superior*

### 2️⃣ Baixar o Projeto
- Baixe o arquivo ZIP do projeto
- Extraia para uma pasta de sua escolha
- Ou clone via Git:
```bash
git clone [url-do-repositorio]
cd Futebol-main
```

### 3️⃣ Instalar Dependências

#### Opção A - Automática (Recomendada)
```bash
python instalar_pillow.py
```

#### Opção B - Manual
```bash
pip install -r requirements.txt
```

#### Opção C - Individual
```bash
pip install Pillow
pip install requests
pip install pygame
```

### 4️⃣ Executar o Jogo
```bash
python main.py
```

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'PIL'"
**Solução:**
```bash
pip install Pillow
```

### Erro: "No module named 'tkinter'"
**Linux/Ubuntu:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

### Erro de Áudio/Som
**Instalar pygame:**
```bash
pip install pygame
```

### Erro de Permissão (Linux/macOS)
```bash
sudo pip install [pacote]
# ou usar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### Erro de Permissão (Windows)
- Execute o terminal como Administrador
- Ou use: `pip install --user [pacote]`

## 🎮 Primeira Execução

1. **Execute o jogo:**
   ```bash
   python main.py
   ```

2. **Aguarde as histórias serem narradas**

3. **Digite seu nome** (ou "flamengo" para easter egg)

4. **Divirta-se!** ⚽

## 📁 Estrutura Esperada

Após a instalação, sua pasta deve conter:
```
Futebol-main/
├── assets/           ✅ Imagens e sons
├── utils/            ✅ Utilitários
├── main.py           ✅ Arquivo principal
├── gui_simple.py     ✅ Interface
├── models.py         ✅ Classes
├── requirements.txt  ✅ Dependências
└── README.md         ✅ Documentação
```

## 🔍 Verificação da Instalação

Execute este teste rápido:
```python
# teste_instalacao.py
try:
    import tkinter
    print("✅ Tkinter OK")
    
    from PIL import Image
    print("✅ Pillow OK")
    
    import pygame
    print("✅ Pygame OK")
    
    import requests
    print("✅ Requests OK")
    
    print("\n🎉 Todas as dependências instaladas com sucesso!")
    print("Execute: python main.py")
    
except ImportError as e:
    print(f"❌ Erro: {e}")
    print("Execute: pip install -r requirements.txt")
```

## 📞 Suporte

Se ainda tiver problemas:
1. Verifique se Python 3.7+ está instalado
2. Tente reinstalar as dependências
3. Execute como administrador (se necessário)
4. Entre em contato com os desenvolvedores

---

**⚽ Boa sorte e bom jogo! ⚽**