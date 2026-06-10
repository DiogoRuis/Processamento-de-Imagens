# -*- coding: utf-8 -*-
"""
============================================================================
 TRABALHO DE PROCESSAMENTO DE IMAGENS / VISAO COMPUTACIONAL
============================================================================
 Aluno(a): ___________________________________
 Disciplina: _________________________________

 Programa unico (acionado por menu) que implementa 4 funcionalidades:

   1) Conversao para tons de cinza com CLUSTERIZACAO (agrupamento a cada
      N tons -> com N=4 uma imagem de 256 tons passa a ter no max. 64 tons).
   2) SUBTRACAO de duas imagens (parede x voce) para realcar o corpo,
      binarizacao por limiar empirico e desenho de um RETANGULO VERMELHO
      sobre a regiao detectada.
   3) Filtro HIGH-BOOST (implementacao propria) comparado com o filtro
      PASSA-ALTA classico.
   4) TEOREMA DA CONVOLUCAO: comparacao do tempo de processamento entre a
      convolucao no dominio espacial e a filtragem no dominio da frequencia.

 Dependencias: opencv-python, numpy, scipy, matplotlib
 Execucao:     python processamento_imagens.py
               (ou "python processamento_imagens.py 1|2|3|4" p/ um exercicio)
============================================================================
"""

import os
import sys
import time

import numpy as np
import cv2
import matplotlib

# --- Deteccao de ambiente grafico --------------------------------------------
# Em uma maquina comum (Windows/Linux com tela) o programa abre janelas e usa
# controles deslizantes (sliders). Em ambiente sem tela (servidor/headless),
# usa o backend "Agg" e salva as figuras em arquivo em vez de exibi-las.
if not os.environ.get("DISPLAY") and os.name != "nt":
    matplotlib.use("Agg")
    MODO_INTERATIVO = False
else:
    MODO_INTERATIVO = True

import matplotlib.pyplot as plt          # noqa: E402
from matplotlib.widgets import Slider     # noqa: E402
from scipy import signal                  # noqa: E402

PASTA_SAIDA = "resultados"
os.makedirs(PASTA_SAIDA, exist_ok=True)


# =============================================================================
# UTILIDADES GERAIS
# =============================================================================
def bgr_para_rgb(img):
    """OpenCV trabalha em BGR; o matplotlib espera RGB."""
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def exibir_ou_salvar(fig, nome_arquivo):
    """Exibe a figura (modo interativo) ou salva em disco (modo headless)."""
    if MODO_INTERATIVO:
        plt.show()
    else:
        caminho = os.path.join(PASTA_SAIDA, nome_arquivo)
        fig.savefig(caminho, dpi=110, bbox_inches="tight")
        plt.close(fig)
        print(f"[salvo] {caminho}")


def gerar_imagem_sintetica(altura=480, largura=640):
    """Cria uma imagem colorida sintetica (gradientes + formas + texto + ruido)
    para que os exercicios 1, 3 e 4 funcionem mesmo sem uma foto do usuario."""
    img = np.zeros((altura, largura, 3), dtype=np.uint8)
    # gradiente azul na vertical
    grad_y = (40 + 160 * np.arange(altura) / altura).astype(np.uint8)
    img[:, :, 0] = grad_y[:, None]
    # gradiente vermelho na horizontal
    grad_x = (120 * np.arange(largura) / largura).astype(np.uint8)
    img[:, :, 2] = grad_x[None, :]
    img[:, :, 1] = 80
    # formas geometricas (geram bordas para os filtros)
    cv2.circle(img, (160, 160), 80, (255, 255, 255), -1)
    cv2.rectangle(img, (400, 90), (560, 250), (0, 0, 0), -1)
    cv2.line(img, (0, 460), (640, 300), (0, 255, 255), 5)
    cv2.putText(img, "TESTE", (190, 360), cv2.FONT_HERSHEY_SIMPLEX, 3,
                (10, 10, 10), 8)
    # ruido leve
    ruido = np.random.normal(0, 12, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + ruido, 0, 255).astype(np.uint8)
    return img


def carregar_ou_gerar_imagem(caminho="entrada.jpg"):
    """Carrega 'entrada.jpg' (se existir) ou gera uma imagem de teste.
    Troque o arquivo 'entrada.jpg' pela sua imagem para usar uma foto real."""
    if os.path.exists(caminho):
        img = cv2.imread(caminho, cv2.IMREAD_COLOR)
        if img is not None:
            print(f"[info] Usando imagem '{caminho}'.")
            return img
    print(f"[info] '{caminho}' nao encontrado -> gerando imagem sintetica.")
    return gerar_imagem_sintetica()


