from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


tabuleiro = {i: ' ' for i in range(1, 10)}
mensagem = ''
jogo_acabou = False


def verificar_vencedor(tab, letra):
    """Verifica se o jogador com a letra dada ganhou"""
    combinacoes = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],  # linhas
        [1, 4, 7], [2, 5, 8], [3, 6, 9],  # colunas
        [1, 5, 9], [3, 5, 7],              # diagonais
    ]
    for a, b, c in combinacoes:
        if tab[a] == tab[b] == tab[c] == letra:
            return True
    return False


def tabuleiro_cheio(tab):
    """Verifica se não há mais posições disponíveis"""
    for posicao in tab:
        if tab[posicao] == ' ':
            return False
    return True


def jogada_ia(tab):
    """IA em lógica pura - tenta vencer, bloquear ou jogar estratégico"""

    combinacoes = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],
        [1, 4, 7], [2, 5, 8], [3, 6, 9],
        [1, 5, 9], [3, 5, 7],
    ]

    
    for a, b, c in combinacoes:
        valores = [tab[a], tab[b], tab[c]]
        if valores.count('O') == 2 and valores.count(' ') == 1:
            for pos in [a, b, c]:
                if tab[pos] == ' ':
                    return pos

    
    for a, b, c in combinacoes:
        valores = [tab[a], tab[b], tab[c]]
        if valores.count('X') == 2 and valores.count(' ') == 1:
            for pos in [a, b, c]:
                if tab[pos] == ' ':
                    return pos

    
    if tab[5] == ' ':
        return 5

   
    for canto in [1, 3, 7, 9]:
        if tab[canto] == ' ':
            return canto

    
    for pos in tab:
        if tab[pos] == ' ':
            return pos


@app.route('/')
def index():
    return render_template('index3ia.html',
                           tabuleiro=tabuleiro,
                           mensagem=mensagem,
                           jogo_acabou=jogo_acabou)


@app.route('/jogar', methods=['POST'])
def jogar():
    global tabuleiro, mensagem, jogo_acabou

    if jogo_acabou:
        return redirect(url_for('index'))

    posicao = int(request.form['posicao'])

    if tabuleiro[posicao] != ' ':
        mensagem = '⚠️ Posição ocupada! Escolha outra.'
        return redirect(url_for('index'))

    
    tabuleiro[posicao] = 'X'

    if verificar_vencedor(tabuleiro, 'X'):
        mensagem = '🏆 Você GANHOU! Parabéns!'
        jogo_acabou = True
        return redirect(url_for('index'))

    if tabuleiro_cheio(tabuleiro):
        mensagem = '🤝 EMPATE!'
        jogo_acabou = True
        return redirect(url_for('index'))

    
    pos_ia = jogada_ia(tabuleiro)
    tabuleiro[pos_ia] = 'O'

    if verificar_vencedor(tabuleiro, 'O'):
        mensagem = '🤖 A IA GANHOU! Tente de novo.'
        jogo_acabou = True
        return redirect(url_for('index'))

    if tabuleiro_cheio(tabuleiro):
        mensagem = '🤝 EMPATE!'
        jogo_acabou = True
        return redirect(url_for('index'))

    mensagem = '🤖 A IA jogou! Sua vez.'
    return redirect(url_for('index'))


@app.route('/reiniciar', methods=['POST'])
def reiniciar():
    global tabuleiro, mensagem, jogo_acabou

    tabuleiro = {i: ' ' for i in range(1, 10)}
    mensagem = '🔄 Novo jogo! Você começa (X).'
    jogo_acabou = False

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')