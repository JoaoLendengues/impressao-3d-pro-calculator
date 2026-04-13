"""
Calculadora de Impressão 3D
Aplicativo Desktop para precificação de peças impressas em 3D
"""
import sys
from interface import Interface3D
from PySide6 import QtWidgets

def main():
    """Função principal do aplicativo"""
    app = QtWidgets.QApplication(sys.argv)

    # Configurar estilo
    app.setStyle('Windows')

    # Criar e mostrar janela
    window = Interface3D()
    window.show()

    # Executar aplicação
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

