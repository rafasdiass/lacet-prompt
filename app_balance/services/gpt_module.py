from app_balance.services.gpt_service import analyze_data
from typing import Dict
from app_balance.models import Recebimento
from sqlalchemy.orm import session

class CatelinaLacetGPT:
    """
    A simpática e bem-humorada IA 'Catelina Lacet' que usa GPT-4 para fornecer análises
    financeiras com referências divertidas a filmes, heróis, cultura pop e humor.
    Ela mistura dados financeiros complexos com uma abordagem leve e divertida.
    Catelina Lacet tem 45 anos, é geek, arquiteta, mãe de pet e bem-humorada.
    """

    def __init__(self, tipo_humor: str = 'padrao'):
        self.tipo_humor = tipo_humor
        self.dados_aprendidos = []  # Armazenará os dados aprendidos

    def generate_gpt_response(self, prompt: str) -> str:
        """
        Gera uma resposta usando GPT-4, chamando a função no serviço `openai_service`.
        Se houver um problema, retorna uma resposta fluida baseada nos dados locais.
        """
        try:
            return analyze_data(prompt)
        except Exception:
            return self.simulate_gpt_response(prompt)  # Não diferencia erro, apenas simula uma resposta fluida

    def simulate_gpt_response(self, prompt: str) -> str:
        """
        Simula uma resposta da IA, utilizando dados do banco de dados e gerando uma resposta fluida.
        """
        # Checando se o prompt é "qual seu nome?" para resposta personalizada
        if "qual seu nome" in prompt.lower():
            return "Meu nome é Catelina Lacet! Sou uma IA geek, arquiteta, mãe de pet e sempre pronta para te ajudar com suas finanças!"

        # Caso não seja sobre o nome, utiliza os dados locais de recebimentos
        recebimentos = session.query(Recebimento).all()
        if recebimentos:
            total_recebimentos = sum([r.valor for r in recebimentos])
            resposta_base = f"Ah, {total_recebimentos:.2f} reais recebidos recentemente! Parece que as finanças estão no caminho certo. "
            
            if self.tipo_humor == 'sarcastico':
                return resposta_base + "Agora, se você conseguir segurar esses ganhos sem gastar tudo em gadgets como Tony Stark, talvez tenhamos uma chance!"
            elif self.tipo_humor == 'compreensivo':
                return resposta_base + "Estou aqui para ajudar! Vamos trabalhar juntos para garantir que tudo fique sob controle, como a Mulher Maravilha organizando suas finanças."
            else:  # padrão
                return resposta_base + "Mantenha o foco, assim como Marty McFly manteve o DeLorean a 88 milhas por hora. Estamos indo para o futuro financeiro!"
        else:
            if self.tipo_humor == 'sarcastico':
                return "Bem, sem dados financeiros, parece que você está mais perdido do que o Thor sem o martelo. Que tal começar adicionando algumas informações?"
            elif self.tipo_humor == 'compreensivo':
                return "Entendo que estamos sem dados por enquanto, mas juntos encontraremos o caminho certo. Vamos começar devagar e construir algo sólido, ok?"
            else:  # padrão
                return "Sem dados por enquanto, mas tudo bem! Vamos organizar isso e garantir que você tenha tudo em ordem. Como Marty McFly, estamos só começando!"

    def aprender_com_dados(self, novos_dados: Dict):
        """
        A Catelina Lacet aprende com novos dados fornecidos e os usa para aprimorar respostas futuras.

        Args:
            novos_dados (Dict): Um dicionário contendo os novos dados que a IA deve aprender.
        
        Returns:
            str: Uma mensagem confirmando que os dados foram aprendidos.
        """
        self.dados_aprendidos.append(novos_dados)
        return "Obrigada pelos novos dados! Estou aprendendo e ficarei ainda mais afiada em minhas análises."
