import os
from concurrent import futures
import grpc
import catalogo_pb2
import catalogo_pb2_grpc
from google.protobuf import empty_pb2
from datetime import datetime

class CatalogoRPC(catalogo_pb2_grpc.CatalogoLivrosServicer):
    
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        livros_path = os.path.join(current_dir, 'livros.txt')
        self.livros = self.carregar_livros(livros_path)
        

    def carregar_livros(self, arquivo):
        livros = {}
        with open(arquivo, 'r') as f:
            for linha in f:
                titulo, autor, ano, estoque, preco, descricao = linha.strip().split(';')
                livros[titulo] = {
                    "titulo": titulo,
                    "autor": autor,
                    "ano": int(ano),
                    "estoque": int(estoque),
                    "preco": float(preco),
                    "descricao": descricao
                }
        return livros


    def AtualizarLivro(self, request, context):
        livro = request.livro
        if livro.titulo in self.livros:
            self.livros[livro.titulo]['estoque'] = livro.estoque
            return empty_pb2.Empty()
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Livro não encontrado para atualização')
            return empty_pb2.Empty()
    
    def encontrar_livro(self, titulo):
        titulo = titulo.lower()
        for livro in self.livros.values():
            if livro["titulo"].lower() == titulo:
                return livro
        return None
    
    def ConsultarLivro(self, request, context):
        livro = self.encontrar_livro(request.titulo)
        if livro:
            return catalogo_pb2.ConsultarLivroResponse(
                titulo=livro['titulo'],
                autor=livro['autor'],
                ano=livro['ano'],
                estoque=livro['estoque'],
                preco=livro['preco'],
                descricao=livro['descricao']
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Livro não encontrado')
            return catalogo_pb2.ConsultarLivroResponse()
        
        
    def ListarLivros(self, request, context):
        livros = [catalogo_pb2.Livro(titulo=livro['titulo'], autor=livro['autor'], ano=livro['ano'], estoque=livro['estoque'], preco=livro['preco'], descricao=livro['descricao']) for livro in self.livros.values()]
        return catalogo_pb2.ListarLivrosResponse(livros=livros)
    
    def ObterDetalhesLivro(self, request, context):
        for livro in self.livros:
            if livro.titulo == request.titulo:
                return catalogo_pb2.ObterDetalhesLivro(
                    titulo=livro.titulo,
                    autor=livro.autor,
                    ano=livro.ano,
                    preco=livro.preco,
                    estoque=livro.estoque,
                    descricao=livro.descricao  # Adicione este campo se disponível
                )
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Livro não encontrado')
        return catalogo_pb2.ObterDetalhesLivro()