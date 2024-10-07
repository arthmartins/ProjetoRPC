import grpc
import pedidos_pb2
import pedidos_pb2_grpc
from datetime import datetime

class PedidosRPC(pedidos_pb2_grpc.GestaoPedidosServicer):
    def __init__(self):
        self.pedidos = {} 

    def RealizarPedido(self, request, context):
        pedido_id = str(len(self.pedidos) + 1)
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.pedidos[pedido_id] = {
            "usuario_id": request.usuario_id, 
            "data": data,
            "livros": [{"titulo": livro.titulo, "quantidade": livro.quantidade} for livro in request.livros]
        }
        return pedidos_pb2.RealizarPedidoResponse(id=pedido_id)

    
    def ObterDetalhesPedido(self, request, context):
        pedido = self.pedidos.get(request.id)
        usuario_id = request.usuario_id
        if pedido and pedido['usuario_id'] == usuario_id:
            return pedidos_pb2.ObterDetalhesPedidoResponse(
                id=request.id,
                data=pedido['data'],
                livros=[pedidos_pb2.Livro(titulo=livro['titulo'], quantidade=livro['quantidade']) for livro in pedido['livros']]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Pedido não encontrado')
            return pedidos_pb2.ObterDetalhesPedidoResponse()
    
    def RecuperarHistoricoPedidos(self, request, context):
        return pedidos_pb2.HistoricoPedidosResponse(
            pedidos=[
                pedidos_pb2.Pedido(
                    id=pedido_id,
                    data=pedido['data'],
                    livros=[
                        pedidos_pb2.Livro(titulo=livro['titulo'], quantidade=livro['quantidade'])
                        for livro in pedido['livros']
                    ]
                )
                for pedido_id, pedido in self.pedidos.items() if pedido['usuario_id'] == request.usuario_id
            ]
        )