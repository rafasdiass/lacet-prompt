import unittest
from app_balance.processamento.file_processing_service import FileProcessingService
from app_balance.processamento.models import Recebimento
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app_balance.processamento.database_setup import Base
import os
import shutil

class TestFileProcessingService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)

    def setUp(self):
        self.session = self.Session()
        self.file_processing_service = FileProcessingService(session=self.session, usuario=self.mock_usuario)

        # Criar diretório temporário
        self.example_dir = os.path.join(os.path.dirname(__file__), 'temp_exemplo')
        os.makedirs(self.example_dir, exist_ok=True)

        # Criar arquivo exemplo.xlsx
        self.excel_path = os.path.join(self.example_dir, 'exemplo.xlsx')
        with open(self.excel_path, 'wb') as f:
            f.write(self._criar_arquivo_excel_exemplo())

    def _criar_arquivo_excel_exemplo(self):
        import pandas as pd
        from io import BytesIO
        df = pd.DataFrame({
            'Categoria': ['Marketing', 'RH', 'TI'],
            'Valor': [5000, 3000, 2000]
        })
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return buffer.getvalue()

    def test_processar_arquivo_excel_e_inserir_no_banco(self):
        with open(self.excel_path, 'rb') as f:
            excel_bytes = f.read()
        result = self.file_processing_service.processar_arquivo_excel(excel_bytes)
        recebimentos = self.session.query(Recebimento).all()
        self.assertGreater(len(recebimentos), 0)

    def tearDown(self):
        self.session.close()
        shutil.rmtree(self.example_dir)

if __name__ == '__main__':
    unittest.main()
