# Processamento de Imagens — Tarefa Avaliativa 1 PARTE 2

Implementação de técnicas de pré-processamento de imagens em Python.

**Alunos:** Diogo Ruis, Marcos Henrique  
**Disciplina:** Processamento de Imagens / Visão Computacional

---

## O que o programa faz

Um único programa (`processamento_imagens.py`), acionado por menu, implementa 4 funcionalidades:

### 1) Tons de cinza com Clusterização
Converte a imagem para tons de cinza e agrupa os tons a cada 4 níveis.  
Exemplo: 256 tons resultam em no máximo 64 tons distintos.

### 2) Subtração de imagens — Detecção do corpo
Subtrai a imagem do fundo (parede) da imagem com a pessoa, binariza por um limiar empírico e desenha um **retângulo vermelho** sobre o corpo detectado.  
No modo gráfico há um slider para ajustar o limiar ao vivo.

### 3) Filtro High-Boost (implementação própria) x Filtro Passa-Alta
Implementação própria do filtro high-boost:
```
high_boost = imagem + A * (imagem - suavizada)
```
Comparado com o filtro passa-alta clássico (laplaciano 3x3). Slider para variar o fator A.

### 4) Teorema da Convolução — Ganho computacional
Aplica o mesmo filtro por convolução no **domínio espacial** e por multiplicação no **domínio da frequência (FFT)**, exibindo os dois tempos e a aceleração obtida.

---

## Requisitos

- Python 3.9 ou superior
- Bibliotecas: `opencv-python`, `numpy`, `scipy`, `matplotlib`

Instalação:
```bash
pip install -r requirements.txt
```

---

## Como executar

```bash
python processamento_imagens.py
```

Ou para rodar um exercício diretamente:
```bash
python processamento_imagens.py 1
python processamento_imagens.py 2
python processamento_imagens.py 3
python processamento_imagens.py 4
```

---

## Usando suas próprias imagens

| Exercício | Arquivo esperado | Observação |
|-----------|-----------------|------------|
| 1, 3 e 4 | `entrada.jpg` | Se não existir, gera imagem sintética automaticamente |
| 2 | `fundo.jpg` + `pessoa.jpg` | Fotos com câmera fixa (parede sozinha e você de braços abertos) |

---

## Gerando o executável

```bash
pip install pyinstaller
pyinstaller --onefile --name processamento_imagens processamento_imagens.py
```

O executável será criado em `dist/processamento_imagens.exe` (Windows).

---

## Arquivos do projeto

```
projeto/
├── processamento_imagens.py   — código-fonte principal
├── requirements.txt           — dependências
├── README.md                  — este arquivo
├── resultados/                — imagens geradas ao executar
└── dist/                      — executável gerado pelo PyInstaller
```
