import unittest
from app_balance.services.text_processing import TextProcessingService

class TestTextProcessingService(unittest.TestCase):

    def setUp(self):
        self.text_processor = TextProcessingService()

    def test_financial_route_from_file_data(self):
        # Teste para garantir que palavras relacionadas a finanças escolhem a rota 'financial'
        file_data = {
            'categorias_custos': {'finança': 100.0, 'investimento': 200.0}
        }
        route = self.text_processor.route_and_process(file_data)
        self.assertEqual(route, "financial", "Esperava a rota 'financial' mas obteve outra rota.")

    def test_joke_route_from_file_data(self):
        # Teste para garantir que palavras relacionadas a piadas escolhem a rota 'joke'
        file_data = {
            'categorias_custos': {'piada': 10.0}
        }
        route = self.text_processor.route_and_process(file_data)
        self.assertEqual(route, "joke", "Esperava a rota 'joke' mas obteve outra rota.")

    def test_general_route_from_file_data(self):
        # Teste para garantir que palavras gerais escolhem a rota 'general'
        file_data = {
            'categorias_custos': {'cultura': 50.0}
        }
        route = self.text_processor.route_and_process(file_data)
        self.assertEqual(route, "general", "Esperava a rota 'general' mas obteve outra rota.")

if __name__ == '__main__':
    unittest.main()