# =============================================================================
# EXERCICIO 1 - TONS DE CINZA COM CLUSTERIZACAO
# =============================================================================
def exercicio1_clusterizacao(tamanho_grupo=4):
    """Converte para cinza e agrupa os tons a cada 'tamanho_grupo' niveis.

    Tecnica: divisao inteira pelo tamanho do grupo e multiplicacao de volta.
        nivel_agrupado = (cinza // tamanho_grupo) * tamanho_grupo
    Assim os tons 0..3 viram 0, 4..7 viram 4, etc. Com tamanho_grupo=4 e
    256 tons originais, restam no maximo 256/4 = 64 tons distintos.
    """
    print("\n----- EXERCICIO 1: clusterizacao de tons de cinza -----")
    img = carregar_ou_gerar_imagem()

    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clusterizada = ((cinza // tamanho_grupo) * tamanho_grupo).astype(np.uint8)

    n_antes = len(np.unique(cinza))
    n_depois = len(np.unique(clusterizada))
    print(f"Tons distintos ANTES  : {n_antes}")
    print(f"Tons distintos DEPOIS : {n_depois}  (tamanho do grupo = {tamanho_grupo})")
    print(f"Maximo teorico de tons: {256 // tamanho_grupo}")

    cv2.imwrite(os.path.join(PASTA_SAIDA, "ex1_cinza.png"), cinza)
    cv2.imwrite(os.path.join(PASTA_SAIDA, "ex1_clusterizada.png"), clusterizada)

    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].imshow(bgr_para_rgb(img));                       ax[0].set_title("Original (colorida)")
    ax[1].imshow(cinza, cmap="gray", vmin=0, vmax=255);    ax[1].set_title(f"Tons de cinza ({n_antes} tons)")
    ax[2].imshow(clusterizada, cmap="gray", vmin=0, vmax=255)
    ax[2].set_title(f"Clusterizada a cada {tamanho_grupo} ({n_depois} tons)")
    for a in ax:
        a.axis("off")
    fig.suptitle("Exercicio 1 - Clusterizacao de tons de cinza", fontsize=14)
    plt.tight_layout()
    exibir_ou_salvar(fig, "ex1_painel.png")


# =============================================================================
# EXERCICIO 2 - SUBTRACAO DE IMAGENS + DETECCAO DO CORPO
# =============================================================================
_demo_par = {}


def _gerar_par_sintetico(altura=480, largura=640):
    """Gera um par (parede, pessoa) sintetico, consistente, caso o usuario
    ainda nao tenha tirado as fotos reais."""
    parede = np.full((altura, largura, 3), (200, 200, 195), dtype=np.uint8)
    parede = np.clip(parede.astype(np.int16) +
                     np.random.normal(0, 4, parede.shape).astype(np.int16),
                     0, 255).astype(np.uint8)
    pessoa = parede.copy()
    cor = (90, 70, 60)  # cor do "corpo", bem diferente da parede clara
    cv2.circle(pessoa, (320, 130), 45, cor, -1)            # cabeca
    cv2.rectangle(pessoa, (285, 175), (355, 360), cor, -1)  # tronco
    cv2.rectangle(pessoa, (150, 185), (285, 215), cor, -1)  # braco esquerdo
    cv2.rectangle(pessoa, (355, 185), (500, 215), cor, -1)  # braco direito
    cv2.rectangle(pessoa, (290, 360), (315, 460), cor, -1)  # perna esquerda
    cv2.rectangle(pessoa, (325, 360), (350, 460), cor, -1)  # perna direita
    _demo_par["fundo"] = parede
    _demo_par["pessoa"] = pessoa


def _carregar_par(caminho, papel):
    if os.path.exists(caminho):
        img = cv2.imread(caminho, cv2.IMREAD_COLOR)
        if img is not None:
            print(f"[info] Usando '{caminho}' como imagem de {papel}.")
            return img
    if "fundo" not in _demo_par:
        _gerar_par_sintetico()
    print(f"[info] '{caminho}' nao encontrado -> usando {papel} sintetico.")
    return _demo_par[papel].copy()


def exercicio2_subtracao(caminho_fundo="fundo.jpg",
                         caminho_pessoa="pessoa.jpg",
                         limiar_inicial=48,
                         sujeito_mais_escuro=True):
    """Subtrai as duas imagens, binariza por limiar empirico e desenha um
    retangulo VERMELHO sobre o corpo detectado.

    Coloque suas fotos como 'fundo.jpg' (so a parede) e 'pessoa.jpg' (voce de
    bracos abertos). No modo interativo, ajuste o limiar pelo slider.

    Subtracao COM SINAL: como normalmente o corpo (roupa) e MAIS ESCURO que a
    parede, usamos (fundo - pessoa). Isso realca o que ESCURECEU (voce) e
    descarta o que CLAREOU na cena (diferenca de iluminacao entre as fotos, ou
    uma sombra que sumiu do fundo) - bem mais robusto que o modulo |a - b|.
    Se voce estiver de roupa CLARA sobre fundo escuro, chame com
    sujeito_mais_escuro=False (passa a calcular pessoa - fundo)."""
    print("\n----- EXERCICIO 2: subtracao de imagens e deteccao do corpo -----")
    fundo = _carregar_par(caminho_fundo, "fundo")
    pessoa = _carregar_par(caminho_pessoa, "pessoa")

    # As duas imagens precisam ter o mesmo tamanho.
    if fundo.shape != pessoa.shape:
        pessoa = cv2.resize(pessoa, (fundo.shape[1], fundo.shape[0]))

    # Tons de cinza + leve suavizacao (reduz ruido e pequenos desalinhamentos).
    fundo_cinza = cv2.GaussianBlur(cv2.cvtColor(fundo, cv2.COLOR_BGR2GRAY), (5, 5), 0)
    pessoa_cinza = cv2.GaussianBlur(cv2.cvtColor(pessoa, cv2.COLOR_BGR2GRAY), (5, 5), 0)

    # Subtracao com sinal (recortada em [0, 255]) na direcao escolhida.
    f16 = fundo_cinza.astype(np.int16)
    p16 = pessoa_cinza.astype(np.int16)
    if sujeito_mais_escuro:
        diff = np.clip(f16 - p16, 0, 255).astype(np.uint8)   # fundo - pessoa
        rotulo_diff = "Diferenca (fundo - pessoa)"
    else:
        diff = np.clip(p16 - f16, 0, 255).astype(np.uint8)   # pessoa - fundo
        rotulo_diff = "Diferenca (pessoa - fundo)"

    def processar(limiar):
        """Binariza, limpa ruido (morfologia) e devolve
        (binaria, imagem_com_retangulo). Usa o MAIOR componente conectado como
        sendo o corpo, ignorando pequenos ruidos residuais."""
        _, binaria = cv2.threshold(diff, limiar, 255, cv2.THRESH_BINARY)
        # Abertura: remove pontos isolados / ruido fino.
        binaria = cv2.morphologyEx(binaria, cv2.MORPH_OPEN,
                                   np.ones((5, 5), np.uint8), iterations=1)
        # Fechamento vertical: religa a cabeca ao tronco (o rosto costuma ter
        # pouca diferenca e "corta" a silhueta).
        binaria = cv2.morphologyEx(binaria, cv2.MORPH_CLOSE,
                                   cv2.getStructuringElement(cv2.MORPH_RECT, (5, 35)),
                                   iterations=2)
        # Fechamento geral: preenche buracos internos do corpo.
        binaria = cv2.morphologyEx(binaria, cv2.MORPH_CLOSE,
                                   np.ones((15, 15), np.uint8), iterations=2)

        resultado = pessoa.copy()
        contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        if contornos:
            maior = max(contornos, key=cv2.contourArea)   # o corpo
            x, y, w, h = cv2.boundingRect(maior)
            # Retangulo vermelho (BGR = 0, 0, 255).
            cv2.rectangle(resultado, (x, y), (x + w, y + h), (0, 0, 255), 5)
        return binaria, resultado

    estado = {"limiar": limiar_inicial}
    binaria, resultado = processar(estado["limiar"])

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    if MODO_INTERATIVO:
        plt.subplots_adjust(bottom=0.14)
    axes[0, 0].imshow(bgr_para_rgb(pessoa));   axes[0, 0].set_title("Imagem com a pessoa")
    axes[0, 1].imshow(diff, cmap="gray");      axes[0, 1].set_title(rotulo_diff)
    im_bin = axes[1, 0].imshow(binaria, cmap="gray", vmin=0, vmax=255)
    axes[1, 0].set_title(f"Binarizada (limiar = {estado['limiar']})")
    im_res = axes[1, 1].imshow(bgr_para_rgb(resultado))
    axes[1, 1].set_title("Deteccao (retangulo vermelho)")
    for a in axes.ravel():
        a.axis("off")
    fig.suptitle("Exercicio 2 - Subtracao de imagens e deteccao do corpo",
                 fontsize=14)

    if MODO_INTERATIVO:
        ax_slider = plt.axes([0.25, 0.04, 0.5, 0.03])
        slider = Slider(ax_slider, "Limiar", 0, 255,
                        valinit=limiar_inicial, valstep=1)

        def atualizar(_):
            estado["limiar"] = int(slider.val)
            b, r = processar(estado["limiar"])
            im_bin.set_data(b)
            axes[1, 0].set_title(f"Binarizada (limiar = {estado['limiar']})")
            im_res.set_data(bgr_para_rgb(r))
            fig.canvas.draw_idle()

        slider.on_changed(atualizar)
        plt.show()
        # Apos fechar a janela, salva com o ultimo limiar escolhido.
        binaria, resultado = processar(estado["limiar"])
    else:
        exibir_ou_salvar(fig, "ex2_painel.png")

    print(f"Limiar final utilizado: {estado['limiar']}")
    cv2.imwrite(os.path.join(PASTA_SAIDA, "ex2_diferenca.png"), diff)
    cv2.imwrite(os.path.join(PASTA_SAIDA, "ex2_binarizada.png"), binaria)
    cv2.imwrite(os.path.join(PASTA_SAIDA, "ex2_resultado.png"), resultado)


# =============================================================================
# EXERCICIO 3 - FILTRO HIGH-BOOST (PROPRIO) x FILTRO PASSA-ALTA
# =============================================================================
def meu_filtro_high_boost(imagem_cinza, A=1.5, tam_kernel=5, sigma=0):
    """IMPLEMENTACAO PROPRIA do filtro high-boost.

    Ideia (mascaramento de nitidez generalizado):
        passa_baixa = suavizacao(imagem)            (borra a imagem)
        mascara     = imagem - passa_baixa          (componente de ALTA freq.)
        high_boost  = imagem + A * mascara

    Interpretacao do fator A:
        A = 1  -> mascaramento de nitidez (unsharp masking) classico
        A > 1  -> high-boost: realca bordas mantendo a imagem original visivel

    Trabalha em float para nao saturar; ao final faz clip em [0, 255].
    Retorna (resultado_high_boost, mascara_detalhes).
    """
    f = imagem_cinza.astype(np.float64)
    passa_baixa = cv2.GaussianBlur(f, (tam_kernel, tam_kernel), sigma)
    mascara = f - passa_baixa                 # detalhes / altas frequencias
    high_boost = f + A * mascara              # soma os detalhes realcados

    resultado = np.clip(high_boost, 0, 255).astype(np.uint8)
    mascara_vis = np.clip(np.abs(mascara), 0, 255).astype(np.uint8)
    return resultado, mascara_vis


def filtro_passa_alta(imagem_cinza):
    """Filtro PASSA-ALTA classico via kernel laplaciano 3x3 (soma = 0).
    Regioes homogeneas -> ~0 (preto); bordas -> realcadas."""
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]], dtype=np.float64)
    resultado = cv2.filter2D(imagem_cinza.astype(np.float64), -1, kernel)
    return np.clip(resultado, 0, 255).astype(np.uint8)


