import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server/autenticacao')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server/catalogo')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server/pedidos')))

from flask import Flask, render_template, request, redirect, url_for, flash, session
import grpc
import catalogo_pb2
import catalogo_pb2_grpc
import pedidos_pb2
import pedidos_pb2_grpc
import autenticacao_pb2
import autenticacao_pb2_grpc



def get_autenticacao_proxy():
    channel = grpc.insecure_channel('localhost:1914')
    return autenticacao_pb2_grpc.AutenticacaoUsuarioStub(channel)

def get_catalogo_proxy():
    channel = grpc.insecure_channel('localhost:1914')
    return catalogo_pb2_grpc.CatalogoLivrosStub(channel)

def get_pedidos_proxy():
    channel = grpc.insecure_channel('localhost:1914')
    return pedidos_pb2_grpc.GestaoPedidosStub(channel)


app = Flask(__name__)
app.secret_key = 'palmeirasMaiordoBrasil'

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        autentic_proxy = get_autenticacao_proxy()
        try:
            response = autentic_proxy.LoginUsuario(autenticacao_pb2.LoginUsuarioRequest(email=email, senha=senha))
            session['token'] = response.token
            session['usuario_id'] = email
            return redirect(url_for('menu'))
        except grpc.RpcError as e:
            flash(f"Erro de autenticação: {e.details()}", 'error')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        autentic_proxy = get_autenticacao_proxy()
        try:
            autentic_proxy.RegistrarUsuario(autenticacao_pb2.RegistrarUsuarioRequest(nome=nome, email=email, senha=senha))
            flash("Usuário registrado com sucesso!", 'success')
            return redirect(url_for('login'))
        except grpc.RpcError as e:
            flash(f"Erro de registro: {e.details()}", 'error')
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('token', None)
    flash("Você foi deslogado.", 'success')
    return redirect(url_for('login'))


@app.route('/catalogo')
def catalogo():
    catalog_proxy = get_catalogo_proxy()
    try:
        response = catalog_proxy.ListarLivros(catalogo_pb2.ListarLivrosRequest())
        livros = [{'titulo': livro.titulo, 'autor': livro.autor, 'ano': livro.ano, 'estoque': livro.estoque, 'preco': livro.preco} for livro in response.livros]
    
        return render_template('catalogo.html', livros=livros)
    except grpc.RpcError as e:
        flash(f"Erro ao listar livros: {e.details()}", 'error')
        return redirect(url_for('index'))


@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html', carrinho=session.get('carrinho', []))


@app.route('/add_carrinho', methods=['POST'])
def add_carrinho():
    
    titulo = request.form['titulo']
    quantidade = int(request.form['quantidade'])
    
    catalog_proxy = get_catalogo_proxy()

    livro_response = catalog_proxy.ConsultarLivro(catalogo_pb2.ConsultarLivroRequest(titulo=titulo))
    
    if not livro_response.titulo:
        flash("Livro não encontrado!", 'danger')
        return redirect(url_for('catalogo'))

    if livro_response.estoque < quantidade:
        flash("Quantidade disponível insuficiente!", 'danger')
        return redirect(url_for('catalogo'))

    carrinho = session.get('carrinho', [])

    for item in carrinho:
        if item['titulo'] == titulo:
            item['quantidade'] += quantidade
            break
    else:
        carrinho.append({'titulo': titulo, 'quantidade': quantidade})

    session['carrinho'] = carrinho

    novo_estoque = livro_response.estoque - quantidade
    
    try:
        catalog_proxy.AtualizarLivro(catalogo_pb2.AtualizarLivroRequest(
            livro=catalogo_pb2.Livro(
                titulo=livro_response.titulo,
                autor=livro_response.autor,
                ano=livro_response.ano,
                estoque=novo_estoque,
                preco=livro_response.preco,
                descricao=livro_response.descricao
            )
        ))
        flash("Livro adicionado ao carrinho!", 'success')
    except grpc.RpcError as e:
        flash(f"Erro ao atualizar livro: {e.details()}", 'danger')

    return redirect(url_for('catalogo'))


