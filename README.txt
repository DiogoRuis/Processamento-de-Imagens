============================================================================
 TRABALHO DE PROCESSAMENTO DE IMAGENS - readme.txt
============================================================================

 Alunos: Diogo Ruis, Marcos Henrique
 Disciplina: Processamento de Imagens / Visao Computacional

----------------------------------------------------------------------------
1. O QUE CADA EXERCICIO FAZ
----------------------------------------------------------------------------
Um unico programa (processamento_imagens.py), acionado por MENU, implementa
as quatro funcionalidades pedidas:

  1) TONS DE CINZA com CLUSTERIZACAO.
     Converte a imagem colorida para tons de cinza e agrupa os tons a cada 4
     niveis, usando: nivel = (cinza // 4) * 4. Assim uma imagem de 256 tons
     passa a ter no maximo 64 tons. O programa imprime a quantidade de tons
     distintos ANTES e DEPOIS do agrupamento.
     Saidas: ex1_cinza.png, ex1_clusterizada.png.

  2) SUBTRACAO de imagens para detectar o corpo.
     Converte as duas fotos (parede e pessoa) para cinza e faz a subtracao
     COM SINAL (fundo - pessoa). Como o corpo (roupa) e mais escuro que a
     parede, isso realca o corpo e descarta variacoes que apenas clareiam a
     cena (diferenca de iluminacao entre as fotos / sombra que sumiu do
     fundo). Em seguida binariza com um LIMIAR empirico (ajustavel), limpa
     com operacoes morfologicas e desenha um RETANGULO VERMELHO sobre toda a
     regiao do corpo detectado (incluindo as maos, que tem pouca diferenca).
     Saidas: ex2_diferenca.png, ex2_binarizada.png, ex2_resultado.png.

  3) Filtro HIGH-BOOST (implementacao propria) x filtro PASSA-ALTA.
     Funcao propria "meu_filtro_high_boost":  resultado = imagem + A*(imagem
     - suavizada), onde (imagem - suavizada) e a mascara de altas frequencias.
     Compara com o filtro PASSA-ALTA classico (kernel laplaciano 3x3). O
     passa-alta deixa basicamente as BORDAS; o high-boost mantem a imagem
     original, porem mais nitida (A controla a intensidade do realce).
     Saidas: ex3_cinza.png, ex3_passa_alta.png, ex3_high_boost.png.

  4) TEOREMA DA CONVOLUCAO (ganho computacional).
     Aplica o MESMO filtro de duas formas: (a) convolucao no DOMINIO ESPACIAL
     e (b) multiplicacao no DOMINIO DA FREQUENCIA (FFT). Exibe o tempo das
     duas, a aceleracao obtida e a diferenca numerica entre os resultados
     (~0, comprovando que as duas abordagens sao equivalentes). Tambem faz
     uma varredura de tamanhos de kernel para mostrar que, no espacial, o
     tempo cresce com o tamanho do kernel, enquanto na FFT fica quase
     constante. Saidas: ex4_espacial.png, ex4_frequencia.png.

Todas as imagens de saida sao gravadas na pasta "resultados/" (criada
automaticamente).

----------------------------------------------------------------------------
2. ARQUIVOS NECESSARIOS (na MESMA pasta do programa/executavel)
----------------------------------------------------------------------------
  entrada.jpg  -> imagem usada nos exercicios 1, 3 e 4
  fundo.jpg    -> foto so da parede (exercicio 2)
  pessoa.jpg   -> foto da pessoa de bracos abertos, com a parede ao fundo (ex.2)

Obs.: se "entrada.jpg" nao existir, o programa gera uma imagem de teste.
Se "fundo.jpg"/"pessoa.jpg" nao existirem, usa um par sintetico de exemplo.

----------------------------------------------------------------------------
3. COMO EXECUTAR - PELO EXECUTAVEL (Windows)
----------------------------------------------------------------------------
IMPORTANTE: o executavel NAO abre as janelas dos graficos. Ele PROCESSA as
imagens e SALVA os resultados na pasta "resultados/". Para ver o resultado,
abra essa pasta e veja as imagens geradas.

Passo a passo:
1) Garanta que entrada.jpg, fundo.jpg e pessoa.jpg estejam na MESMA pasta do
   arquivo processamento_imagens.exe.
2) Rode o processamento_imagens.exe (duplo clique ou pelo terminal).
3) Digite 1, 2, 3 ou 4 para rodar cada exercicio e 0 para sair. As mensagens
   (ex.: contagem de tons no ex.1, tempos no ex.4) aparecem no terminal e as
   imagens sao salvas em "resultados/".

(O aviso "FigureCanvasAgg is non-interactive" e normal no executavel: significa
apenas que ele nao exibe janelas, somente salva os arquivos.)

----------------------------------------------------------------------------
4. COMO EXECUTAR - PELO CODIGO-FONTE (Python / VS Code)
----------------------------------------------------------------------------
Rodando pelo Python, ALEM de salvar os arquivos, o programa ABRE as janelas
com os resultados e com os controles deslizantes (slider do LIMIAR no ex.2 e
do fator A no ex.3) para ajuste em tempo real.

Requisitos:
  - Python 3.9 ou superior.
  - Bibliotecas: opencv-python, numpy, scipy, matplotlib.

Instalacao das bibliotecas (uma vez):
    pip install -r requirements.txt
ou:
    pip install opencv-python numpy scipy matplotlib

Execucao:
    python processamento_imagens.py

Sera exibido o menu. Digite 1, 2, 3 ou 4 para rodar cada exercicio e 0 para
sair. Cada exercicio abre uma janela; FECHE a janela para voltar ao menu.

Para rodar um exercicio diretamente (sem menu):
    python processamento_imagens.py 1
    python processamento_imagens.py 2
    python processamento_imagens.py 3
    python processamento_imagens.py 4

----------------------------------------------------------------------------
5. DICAS DO EXERCICIO 2 (subtracao)
----------------------------------------------------------------------------
- As duas fotos (fundo.jpg e pessoa.jpg) devem ser tiradas com a CAMERA FIXA,
  apontada para uma parede de cor uniforme: uma so da parede e a outra com
  voce de bracos abertos.
- Rodando pelo Python, use o slider "Limiar" para ajustar ate que apenas o
  corpo fique branco na imagem binarizada (limiar determinado empiricamente).
- As duas imagens devem ter o mesmo tamanho. Se forem diferentes, o programa
  redimensiona a foto da pessoa para o tamanho do fundo.

----------------------------------------------------------------------------
6. COMO GERAR O EXECUTAVEL (caso precise gerar de novo)
----------------------------------------------------------------------------
    pip install pyinstaller
    pyinstaller --onefile --name processamento_imagens processamento_imagens.py

O executavel sera criado em: dist\processamento_imagens.exe
Lembre de copiar entrada.jpg, fundo.jpg e pessoa.jpg para a mesma pasta do .exe.

----------------------------------------------------------------------------
7. ARQUIVOS DA ENTREGA
----------------------------------------------------------------------------
  processamento_imagens.py  -> codigo-fonte (todas as 4 funcionalidades)
  processamento_imagens.exe -> executavel (Windows)
  readme.txt                -> este arquivo
  requirements.txt          -> lista de dependencias
  entrada.jpg / fundo.jpg / pessoa.jpg -> imagens usadas
  video.*                   -> video demonstrando o funcionamento
============================================================================
