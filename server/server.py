import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'autenticacao')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'catalogo')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'pedidos')))


from concurrent import futures
import grpc
import catalogo_pb2
import catalogo_pb2_grpc
import pedidos_pb2
import pedidos_pb2_grpc
import autenticacao_pb2
import autenticacao_pb2_grpc
import catalogoRPC
import pedidosRPC
import autenticacaoRPC

from google.protobuf import empty_pb2
from datetime import datetime



def serve():
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    catalogo_pb2_grpc.add_CatalogoLivrosServicer_to_server(catalogoRPC.CatalogoRPC(), server)
    pedidos_pb2_grpc.add_GestaoPedidosServicer_to_server(pedidosRPC.PedidosRPC(), server)
    autenticacao_pb2_grpc.add_AutenticacaoUsuarioServicer_to_server(autenticacaoRPC.AutenticacaoRPC(), server)
    server.add_insecure_port('[::]:1914')
    server.start()
    print("Servidor iniciado. Ouvindo em [::]:1914.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