@app.route('/checkout', methods=['POST'])
def checkout():
    carrinho = session.get('carrinho', [])
    pedido_proxy = get_pedidos_proxy()
    livros = [pedidos_pb2.Livro(titulo=item['titulo'], quantidade=item['quantidade']) for item in carrinho]
    try:
        response = pedido_proxy.RealizarPedido(pedidos_pb2.RealizarPedidoRequest(usuario_id=session['usuario_id'], livros=livros))
        session.pop('carrinho', None)
        return redirect(url_for('relatorio_pedido', pedido_id=response.id))
    except grpc.RpcError as e:
        flash(f"Erro ao realizar pedido: {e.details()}", 'error')
        return redirect(url_for('carrinho'))
    
    
@app.route('/relatorio_pedido/<pedido_id>')
def relatorio_pedido(pedido_id):
    pedido_proxy = get_pedidos_proxy()
    try:
        response = pedido_proxy.ObterDetalhesPedido(pedidos_pb2.ObterDetalhesPedidoRequest(id=pedido_id,usuario_id=session['usuario_id']))
        return render_template('relatorio_pedido.html', pedido=response)
    except grpc.RpcError as e:
        flash("Pedido não encontrado", 'warning')
        return redirect(url_for('pesquisar_pedido'))


@app.route('/historico')
def historico():
    pedido_proxy = get_pedidos_proxy()
    try:
        response = pedido_proxy.RecuperarHistoricoPedidos(pedidos_pb2.HistoricoPedidosRequest(usuario_id=session['usuario_id']))
        pedidos = [{'id': pedido.id, 'data': pedido.data, 'livros': [{'titulo': livro.titulo, 'quantidade': livro.quantidade} for livro in pedido.livros]} for pedido in response.pedidos]
        return render_template('historico.html', pedidos=pedidos)
    except grpc.RpcError as e:
        flash(f"Erro ao recuperar histórico de pedidos: {e.details()}", 'error')
        return redirect(url_for('index'))
    
    
@app.route('/pesquisar_livro', methods=['GET', 'POST'])
def pesquisar_livro():
    resultado = None
    livro_nao_encontrado = False
    if request.method == 'POST':
        titulo = request.form['titulo']
        catalog_proxy = get_catalogo_proxy()
        try:
            response = catalog_proxy.ConsultarLivro(catalogo_pb2.ConsultarLivroRequest(titulo=titulo))
            resultado = {
                'titulo': response.titulo,
                'autor': response.autor,
                'ano': response.ano,
                'estoque': response.estoque,
                'preco': response.preco,
                'descricao': response.descricao
            }
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                livro_nao_encontrado = True
            else:
                flash(f"Erro ao pesquisar livro: {e.details()}", 'error')

    return render_template('pesquisar_livro.html', resultado=resultado, livro_nao_encontrado=livro_nao_encontrado)


@app.route('/pesquisar_pedido', methods=['GET', 'POST'])
def pesquisar_pedido():
    pedido_id = None
    if request.method == 'POST':
        pedido_id = request.form['pedido_id']
        return redirect(url_for('relatorio_pedido', pedido_id=pedido_id))

    return render_template('pesquisar_pedido.html')


@app.route('/detalhes_livro/<titulo>')
def detalhes_livro(titulo):
    catalog_proxy = get_catalogo_proxy()
    livro_detalhes = catalog_proxy.ConsultarLivro(catalogo_pb2.ConsultarLivroRequest(titulo=titulo))
    return render_template('detalhes_livro.html', livro=livro_detalhes)


@app.route('/remover_item/<titulo>', methods=['POST'])
def remover_item(titulo):
    carrinho = session.get('carrinho', [])
    
    for item in carrinho:
        if item['titulo'] == titulo:
            item['quantidade'] -= 1
            
            catalog_proxy = get_catalogo_proxy()
            livro_response = catalog_proxy.ConsultarLivro(catalogo_pb2.ConsultarLivroRequest(titulo=titulo))
            novo_estoque = livro_response.estoque + 1
            
            catalog_proxy.AtualizarLivro(catalogo_pb2.AtualizarLivroRequest(
                livro=catalogo_pb2.Livro(
                    titulo=livro_response.titulo,
                    autor=livro_response.autor,
                    ano=livro_response.ano,
                    estoque=novo_estoque,
                    preco=livro_response.preco,
                    descricao=livro_response.descricao
                )
            ))
            
            if item['quantidade'] <= 0:
                carrinho.remove(item)
            break

    session['carrinho'] = carrinho
    flash("Uma unidade do livro foi removida do carrinho.", 'success')
    
    return redirect(url_for('carrinho'))

if __name__ == '__main__':
    app.run(host='localhost', port=3000)
