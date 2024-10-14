import unittest
import os
from processamento.file_processing_service import FileProcessingService

class TestFileProcessingService(unittest.TestCase):

    def setUp(self):
        # Inicializando o serviço de processamento de arquivos
        self.file_service = FileProcessingService()

        # Definindo o caminho absoluto para os arquivos de teste
        base_path = os.path.abspath(os.path.dirname(__file__))  # Caminho absoluto do diretório de testes
        self.excel_file_path = os.path.join(base_path, '../app_balance/exemplo/exemplo.xlsx')
        self.pdf_file_path = os.path.join(base_path, '../app_balance/exemplo/exemplo.pdf')
        self.docx_file_path = os.path.join(base_path, '../app_balance/exemplo/exemplo.docx')

    def test_processar_arquivo_excel_real(self):
        """Testa o processamento de um arquivo Excel real."""
        with open(self.excel_file_path, 'rb') as f:
            arquivo_excel = f.read()

        result = self.file_service.processar_arquivo(arquivo_excel, 'excel')

        # Verifica se os dados foram extraídos corretamente
        self.assertIn('Sheet1', result)
        self.assertTrue(isinstance(result['Sheet1'], list))  # Verifique se retorna uma lista de registros

    def test_processar_arquivo_pdf_real(self):
        """Testa o processamento de um arquivo PDF real."""
        with open(self.pdf_file_path, 'rb') as f:
            arquivo_pdf = f.read()

        result = self.file_service.processar_arquivo(arquivo_pdf, 'pdf')

        # Verifica se o texto foi extraído corretamente
        self.assertTrue(isinstance(result['texto'], str))
        self.assertGreater(len(result['texto']), 0)  # Verifica se o texto extraído não está vazio

    def test_processar_arquivo_docx_real(self):
        """Testa o processamento de um arquivo DOCX real."""
        with open(self.docx_file_path, 'rb') as f:
            arquivo_docx = f.read()

        result = self.file_service.processar_arquivo(arquivo_docx, 'docx')

        # Verifica se o texto foi extraído corretamente
        self.assertTrue(isinstance(result['texto'], str))
        self.assertGreater(len(result['texto']), 0)  # Verifica se o texto extraído não está vazio


if __name__ == '__main__':
    unittest.main()