def exercicio3_high_boost(A_inicial=1.5):
    print("\n----- EXERCICIO 3: high-boost (proprio) x passa-alta -----")
    img = carregar_ou_gerar_imagem()
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    passa_alta = filtro_passa_alta(cinza)
    high_boost, mascara = meu_filtro_high_boost(cinza, A=A_inicial)

    cv2.imwrite(os.path.join(PASTA_SAIDA, "ex3_cinza.png"), cinza)
    cv2.imwrite(os.path.join(PASTA_SAIDA, "ex3_passa_alta.png"), passa_alta)
    cv2.imwrite(os.path.join(PASTA_SAIDA, "ex3_high_boost.png"), high_boost)

    print("Analise (resumo):")
    print(" - PASSA-ALTA: descarta as baixas frequencias; sobra basicamente as")
    print("   BORDAS. A imagem fica escura com contornos realcados (perde o")
    print("   conteudo/iluminacao geral da cena).")
    print(" - HIGH-BOOST: parte da imagem ORIGINAL e SOMA os detalhes (A*mascara).")
    print("   A imagem continua reconhecivel, porem mais NITIDA. Quanto maior A,")
    print("   mais forte o realce de bordas (A=1 equivale ao unsharp masking).")

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    if MODO_INTERATIVO:
        plt.subplots_adjust(bottom=0.14)
    axes[0, 0].imshow(cinza, cmap="gray", vmin=0, vmax=255)
    axes[0, 0].set_title("Original (tons de cinza)")
    axes[0, 1].imshow(passa_alta, cmap="gray", vmin=0, vmax=255)
    axes[0, 1].set_title("Filtro PASSA-ALTA (laplaciano)")
    axes[1, 0].imshow(mascara, cmap="gray", vmin=0, vmax=255)
    axes[1, 0].set_title("Mascara de detalhes |original - suave|")
    im_hb = axes[1, 1].imshow(high_boost, cmap="gray", vmin=0, vmax=255)
    axes[1, 1].set_title(f"HIGH-BOOST (minha funcao, A = {A_inicial:.1f})")
    for a in axes.ravel():
        a.axis("off")
    fig.suptitle("Exercicio 3 - High-boost x Passa-alta", fontsize=14)

    if MODO_INTERATIVO:
        ax_slider = plt.axes([0.25, 0.04, 0.5, 0.03])
        slider = Slider(ax_slider, "Fator A", 1.0, 5.0,
                        valinit=A_inicial, valstep=0.1)

        def atualizar(_):
            A = float(slider.val)
            hb, _m = meu_filtro_high_boost(cinza, A=A)
            im_hb.set_data(hb)
            axes[1, 1].set_title(f"HIGH-BOOST (minha funcao, A = {A:.1f})")
            fig.canvas.draw_idle()

        slider.on_changed(atualizar)
        plt.show()
    else:
        exibir_ou_salvar(fig, "ex3_painel.png")


