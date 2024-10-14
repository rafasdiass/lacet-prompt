import unittest
from app_balance.services.text_processing import TextProcessingService

class TestTextProcessingService(unittest.TestCase):

    def setUp(self):
        self.text_processor = TextProcessingService()

    def test_financial_route_from_file_data(self):
        file_data = {
            'categorias_custos': {'finança': 100.0, 'investimento': 200.0}
        }
        route = self.text_processor.route_and_process(file_data)
        self.assertEqual(route, "financial")

    def test_joke_route_from_file_data(self):
        file_data = {
            'categorias_custos': {'piada': 10.0}
        }
        route = self.text_processor.route_and_process(file_data)
        self.assertEqual(route, "joke")

    def test_general_route_from_file_data(self):
        file_data = {
            'categorias_custos': {'cultura': 50.0}
        }
        route = self.text_processor.route_and_process(file_data)
        self.assertEqual(route, "general")


if __name__ == '__main__':
    unittest.main()
