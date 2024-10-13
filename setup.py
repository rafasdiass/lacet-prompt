from setuptools import setup, find_packages

setup(
    name='app_balance',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'qtawesome',
        'sqlalchemy',
        'environs',
        'openai',
        # Adicione outras dependências aqui
    ],
)
