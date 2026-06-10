============================================================================
 TRABALHO DE PROCESSAMENTO DE IMAGENS - README
============================================================================

Aluno(a): ___________________________________
Disciplina: _________________________________

----------------------------------------------------------------------------
1. O QUE O PROGRAMA FAZ
----------------------------------------------------------------------------
Um unico programa (processamento_imagens.py), acionado por MENU, implementa
as quatro funcionalidades pedidas:

  1) Tons de cinza com CLUSTERIZACAO.
     Converte a imagem para cinza e agrupa os tons a cada 4 niveis
     (256 tons -> no maximo 64 tons). Mostra a contagem de tons antes/depois.

  2) SUBTRACAO de imagens para detectar o corpo.
     Subtrai a imagem do fundo (parede) da imagem com a pessoa, binariza por
     um limiar empirico e desenha um RETANGULO VERMELHO sobre o corpo
     detectado. No modo grafico ha um slider para ajustar o limiar ao vivo.

  3) Filtro HIGH-BOOST (implementacao propria) x filtro PASSA-ALTA.
     A funcao "meu_filtro_high_boost" faz:  imagem + A*(imagem - suavizada).
     Compara o resultado com o filtro passa-alta (laplaciano 3x3).
     Ha um slider para variar o fator A.

  4) TEOREMA DA CONVOLUCAO (ganho computacional).
     Aplica o mesmo filtro pela convolucao no DOMINIO ESPACIAL e pela
     multiplicacao no DOMINIO DA FREQUENCIA (FFT), exibe os dois tempos, a
     aceleracao e a diferenca numerica entre os resultados (~0, comprovando o
     teorema). Tambem plota um grafico de tempo x tamanho do kernel.

Todas as imagens de saida sao gravadas automaticamente na pasta "resultados/".

----------------------------------------------------------------------------
2. REQUISITOS
----------------------------------------------------------------------------
- Python 3.9 ou superior.
- Bibliotecas: opencv-python, numpy, scipy, matplotlib.

Instalacao das bibliotecas (uma vez):

    pip install -r requirements.txt

ou, individualmente:

    pip install opencv-python numpy scipy matplotlib

----------------------------------------------------------------------------
3. COMO EXECUTAR
----------------------------------------------------------------------------
Pelo terminal, na pasta do projeto:

    python processamento_imagens.py

Sera exibido o menu. Digite 1, 2, 3 ou 4 para rodar cada exercicio e 0 para
sair. Cada exercicio abre uma janela com os resultados; FECHE a janela para
voltar ao menu.

Para rodar um exercicio diretamente (sem menu):

    python processamento_imagens.py 1
    python processamento_imagens.py 2
    python processamento_imagens.py 3
    python processamento_imagens.py 4

----------------------------------------------------------------------------
4. USANDO SUAS PROPRIAS IMAGENS
----------------------------------------------------------------------------
- Exercicios 1, 3 e 4: coloque uma foto chamada "entrada.jpg" na pasta do
  programa. Se o arquivo nao existir, o programa gera uma imagem de teste
  automaticamente (assim ele sempre roda).

- Exercicio 2 (OBRIGATORIO usar suas fotos para a entrega):
  Como tirar as fotos (conforme o enunciado):
    a) Escolha uma cena com uma PAREDE de fundo com pouca variacao de cor.
    b) Posicione a camera em um local FIXO, apontada para a parede. NAO mova
       a camera entre as duas fotos.
    c) Foto 1: somente a parede (sem voce)  -> salve como  fundo.jpg
    d) Foto 2: voce, de BRACOS ABERTOS, com a parede ao fundo -> salve como
       pessoa.jpg
  Coloque "fundo.jpg" e "pessoa.jpg" na pasta do programa e rode o exercicio 2.
  Ajuste o slider "Limiar" ate que apenas o seu corpo fique branco na imagem
  binarizada (esse e o limiar "determinado empiricamente"). Se o arquivo nao
  existir, o programa usa um par sintetico apenas para demonstracao.

Observacao: as duas imagens devem ter o mesmo tamanho. Se forem diferentes, o
programa redimensiona a foto da pessoa para o tamanho do fundo.

----------------------------------------------------------------------------
5. GERANDO O EXECUTAVEL
----------------------------------------------------------------------------
O executavel e especifico do sistema operacional (um .exe so roda no Windows,
etc.), por isso ele deve ser gerado NO MESMO sistema em que sera usado.

Passos (no terminal, na pasta do projeto):

    pip install pyinstaller
    pyinstaller --onefile --name processamento_imagens processamento_imagens.py

O executavel sera criado dentro da pasta "dist/":
    - Windows: dist\processamento_imagens.exe
    - Linux/Mac: dist/processamento_imagens

Rode o executavel a partir de um terminal (ele usa um menu de texto).

----------------------------------------------------------------------------
6. VIDEO DE DEMONSTRACAO
----------------------------------------------------------------------------
Grave a tela (ex.: OBS Studio, Xbox Game Bar no Windows, ou a gravacao de
tela do sistema) executando o programa e mostrando:
  - O menu e a execucao dos 4 exercicios.
  - No exercicio 2, suas fotos reais e o ajuste do limiar pelo slider ate
    aparecer o retangulo vermelho no seu corpo.
  - No exercicio 4, os tempos impressos no terminal e o grafico comparativo.
Salve o video junto com a entrega.

----------------------------------------------------------------------------
7. ARQUIVOS DA ENTREGA
----------------------------------------------------------------------------
  processamento_imagens.py  -> codigo-fonte (todas as 4 funcionalidades)
  README.txt                -> este arquivo
  requirements.txt          -> lista de dependencias
  resultados/               -> imagens geradas pelo programa (criada ao rodar)
  dist/...                  -> executavel (gerado por voce, secao 5)
  video.*                   -> video de demonstracao (gravado por voce)
============================================================================
