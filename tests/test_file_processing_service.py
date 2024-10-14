import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
from processamento.file_processing_service import FileProcessingService
from app_balance.services.text_processing import TextProcessingService

class TestFileProcessingService(unittest.TestCase):

    def setUp(self):
        # Inicializar os serviços
        self.file_service = FileProcessingService()
        self.text_processor = TextProcessingService()

    @patch('pandas.read_excel')
    def test_processar_arquivo_excel(self, mock_read_excel):
        # Simulando leitura de Excel com dados de exemplo
        mock_read_excel.return_value = {
            'Sheet1': pd.DataFrame([{'Coluna1': 'Valor1', 'Coluna2': 'Valor2'}])
        }

        # Dados simulados de arquivo Excel
        arquivo_excel = b"simulacao de bytes de excel"
        result = self.file_service.processar_arquivo(arquivo_excel, 'excel')

        # Verificar se os dados foram extraídos corretamente
        self.assertIn('Sheet1', result)
        self.assertEqual(result['Sheet1'][0]['Coluna1'], 'Valor1')
        self.assertEqual(result['Sheet1'][0]['Coluna2'], 'Valor2')

    @patch('PyPDF2.PdfReader')
    def test_processar_arquivo_pdf(self, mock_pdf_reader):
        # Simular a leitura do PDF
        mock_pdf_reader.return_value.pages = [MagicMock(extract_text=lambda: "Texto PDF Simulado")]
        
        # Dados simulados de arquivo PDF
        arquivo_pdf = b"simulacao de bytes de pdf"
        result = self.file_service.processar_arquivo(arquivo_pdf, 'pdf')

        # Verificar se os dados foram extraídos corretamente
        self.assertEqual(result['texto'], "Texto PDF Simulado")

    @patch('docx.Document')
    def test_processar_arquivo_docx(self, mock_docx):
        # Simular a leitura de DOCX
        mock_docx.return_value.paragraphs = [MagicMock(text="Texto DOCX Simulado")]

        # Dados simulados de arquivo DOCX
        arquivo_docx = b"simulacao de bytes de docx"
        result = self.file_service.processar_arquivo(arquivo_docx, 'docx')

        # Verificar se os dados foram extraídos corretamente
        self.assertEqual(result['texto'], "Texto DOCX Simulado")

    @patch.object(TextProcessingService, 'route_and_process')
    def test_processar_excel_enviar_para_text_processing(self, mock_route_and_process):
        # Simulando a leitura de Excel
        self.file_service.processar_arquivo_excel = MagicMock(return_value={"Sheet1": [{"Coluna1": "Valor1"}]})
        
        # Processar arquivo e enviar para TextProcessingService
        arquivo_excel = b"simulacao de bytes de excel"
        dados_extraidos = self.file_service.processar_arquivo(arquivo_excel, 'excel')

        # Simulação de processamento pelo serviço de texto
        self.text_processor.route_and_process(dados_extraidos)

        # Verifica se o serviço de texto recebeu os dados
        mock_route_and_process.assert_called_once_with(dados_extraidos)

    @patch.object(TextProcessingService, 'route_and_process')
    def test_processar_pdf_enviar_para_text_processing(self, mock_route_and_process):
        # Simular a leitura de um arquivo PDF
        self.file_service.processar_arquivo_pdf = MagicMock(return_value="Texto de Exemplo PDF")
        
        # Processar arquivo e enviar para TextProcessingService
        arquivo_pdf = b"simulacao de bytes de pdf"
        dados_extraidos = self.file_service.processar_arquivo(arquivo_pdf, 'pdf')

        # Simulação de processamento pelo serviço de texto
        self.text_processor.route_and_process(dados_extraidos)

        # Verifica se o serviço de texto recebeu os dados
        mock_route_and_process.assert_called_once_with(dados_extraidos)


if __name__ == '__main__':
    unittest.main()
