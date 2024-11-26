import boto3
from datetime import datetime

TABLA_TERAPIAS = os.environ['TABLA_TERAPIAS']

class TerapiasHandler:
    def registrar_terapia(self, id_paciente, tipo_terapia, fecha):
        id_terapia = f"T{hash(id_paciente)}-{int(datetime.now().timestamp())}"
        self.dynamodb.put_item(
            TableName=TABLA_TERAPIAS,
            Item={
                'IDTerapia': {'S': id_terapia},
                'IDPaciente': {'S': id_paciente},
                'TipoTerapia': {'S': tipo_terapia},
                'Fecha': {'S': fecha},
                'Timestamp': {'S': datetime.now().isoformat()}
            }
        )
        return id_terapia
