# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: catalogo.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x63\x61talogo.proto\x12\x08\x63\x61talogo\x1a\x1bgoogle/protobuf/empty.proto\"\'\n\x15\x43onsultarLivroRequest\x12\x0e\n\x06titulo\x18\x01 \x01(\t\"w\n\x16\x43onsultarLivroResponse\x12\x0e\n\x06titulo\x18\x01 \x01(\t\x12\r\n\x05\x61utor\x18\x02 \x01(\t\x12\x0b\n\x03\x61no\x18\x03 \x01(\x05\x12\x0f\n\x07\x65stoque\x18\x04 \x01(\x05\x12\r\n\x05preco\x18\x05 \x01(\x02\x12\x11\n\tdescricao\x18\x06 \x01(\t\"f\n\x05Livro\x12\x0e\n\x06titulo\x18\x01 \x01(\t\x12\r\n\x05\x61utor\x18\x02 \x01(\t\x12\x0b\n\x03\x61no\x18\x03 \x01(\x05\x12\x0f\n\x07\x65stoque\x18\x04 \x01(\x05\x12\r\n\x05preco\x18\x05 \x01(\x02\x12\x11\n\tdescricao\x18\x06 \x01(\t\"\x15\n\x13ListarLivrosRequest\"7\n\x14ListarLivrosResponse\x12\x1f\n\x06livros\x18\x01 \x03(\x0b\x32\x0f.catalogo.Livro\"7\n\x15\x41tualizarLivroRequest\x12\x1e\n\x05livro\x18\x01 \x01(\x0b\x32\x0f.catalogo.Livro2\xd8\x02\n\x0e\x43\x61talogoLivros\x12S\n\x0e\x43onsultarLivro\x12\x1f.catalogo.ConsultarLivroRequest\x1a .catalogo.ConsultarLivroResponse\x12M\n\x0cListarLivros\x12\x1d.catalogo.ListarLivrosRequest\x1a\x1e.catalogo.ListarLivrosResponse\x12W\n\x12ObterDetalhesLivro\x12\x1f.catalogo.ConsultarLivroRequest\x1a .catalogo.ConsultarLivroResponse\x12I\n\x0e\x41tualizarLivro\x12\x1f.catalogo.AtualizarLivroRequest\x1a\x16.google.protobuf.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'catalogo_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CONSULTARLIVROREQUEST']._serialized_start=57
  _globals['_CONSULTARLIVROREQUEST']._serialized_end=96
  _globals['_CONSULTARLIVRORESPONSE']._serialized_start=98
  _globals['_CONSULTARLIVRORESPONSE']._serialized_end=217
  _globals['_LIVRO']._serialized_start=219
  _globals['_LIVRO']._serialized_end=321
  _globals['_LISTARLIVROSREQUEST']._serialized_start=323
  _globals['_LISTARLIVROSREQUEST']._serialized_end=344
  _globals['_LISTARLIVROSRESPONSE']._serialized_start=346
  _globals['_LISTARLIVROSRESPONSE']._serialized_end=401
  _globals['_ATUALIZARLIVROREQUEST']._serialized_start=403
  _globals['_ATUALIZARLIVROREQUEST']._serialized_end=458
  _globals['_CATALOGOLIVROS']._serialized_start=461
  _globals['_CATALOGOLIVROS']._serialized_end=805
# @@protoc_insertion_point(module_scope)
