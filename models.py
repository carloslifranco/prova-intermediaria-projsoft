from datetime import datetime
from bson import ObjectId

class Pagamento:
    def __init__(self, codigo, valor_pagamento, tipo_pagamento, parcelas, valor_parcela, usuario_email, usuario_id, _id=None, data_pagamento=None):
        self._id = _id
        self.usuario_id = usuario_id
        self.usuario_email = usuario_email
        self.codigo = codigo
        self.valor_pagamento = valor_pagamento
        self.tipo_pagamento = tipo_pagamento
        self.parcelas = parcelas
        self.valor_parcela = valor_parcela

        # Se não vier data (criação), o servidor gera o timestamp atual
        self.data_pagamento = data_pagamento if data_pagamento else datetime.utcnow()

    def to_dict(self):
        """Converte o objeto para um dicionário compatível com o MongoDB"""
        pagamento_dict = {
            "usuario_id": self.usuario_id,
            "usuario_email": self.usuario_email,
            "codigo": self.codigo,
            "valor_pagamento": self.valor_pagamento,
            "tipo_pagamento": self.tipo_pagamento,
            "parcelas": self.parcelas,
            "valor_parcela": self.valor_parcela,
            "data_pagamento": self.data_pagamento
        }
        if self._id:
            pagamento_dict["_id"] = ObjectId(self._id) if isinstance(self._id, str) else self._id
        return pagamento_dict

    @staticmethod
    def from_mongo(data):
        """Converte o documento do MongoDB de volta para a classe Post"""
        if not data:
            return None
        return Pagamento(
            _id=str(data.get('_id')),
            usuario_id=data.get('usuario_id'),
            usuario_email=data.get('usuario_email'),
            codigo=data.get('codigo'),
            valor_pagamento=data.get('valor_pagamento'),
            tipo_pagamento=data.get('tipo_pagamento'),
            parcelas=data.get('parcelas'),
            valor_parcela=data.get('valor_parcela'),
            data_pagamento=data.get('data_pagamento')
        )