# =============================================================================
# EXERCICIO 4 - TEOREMA DA CONVOLUCAO (espacial x frequencia)
# =============================================================================
def convolucao_frequencia(imagem, kernel):
    """Convolucao via TEOREMA DA CONVOLUCAO (multiplicacao no dominio da freq.).

        conv(f, h) = IDFT( DFT(f) . DFT(h) )

    Faz convolucao LINEAR (com zero-padding ate H+kh-1 x W+kw-1) e recorta a
    regiao central equivalente ao modo 'same' do dominio espacial.
    """
    H, W = imagem.shape
    kh, kw = kernel.shape
    sh, sw = H + kh - 1, W + kw - 1

    F = np.fft.fft2(imagem, s=(sh, sw))
    Hk = np.fft.fft2(kernel, s=(sh, sw))
    conv_full = np.real(np.fft.ifft2(F * Hk))

    di, dj = (kh - 1) // 2, (kw - 1) // 2
    return conv_full[di:di + H, dj:dj + W]


def exercicio4_convolucao(tam_kernel=31):
    """Compara o tempo da convolucao no dominio ESPACIAL (operador de
    convolucao direto) com o tempo no dominio da FREQUENCIA (FFT)."""
    print("\n----- EXERCICIO 4: Teorema da Convolucao (tempos) -----")
    img = carregar_ou_gerar_imagem()
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float64)

    # Kernel de media (passa-baixa) normalizado, de tamanho tam_kernel x tam_kernel.
    kernel = np.ones((tam_kernel, tam_kernel), np.float64) / (tam_kernel ** 2)

    # ---- Dominio espacial: operador de convolucao direto ----
    t0 = time.perf_counter()
    espacial = signal.convolve2d(cinza, kernel, mode="same", boundary="fill")
    t_espacial = time.perf_counter() - t0

    # ---- Dominio da frequencia: Teorema da Convolucao (FFT) ----
    t0 = time.perf_counter()
    frequencia = convolucao_frequencia(cinza, kernel)
    t_frequencia = time.perf_counter() - t0

    erro = float(np.max(np.abs(espacial - frequencia)))
    print(f"Imagem: {cinza.shape[0]}x{cinza.shape[1]}  |  Kernel: {tam_kernel}x{tam_kernel}")
    print(f"Tempo DOMINIO ESPACIAL   (convolucao): {t_espacial*1000:9.2f} ms")
    print(f"Tempo DOMINIO FREQUENCIA (FFT)       : {t_frequencia*1000:9.2f} ms")
    print(f"Aceleracao (espacial / frequencia)   : {t_espacial/max(t_frequencia,1e-9):9.2f}x")
    print(f"Diferenca maxima entre resultados    : {erro:.6e}  (deve ser ~0)")

    cv2.imwrite(os.path.join(PASTA_SAIDA, "ex4_espacial.png"),
                np.clip(espacial, 0, 255).astype(np.uint8))
    cv2.imwrite(os.path.join(PASTA_SAIDA, "ex4_frequencia.png"),
                np.clip(frequencia, 0, 255).astype(np.uint8))

    # ---- Varredura: como o tempo cresce com o tamanho do kernel ----
    tamanhos = [3, 7, 15, 25, 35, 45]
    t_esp, t_freq = [], []
    print("\nVarredura de tamanhos de kernel:")
    print(f"{'kernel':>8} | {'espacial (ms)':>14} | {'frequencia (ms)':>16}")
    for k in tamanhos:
        ker = np.ones((k, k), np.float64) / (k ** 2)
        t0 = time.perf_counter(); signal.convolve2d(cinza, ker, mode="same", boundary="fill"); te = time.perf_counter() - t0
        t0 = time.perf_counter(); convolucao_frequencia(cinza, ker);                              tf = time.perf_counter() - t0
        t_esp.append(te * 1000); t_freq.append(tf * 1000)
        print(f"{k:>6}x{k:<1} | {te*1000:>14.2f} | {tf*1000:>16.2f}")

    print("\nAnalise: no dominio espacial o custo cresce com o tamanho do kernel")
    print("(O(N*M*k^2)); ja no dominio da frequencia o custo e praticamente")
    print("constante (O(N*M*log(N*M))), pois nao depende de k. Por isso, a partir")
    print("de kernels grandes a abordagem por FFT (Teorema da Convolucao) e bem")
    print("mais rapida. Para kernels muito pequenos, a convolucao direta pode")
    print("vencer por causa do custo fixo da FFT (padding + transformadas).")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].imshow(np.clip(espacial, 0, 255).astype(np.uint8), cmap="gray")
    axes[0].set_title(f"Resultado (kernel {tam_kernel}x{tam_kernel})")
    axes[0].axis("off")
    axes[1].plot(tamanhos, t_esp, "o-", label="Dominio espacial (convolucao)")
    axes[1].plot(tamanhos, t_freq, "s-", label="Dominio frequencia (FFT)")
    axes[1].set_xlabel("Tamanho do kernel (lado)")
    axes[1].set_ylabel("Tempo (ms)")
    axes[1].set_title("Tempo x tamanho do kernel")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    fig.suptitle("Exercicio 4 - Teorema da Convolucao", fontsize=14)
    plt.tight_layout()
    exibir_ou_salvar(fig, "ex4_painel.png")


# =============================================================================
# MENU PRINCIPAL
# =============================================================================
def menu():
    opcoes = {
        "1": exercicio1_clusterizacao,
        "2": exercicio2_subtracao,
        "3": exercicio3_high_boost,
        "4": exercicio4_convolucao,
    }
    while True:
        print("\n========= PROCESSAMENTO DE IMAGENS =========")
        print(" 1) Tons de cinza com clusterizacao (a cada 4)")
        print(" 2) Subtracao de imagens + deteccao do corpo")
        print(" 3) Filtro high-boost (proprio) x passa-alta")
        print(" 4) Teorema da Convolucao (espacial x frequencia)")
        print(" 0) Sair")
        op = input("Escolha uma opcao: ").strip()
        if op == "0":
            print("Encerrando.")
            break
        elif op in opcoes:
            opcoes[op]()
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    # Permite rodar um exercicio direto: python processamento_imagens.py 3
    if len(sys.argv) > 1 and sys.argv[1] in {"1", "2", "3", "4"}:
        {"1": exercicio1_clusterizacao, "2": exercicio2_subtracao,
         "3": exercicio3_high_boost, "4": exercicio4_convolucao}[sys.argv[1]]()
    else:
        menu()
