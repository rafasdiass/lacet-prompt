import unittest
from unittest.mock import patch
from app_balance.services.text_processing import TextProcessingService

# Verifique e baixe os pacotes NLTK se necessário
import nltk

def setup_nltk():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

# Chame a função setup_nltk no início
setup_nltk()


class TestTextProcessingService(unittest.TestCase):

    def setUp(self):
        self.text_processor = TextProcessingService()

    def test_greeting_route(self):
        prompt = "Olá"
        route = self.text_processor.route_and_process(prompt)
        self.assertEqual(route, "general")  # Não há rota específica para cumprimentos no exemplo dado

    @patch('app_balance.services.text_processing_service.classifier', return_value=[{'label': 'POSITIVE'}])
    def test_financial_route(self, mock_classifier):
        route = self.text_processor.route_and_process("Me fale sobre finanças")
        self.assertEqual(route, "financial")

    @patch('app_balance.services.text_processing_service.classifier', return_value=[{'label': 'POSITIVE'}])
    def test_advanced_financial_route(self, mock_classifier):
        route = self.text_processor.route_and_process("Faça uma análise financeira avançada de AAPL")
        self.assertEqual(route, "advanced_financial")

    @patch('app_balance.services.text_processing_service.classifier', return_value=[{'label': 'POSITIVE'}])
    def test_joke_route(self, mock_classifier):
        route = self.text_processor.route_and_process("Conte-me uma piada")
        self.assertEqual(route, "joke")

    def test_general_route(self):
        route = self.text_processor.route_and_process("Qual é a teoria da relatividade?")
        self.assertEqual(route, "general")


if __name__ == '__main__':
    unittest.main()
