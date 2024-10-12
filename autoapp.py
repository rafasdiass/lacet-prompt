# -*- coding: utf-8 -*-
"""Create an application instance."""
from app_balance.app import create_app
from app_balance.settings import Config

# Cria a instância da aplicação com as configurações especificadas
app = create_app(config_object=Config)

# Verifica se a aplicação está configurada para usar a GUI ou o modo de servidor
if Config.USE_GUI:
    from app_balance.gui_app import run_gui
    # Inicia a aplicação GUI
    run_gui()
else:
    # Inicia o servidor Flask para modo web
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)
