from concurrent import futures
import grpc
import autenticacao_pb2
import autenticacao_pb2_grpc
import hashlib
import uuid
from google.protobuf import empty_pb2
from datetime import datetime

# Implementação do serviço de autenticação RPC
class AutenticacaoRPC(autenticacao_pb2_grpc.AutenticacaoUsuarioServicer):
    def __init__(self):
        self.usuarios = {}

    def RegistrarUsuario(self, request, context):
        user_id = str(uuid.uuid4())
        hashed_password = hashlib.sha256(request.senha.encode()).hexdigest()
        self.usuarios[request.email] = {'id': user_id, 'nome': request.nome, 'senha': hashed_password}
        return autenticacao_pb2.RegistrarUsuarioResponse(id=user_id)

    def LoginUsuario(self, request, context):
        user = self.usuarios.get(request.email)
        if user and user['senha'] == hashlib.sha256(request.senha.encode()).hexdigest():
            token = str(uuid.uuid4())  # Simple token generation for demonstration
            return autenticacao_pb2.LoginUsuarioResponse(token=token)
        context.set_code(grpc.StatusCode.UNAUTHENTICATED)
        context.set_details('Credenciais inválidas')
        return autenticacao_pb2.LoginUsuarioResponse()