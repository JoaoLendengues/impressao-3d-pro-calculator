"""
Interface gráfica com PySide6 - Tema Escuro Moderno
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTabWidget, QTableWidget,
    QTableWidgetItem, QTextEdit, QGroupBox, QMessageBox, QComboBox,
    QHeaderView, QDialog, QDialogButtonBox, QFrame, QScrollArea,
    QSizePolicy, QSplitter
)
from PySide6.QtCore import Qt, Signal, QSize, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush, QIcon, QPixmap
from calculadora import Calculadora3D
from banco_dados import BancoDados
from updater import UpdateManager

class Interface3D(QMainWindow):
    """Janela principal do aplicativo com tema escuro moderno"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Impressão 3D")
        self.setMinimumSize(1300, 750)
        
        # Inicializar componentes
        self.calculadora = Calculadora3D()
        self.banco = BancoDados()
        
        # Conectar sinais
        self.banco.dados_atualizados.connect(self.carregar_pedidos)
        
        # Carregar configurações
        self.carregar_configuracoes()
        
        # Configurar interface
        self.setup_ui()
        
        # Aplicar tema escuro
        self.aplicar_tema_escuro()
        
        # Carregar dados iniciais
        self.carregar_pedidos()
        self.atualizar_estatisticas()

        # Configurar sistema de atualizações
        self.setup_update_system()
    
    def aplicar_tema_escuro(self):
        """Aplica um tema escuro moderno"""
        self.setStyleSheet("""
            /* Estilo geral */
            QMainWindow {
                background-color: #0a0e1a;
            }
            
            QWidget {
                background-color: #0a0e1a;
                color: #e4e6eb;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
            
            /* Abas */
            QTabWidget::pane {
                border: none;
                background-color: #13161f;
                border-radius: 12px;
                margin-top: -1px;
            }
            
            QTabBar::tab {
                background: #1a1f2e;
                color: #8b92a8;
                padding: 12px 28px;
                margin-right: 4px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: 500;
                font-size: 13px;
            }
            
            QTabBar::tab:hover {
                background: #252b3d;
                color: #e4e6eb;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4f46e5, stop:1 #7c3aed);
                color: white;
            }
            
            /* GroupBox */
            QGroupBox {
                font-weight: bold;
                border: 1px solid #252b3d;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 12px;
                background-color: #13161f;
                font-size: 13px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                color: #8b92a8;
            }
            
            /* Botões */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4f46e5, stop:1 #7c3aed);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 10px;
                font-weight: 600;
                font-size: 13px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4338ca, stop:1 #6d28d9);
            }
            
            QPushButton:disabled {
                background: #2d2f36;
                color: #6b7280;
            }
            
            /* Campos de entrada */
            QLineEdit, QTextEdit, QComboBox {
                background-color: #1a1f2e;
                border: 1px solid #2d3246;
                border-radius: 8px;
                padding: 8px 12px;
                color: #e4e6eb;
                selection-background-color: #4f46e5;
                font-size: 13px;
            }
            
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border-color: #4f46e5;
                background-color: #1e2436;
            }
            
            QLineEdit:hover, QTextEdit:hover, QComboBox:hover {
                border-color: #6366f1;
            }
            
            /* ComboBox dropdown */
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #8b92a8;
                margin-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #1a1f2e;
                border: 1px solid #2d3246;
                border-radius: 8px;
                selection-background-color: #4f46e5;
                color: #e4e6eb;
            }
            
            /* Tabela */
            QTableWidget {
                background-color: #13161f;
                border: none;
                border-radius: 12px;
                gridline-color: #252b3d;
                font-size: 13px;
            }
            
            QTableWidget::item {
                padding: 8px;
            }
            
            QTableWidget::item:selected {
                background-color: #4f46e5;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #1a1f2e;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #4f46e5;
                font-weight: bold;
                color: #8b92a8;
                font-size: 12px;
            }
            
            QHeaderView::section:hover {
                background-color: #252b3d;
            }
            
            /* Scrollbars */
            QScrollBar:vertical {
                background-color: #13161f;
                width: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #2d3246;
                border-radius: 5px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #4f46e5;
            }
            
            QScrollBar:horizontal {
                background-color: #13161f;
                height: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:horizontal {
                background-color: #2d3246;
                border-radius: 5px;
                min-width: 30px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background-color: #4f46e5;
            }
            
            /* Labels */
            QLabel {
                color: #e4e6eb;
                font-size: 13px;
            }
            
            /* Status Bar */
            QStatusBar {
                background-color: #0a0e1a;
                color: #8b92a8;
                padding: 5px;
                font-size: 12px;
            }
            
            /* TextEdit específico para resultados */
            QTextEdit#resultadoText {
                background-color: #0a0e1a;
                border: 1px solid #2d3246;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            
            /* Separador */
            QFrame[frameShape="4"] {
                background-color: #2d3246;
                max-height: 1px;
            }
        """)
    
    def carregar_configuracoes(self):
        """Carrega configurações salvas ou usa padrões"""
        self.config = {
            'custo_material': self.banco.obter_configuracao('custo_material', '150.00'),
            'consumo': self.banco.obter_configuracao('consumo', '250'),
            'custo_energia': self.banco.obter_configuracao('custo_energia', '0.80'),
            'taxa_horaria': self.banco.obter_configuracao('taxa_horaria', '20.00'),
            'margem': self.banco.obter_configuracao('margem', '30')
        }
    
    def setup_ui(self):
        """Configura toda a interface"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header com gradiente
        self.criar_header()
        layout.addWidget(self.header)
        
        # Criar abas
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        layout.addWidget(self.tabs)
        
        # Aba de cálculo
        self.aba_calculo = QWidget()
        self.tabs.addTab(self.aba_calculo, "  📊  CÁLCULO  ")
        self.setup_aba_calculo()
        
        # Aba de pedidos
        self.aba_pedidos = QWidget()
        self.tabs.addTab(self.aba_pedidos, "  📋  PEDIDOS  ")
        self.setup_aba_pedidos()
        
        # Aba de configurações
        self.aba_config = QWidget()
        self.tabs.addTab(self.aba_config, "  ⚙️  CONFIGURAÇÕES  ")
        self.setup_aba_configuracoes()
        
        # Barra de status
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("✓ Sistema pronto")
    
    def criar_header(self):
        """Cria o cabeçalho com gradiente"""
        self.header = QWidget()
        self.header.setFixedHeight(80)
        
        # Gradiente para o header
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(79, 70, 229))  # #4f46e5
        gradient.setColorAt(1, QColor(124, 58, 237))  # #7c3aed
        
        palette = self.header.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.header.setPalette(palette)
        self.header.setAutoFillBackground(True)
        
        # Layout do header
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(30, 0, 30, 0)
        
        # Título e subtítulo
        titulo_layout = QVBoxLayout()
        
        titulo = QLabel("IMPRESSÃO 3D PRO")
        titulo.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: white;
            letter-spacing: 1px;
        """)
        titulo_layout.addWidget(titulo)
        
        subtitulo = QLabel("Calculadora Profissional de Preços")
        subtitulo.setStyleSheet("""
            font-size: 12px;
            color: rgba(255, 255, 255, 0.8);
        """)
        titulo_layout.addWidget(subtitulo)
        
        header_layout.addLayout(titulo_layout)
        header_layout.addStretch()
        
        # Informações rápidas
        info_layout = QHBoxLayout()
        
        self.pedidos_hoje_label = QLabel("📦 0 pedidos")
        self.pedidos_hoje_label.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.15);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            color: white;
        """)
        info_layout.addWidget(self.pedidos_hoje_label)
        
        header_layout.addLayout(info_layout)
    
    def setup_aba_calculo(self):
        """Configura a aba de cálculo com design moderno"""
        # Layout principal com scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        content = QWidget()
        scroll.setWidget(content)
        
        layout = QHBoxLayout(content)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Frame esquerdo - Dados de entrada
        frame_entrada = QGroupBox("DADOS DA IMPRESSÃO")
        frame_entrada.setMinimumWidth(500)
        
        entrada_layout = QGridLayout(frame_entrada)
        entrada_layout.setSpacing(15)
        entrada_layout.setContentsMargins(20, 25, 20, 25)
        
        row = 0
        
        # Cliente
        label_cliente = QLabel("👤 CLIENTE")
        label_cliente.setStyleSheet("color: #8b92a8; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;")
        entrada_layout.addWidget(label_cliente, row, 0)
        self.cliente_edit = QLineEdit()
        self.cliente_edit.setPlaceholderText("Nome do cliente")
        self.cliente_edit.setMinimumHeight(40)
        entrada_layout.addWidget(self.cliente_edit, row, 1)
        row += 1
        
        # Peso
        label_peso = QLabel("⚖️ PESO DO MATERIAL")
        label_peso.setStyleSheet("color: #8b92a8; font-size: 11px; font-weight: bold;")
        entrada_layout.addWidget(label_peso, row, 0)
        self.peso_edit = QLineEdit()
        self.peso_edit.setPlaceholderText("Ex: 250")
        self.peso_edit.setMinimumHeight(40)
        entrada_layout.addWidget(self.peso_edit, row, 1)
        entrada_layout.addWidget(QLabel("gramas"), row, 2)
        row += 1
        
        # Tempo
        label_tempo = QLabel("⏱️ TEMPO DE IMPRESSÃO")
        label_tempo.setStyleSheet("color: #8b92a8; font-size: 11px; font-weight: bold;")
        entrada_layout.addWidget(label_tempo, row, 0)
        
        tempo_layout = QHBoxLayout()
        self.horas_edit = QLineEdit()
        self.horas_edit.setPlaceholderText("horas")
        self.horas_edit.setMinimumHeight(40)
        self.horas_edit.setMaximumWidth(100)
        tempo_layout.addWidget(self.horas_edit)
        tempo_layout.addWidget(QLabel("horas"))
        
        self.minutos_edit = QLineEdit()
        self.minutos_edit.setPlaceholderText("minutos")
        self.minutos_edit.setMinimumHeight(40)
        self.minutos_edit.setMaximumWidth(100)
        tempo_layout.addWidget(self.minutos_edit)
        tempo_layout.addWidget(QLabel("minutos"))
        tempo_layout.addStretch()
        
        entrada_layout.addLayout(tempo_layout, row, 1, 1, 2)
        row += 1
        
        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setStyleSheet("background-color: #2d3246; max-height: 1px;")
        entrada_layout.addWidget(separador, row, 0, 1, 3)
        row += 1
        
        # Custos
        custos = [
            ("💰 CUSTO DO MATERIAL (R$/kg):", "custo_material", self.config['custo_material']),
            ("⚡ CONSUMO DA IMPRESSORA (watts):", "consumo", self.config['consumo']),
            ("💡 CUSTO DA ENERGIA (R$/kWh):", "custo_energia", self.config['custo_energia']),
            ("⏰ TAXA HORÁRIA (R$/hora):", "taxa_horaria", self.config['taxa_horaria']),
            ("🎨 CUSTO DE DESIGN (R$):", "custo_design", "0"),
            ("📈 MARGEM DE LUCRO (%):", "margem", self.config['margem'])
        ]
        
        for label, attr, valor in custos:
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #8b92a8; font-size: 11px; font-weight: bold;")
            entrada_layout.addWidget(lbl, row, 0)
            
            edit = QLineEdit(valor)
            edit.setMinimumHeight(40)
            setattr(self, f"{attr}_edit", edit)
            entrada_layout.addWidget(edit, row, 1)
            row += 1
        
        # Observações
        label_obs = QLabel("📝 OBSERVAÇÕES")
        label_obs.setStyleSheet("color: #8b92a8; font-size: 11px; font-weight: bold;")
        entrada_layout.addWidget(label_obs, row, 0)
        self.obs_text = QTextEdit()
        self.obs_text.setMaximumHeight(80)
        self.obs_text.setPlaceholderText("Observações adicionais...")
        entrada_layout.addWidget(self.obs_text, row, 1, 1, 2)
        row += 1
        
        # Botões
        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(15)
        
        self.calcular_btn = QPushButton("CALCULAR PREÇO")
        self.calcular_btn.setMinimumHeight(45)
        self.calcular_btn.setCursor(Qt.PointingHandCursor)
        self.calcular_btn.clicked.connect(self.calcular)
        botoes_layout.addWidget(self.calcular_btn)
        
        self.salvar_btn = QPushButton("SALVAR PEDIDO")
        self.salvar_btn.setMinimumHeight(45)
        self.salvar_btn.setCursor(Qt.PointingHandCursor)
        self.salvar_btn.clicked.connect(self.salvar_pedido)
        botoes_layout.addWidget(self.salvar_btn)
        
        self.limpar_btn = QPushButton("LIMPAR")
        self.limpar_btn.setMinimumHeight(45)
        self.limpar_btn.setCursor(Qt.PointingHandCursor)
        self.limpar_btn.clicked.connect(self.limpar_campos)
        botoes_layout.addWidget(self.limpar_btn)
        
        botoes_layout.addStretch()
        entrada_layout.addLayout(botoes_layout, row, 0, 1, 3)
        
        # Frame direito - Resultados
        frame_resultado = QGroupBox("RESULTADO")
        frame_resultado.setMinimumWidth(500)
        
        resultado_layout = QVBoxLayout(frame_resultado)
        resultado_layout.setContentsMargins(20, 25, 20, 20)
        
        self.resultado_text = QTextEdit()
        self.resultado_text.setObjectName("resultadoText")
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setMinimumHeight(500)
        resultado_layout.addWidget(self.resultado_text)
        
        # Adicionar ao layout principal
        layout.addWidget(frame_entrada)
        layout.addWidget(frame_resultado)
        
        # Adicionar scroll ao layout principal
        main_layout = QVBoxLayout(self.aba_calculo)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def setup_aba_pedidos(self):
        """Configura a aba de pedidos com design moderno"""
        layout = QVBoxLayout(self.aba_pedidos)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título da seção
        titulo = QLabel("GERENCIAMENTO DE PEDIDOS")
        titulo.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #e4e6eb;
            letter-spacing: 1px;
        """)
        layout.addWidget(titulo)
        
        # Tabela de pedidos
        self.tabela_pedidos = QTableWidget()
        self.tabela_pedidos.setColumnCount(7)
        self.tabela_pedidos.setHorizontalHeaderLabels(
            ["ID", "CLIENTE", "DATA", "STATUS", "PESO (g)", "TEMPO (h)", "VALOR (R$)"]
        )
        self.tabela_pedidos.horizontalHeader().setStretchLastSection(True)
        self.tabela_pedidos.setAlternatingRowColors(True)
        self.tabela_pedidos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_pedidos.setShowGrid(False)
        self.tabela_pedidos.verticalHeader().setVisible(False)
        self.tabela_pedidos.doubleClicked.connect(self.ver_detalhes)
        layout.addWidget(self.tabela_pedidos)
        
        # Botões de ação
        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(12)
        
        self.atualizar_btn = QPushButton("⟳ ATUALIZAR")
        self.atualizar_btn.setCursor(Qt.PointingHandCursor)
        self.atualizar_btn.clicked.connect(self.carregar_pedidos)
        botoes_layout.addWidget(self.atualizar_btn)
        
        self.detalhes_btn = QPushButton("👁️ VER DETALHES")
        self.detalhes_btn.setCursor(Qt.PointingHandCursor)
        self.detalhes_btn.clicked.connect(self.ver_detalhes)
        botoes_layout.addWidget(self.detalhes_btn)
        
        self.status_btn = QPushButton("🔄 ALTERAR STATUS")
        self.status_btn.setCursor(Qt.PointingHandCursor)
        self.status_btn.clicked.connect(self.alterar_status)
        botoes_layout.addWidget(self.status_btn)
        
        self.excluir_btn = QPushButton("🗑️ EXCLUIR")
        self.excluir_btn.setCursor(Qt.PointingHandCursor)
        self.excluir_btn.clicked.connect(self.excluir_pedido)
        botoes_layout.addWidget(self.excluir_btn)
        
        botoes_layout.addStretch()
        layout.addLayout(botoes_layout)
        
        # Card de resumo
        self.resumo_card = QWidget()
        self.resumo_card.setStyleSheet("""
            QWidget {
                background-color: #13161f;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        card_layout = QHBoxLayout(self.resumo_card)
        
        self.resumo_label = QLabel()
        self.resumo_label.setStyleSheet("""
            font-size: 13px;
            color: #8b92a8;
        """)
        card_layout.addWidget(self.resumo_label)
        card_layout.addStretch()
        
        layout.addWidget(self.resumo_card)
    
    def setup_aba_configuracoes(self):
        """Configura a aba de configurações com design moderno"""
        # Layout principal com scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        content = QWidget()
        scroll.setWidget(content)
        
        layout = QHBoxLayout(content)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Configurações
        frame_config = QGroupBox("CONFIGURAÇÕES PADRÃO")
        frame_config.setMinimumWidth(500)
        
        config_layout = QGridLayout(frame_config)
        config_layout.setSpacing(15)
        config_layout.setContentsMargins(20, 25, 20, 25)
        
        configs = [
            ("💰 Custo do material (R$/kg):", "custo_material", "150.00", "Valor do filamento por quilo"),
            ("⚡ Consumo da impressora (watts):", "consumo", "250", "Consumo médio da impressora"),
            ("💡 Custo da energia (R$/kWh):", "custo_energia", "0.80", "Tarifa de energia elétrica"),
            ("⏰ Taxa horária (R$/hora):", "taxa_horaria", "20.00", "Valor da hora de impressão"),
            ("📈 Margem de lucro padrão (%):", "margem", "30", "Margem de lucro recomendada")
        ]
        
        self.config_widgets = {}
        
        for i, (label, chave, padrao, desc) in enumerate(configs):
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #8b92a8; font-size: 12px; font-weight: bold;")
            config_layout.addWidget(lbl, i, 0)
            
            edit = QLineEdit(self.banco.obter_configuracao(chave, padrao))
            edit.setMinimumHeight(40)
            self.config_widgets[chave] = edit
            config_layout.addWidget(edit, i, 1)
            
            desc_lbl = QLabel(desc)
            desc_lbl.setStyleSheet("color: #6b7280; font-size: 11px;")
            config_layout.addWidget(desc_lbl, i, 2)
        
        self.salvar_config_btn = QPushButton("💾 SALVAR CONFIGURAÇÕES")
        self.salvar_config_btn.setMinimumHeight(45)
        self.salvar_config_btn.setCursor(Qt.PointingHandCursor)
        self.salvar_config_btn.clicked.connect(self.salvar_configuracoes)
        config_layout.addWidget(self.salvar_config_btn, len(configs), 0, 1, 3)
        
        # Estatísticas
        frame_stats = QGroupBox("ESTATÍSTICAS")
        frame_stats.setMinimumWidth(450)
        
        stats_layout = QVBoxLayout(frame_stats)
        stats_layout.setContentsMargins(20, 25, 20, 20)
        
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setFont(QFont("Consolas", 11))
        self.stats_text.setMinimumHeight(350)
        stats_layout.addWidget(self.stats_text)
        
        self.atualizar_stats_btn = QPushButton("⟳ ATUALIZAR ESTATÍSTICAS")
        self.atualizar_stats_btn.setMinimumHeight(40)
        self.atualizar_stats_btn.setCursor(Qt.PointingHandCursor)
        self.atualizar_stats_btn.clicked.connect(self.atualizar_estatisticas)
        stats_layout.addWidget(self.atualizar_stats_btn)
        
        # Adicionar ao layout
        layout.addWidget(frame_config)
        layout.addWidget(frame_stats)
        
        main_layout = QVBoxLayout(self.aba_config)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def calcular(self):
        """Realiza o cálculo da peça"""
        try:
            # Coletar dados
            dados = {
                'peso_g': self.peso_edit.text(),
                'horas': self.horas_edit.text() or '0',
                'minutos': self.minutos_edit.text() or '0',
                'custo_material_kg': self.custo_material_edit.text(),
                'consumo_watts': self.consumo_edit.text(),
                'custo_energia_kwh': self.custo_energia_edit.text(),
                'taxa_horaria': self.taxa_horaria_edit.text(),
                'custo_design': self.custo_design_edit.text() or '0',
                'margem_lucro': self.margem_edit.text()
            }
            
            # Validar dados
            valido, msg = self.calculadora.validar_dados(dados)
            if not valido:
                QMessageBox.warning(self, "Aviso", msg)
                return
            
            # Converter para números
            dados = {k: float(v) if v else 0 for k, v in dados.items()}
            
            # Calcular
            resultados = self.calculadora.calcular(dados)
            self.ultimo_calculo = resultados
            
            # Exibir resultados
            self.mostrar_resultados(resultados)
            
            self.status_bar.showMessage("✓ Cálculo realizado com sucesso!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao calcular: {str(e)}")
    
    def mostrar_resultados(self, r):
        """Exibe os resultados formatados com estilo"""
        texto = f"""
{'═'*48}╗
{' ' * 12}DETALHES DO CÁLCULO{' ' * 13}
{'═'*48}╣
                                                       
  📊 DADOS DE ENTRADA                                  
  ├─ Peso: {r['peso_g']:>8.2f} g{' ' * 25}
  └─ Tempo: {r['tempo_total']:>7.2f} horas{' ' * 25}
                                                       
  💰 CUSTOS                                           
  ├─ Material:      R$ {r['custo_material']:>10.2f}{' ' * 17}
  ├─ Eletricidade:  R$ {r['custo_eletricidade']:>10.2f}{' ' * 17}
  ├─ Tempo:         R$ {r['custo_tempo']:>10.2f}{' ' * 17}
  └─ Design:        R$ {r['custo_design']:>10.2f}{' ' * 17}
                                                       
  {'─'*44}                                            
  📊 SUBTOTAL:        R$ {r['custo_total']:>10.2f}{' ' * 17}
  📈 LUCRO ({r['margem_percentual']:>5.1f}%):      R$ {r['lucro']:>10.2f}{' ' * 17}
                                                       
  {'═'*44}                                            
  🎯 VALOR DE VENDA:  R$ {r['valor_venda']:>10.2f}{' ' * 17}
  {'═'*44}                                            
{'═'*48}╝
"""
        self.resultado_text.setText(texto)
    
    def salvar_pedido(self):
        """Salva o pedido no banco de dados"""
        if not hasattr(self, 'ultimo_calculo'):
            QMessageBox.warning(self, "Aviso", "Calcule o valor primeiro!")
            return
        
        cliente = self.cliente_edit.text().strip()
        if not cliente:
            QMessageBox.warning(self, "Aviso", "Informe o nome do cliente!")
            return
        
        try:
            # Preparar dados
            dados_pedido = {
                'cliente': cliente,
                'peso_material': float(self.peso_edit.text()) if self.peso_edit.text() else 0,
                'tempo_impressao': self.ultimo_calculo['tempo_total'],
                'custo_material': self.ultimo_calculo['custo_material'],
                'custo_eletricidade': self.ultimo_calculo['custo_eletricidade'],
                'custo_tempo': self.ultimo_calculo['custo_tempo'],
                'custo_design': float(self.custo_design_edit.text()) if self.custo_design_edit.text() else 0,
                'custo_total': self.ultimo_calculo['custo_total'],
                'valor_venda': self.ultimo_calculo['valor_venda'],
                'lucro': self.ultimo_calculo['lucro'],
                'observacoes': self.obs_text.toPlainText().strip()
            }
            
            # Salvar
            pedido_id = self.banco.salvar_pedido(dados_pedido)
            
            QMessageBox.information(self, "Sucesso", f"✅ Pedido #{pedido_id} salvo com sucesso!")
            
            # Limpar campos
            self.limpar_campos()
            
            self.status_bar.showMessage(f"✓ Pedido #{pedido_id} salvo!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar: {str(e)}")
    
    def limpar_campos(self):
        """Limpa todos os campos"""
        self.cliente_edit.clear()
        self.peso_edit.clear()
        self.horas_edit.clear()
        self.minutos_edit.clear()
        self.custo_design_edit.clear()
        self.obs_text.clear()
        self.resultado_text.clear()
        if hasattr(self, 'ultimo_calculo'):
            delattr(self, 'ultimo_calculo')
    
    def carregar_pedidos(self):
        """Carrega os pedidos na tabela"""
        pedidos = self.banco.listar_pedidos()
        
        self.tabela_pedidos.setRowCount(len(pedidos))
        
        for i, pedido in enumerate(pedidos):
            self.tabela_pedidos.setItem(i, 0, QTableWidgetItem(str(pedido['id'])))
            self.tabela_pedidos.setItem(i, 1, QTableWidgetItem(pedido['cliente']))
            self.tabela_pedidos.setItem(i, 2, QTableWidgetItem(pedido['data_pedido']))
            
            # Status com cores
            status_item = QTableWidgetItem(pedido['status'])
            if pedido['status'] == 'Entregue':
                status_item.setForeground(QColor(34, 197, 94))  # Verde
            elif pedido['status'] == 'Pendente':
                status_item.setForeground(QColor(245, 158, 11))  # Laranja
            elif pedido['status'] == 'Em andamento':
                status_item.setForeground(QColor(59, 130, 246))  # Azul
            elif pedido['status'] == 'Concluído':
                status_item.setForeground(QColor(168, 85, 247))  # Roxo
            self.tabela_pedidos.setItem(i, 3, status_item)
            
            self.tabela_pedidos.setItem(i, 4, QTableWidgetItem(f"{pedido['peso_material']:.1f}"))
            self.tabela_pedidos.setItem(i, 5, QTableWidgetItem(f"{pedido['tempo_impressao']:.1f}"))
            self.tabela_pedidos.setItem(i, 6, QTableWidgetItem(f"R$ {pedido['valor_venda']:.2f}"))
        
        # Ajustar altura das linhas
        for i in range(len(pedidos)):
            self.tabela_pedidos.setRowHeight(i, 40)
        
        # Ajustar largura das colunas
        self.tabela_pedidos.resizeColumnsToContents()
        
        # Atualizar resumo
        stats = self.banco.obter_estatisticas()
        self.resumo_label.setText(
            f"📊 Total de pedidos: {stats['total_pedidos']} | "
            f"💰 Vendas: R$ {stats['total_vendas']:.2f} | "
            f"📈 Lucro: R$ {stats['total_lucro']:.2f} | "
            f"🎫 Ticket médio: R$ {stats['ticket_medio']:.2f}"
        )
        
        # Atualizar header
        self.pedidos_hoje_label.setText(f"📦 {stats['total_pedidos']} pedidos")
    
    def ver_detalhes(self):
        """Mostra detalhes do pedido selecionado"""
        current_row = self.tabela_pedidos.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um pedido!")
            return
        
        pedido_id = int(self.tabela_pedidos.item(current_row, 0).text())
        pedido = self.banco.obter_pedido(pedido_id)
        
        if pedido:
            self.mostrar_detalhes_pedido(pedido)
    
    def mostrar_detalhes_pedido(self, pedido):
        """Exibe janela com detalhes do pedido com estilo moderno"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Detalhes do Pedido #{pedido['id']}")
        dialog.setMinimumSize(600, 650)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #0a0e1a;
            }
            QLabel {
                color: #e4e6eb;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Texto com detalhes
        text = QTextEdit()
        text.setReadOnly(True)
        text.setFont(QFont("Consolas", 10))
        text.setStyleSheet("""
            QTextEdit {
                background-color: #13161f;
                border: 1px solid #2d3246;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        # Calcular margem
        margem = (pedido['lucro'] / pedido['custo_total'] * 100) if pedido['custo_total'] > 0 else 0
        
        conteudo = f"""
{'═'*56}
{' ' * 18}DETALHES DO PEDIDO #{pedido['id']}{' ' * 19}
{'═'*56}
                                                          
  📋 INFORMAÇÕES GERAIS                                  
  ├─ Cliente: {pedido['cliente']:<35}
  ├─ Data do Pedido: {pedido['data_pedido']:<35}
  ├─ Data de Entrega: {(pedido['data_entrega'] or 'Não entregue'):<35}
  └─ Status: {pedido['status']:<41}
                                                      
  🖨️ DADOS DA IMPRESSÃO                                  
  ├─ Peso do Material: {pedido['peso_material']:>6.2f} g{' ' * 36}
  └─ Tempo de Impressão: {pedido['tempo_impressao']:>6.2f} horas{' ' * 31}
                                                          
  💰 CUSTOS                                              
  ├─ Custo do Material:     R$ {pedido['custo_material']:>9.2f}{' ' * 28}
  ├─ Custo de Eletricidade: R$ {pedido['custo_eletricidade']:>9.2f}{' ' * 28}
  ├─ Custo do Tempo:        R$ {pedido['custo_tempo']:>9.2f}{' ' * 28}
  └─ Custo de Design:       R$ {pedido['custo_design']:>9.2f}{' ' * 28}
                                                          
  {'─'*52}                                               
  📊 Custo Total:            R$ {pedido['custo_total']:>9.2f}{' ' * 28}
                                                          
  🎯 VALORES FINAIS                                      
  ├─ Valor de Venda:        R$ {pedido['valor_venda']:>9.2f}{' ' * 28}
  ├─ Lucro:                 R$ {pedido['lucro']:>9.2f}{' ' * 28}
  └─ Margem de Lucro:       {margem:>6.1f}%{' ' * 37}║
                                                          
  📝 OBSERVAÇÕES                                         
  {pedido['observacoes'] or 'Nenhuma observação'}{' ' * (52 - len(pedido.get('observacoes', 'Nenhuma observação')))}║
                                                          
{'═'*56}
"""
        text.setText(conteudo)
        layout.addWidget(text)
        
        # Botão fechar
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        button_box.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4f46e5, stop:1 #7c3aed);
                padding: 10px 30px;
                min-width: 120px;
            }
        """)
        layout.addWidget(button_box)
        
        dialog.exec()
    
    def alterar_status(self):
        """Altera o status do pedido selecionado"""
        current_row = self.tabela_pedidos.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um pedido!")
            return
        
        pedido_id = int(self.tabela_pedidos.item(current_row, 0).text())
        status_atual = self.tabela_pedidos.item(current_row, 3).text()
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Alterar Status - Pedido #{pedido_id}")
        dialog.setMinimumWidth(350)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #0a0e1a;
            }
            QLabel {
                color: #e4e6eb;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        layout.addWidget(QLabel(f"Status atual: {status_atual}"))
        layout.addWidget(QLabel("Novo status:"))
        
        combo = QComboBox()
        combo.addItems(['Pendente', 'Em andamento', 'Concluído', 'Entregue'])
        combo.setCurrentText(status_atual)
        combo.setMinimumHeight(35)
        layout.addWidget(combo)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        if dialog.exec() == QDialog.Accepted:
            novo_status = combo.currentText()
            if self.banco.atualizar_status(pedido_id, novo_status):
                QMessageBox.information(self, "Sucesso", f"✅ Status alterado para '{novo_status}'!")
                self.status_bar.showMessage(f"✓ Pedido #{pedido_id} atualizado")
    
    def excluir_pedido(self):
        """Exclui o pedido selecionado"""
        current_row = self.tabela_pedidos.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um pedido!")
            return
        
        pedido_id = int(self.tabela_pedidos.item(current_row, 0).text())
        cliente = self.tabela_pedidos.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirmar exclusão",
            f"Tem certeza que deseja excluir o pedido de {cliente}?\n\nEsta ação não pode ser desfeita!",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.banco.excluir_pedido(pedido_id):
                QMessageBox.information(self, "Sucesso", "✅ Pedido excluído com sucesso!")
                self.status_bar.showMessage(f"✓ Pedido #{pedido_id} excluído")
    
    def salvar_configuracoes(self):
        """Salva as configurações"""
        for chave, widget in self.config_widgets.items():
            self.banco.salvar_configuracao(chave, widget.text())
        
        # Recarregar configurações
        self.carregar_configuracoes()
        
        # Atualizar campos na aba de cálculo
        self.custo_material_edit.setText(self.config['custo_material'])
        self.consumo_edit.setText(self.config['consumo'])
        self.custo_energia_edit.setText(self.config['custo_energia'])
        self.taxa_horaria_edit.setText(self.config['taxa_horaria'])
        self.margem_edit.setText(self.config['margem'])
        
        QMessageBox.information(self, "Sucesso", "✅ Configurações salvas com sucesso!")
        self.status_bar.showMessage("✓ Configurações atualizadas")
    
    def atualizar_estatisticas(self):
        """Atualiza as estatísticas na aba de configurações"""
        stats = self.banco.obter_estatisticas()
        
        texto = f"""
{'═'*48}╗
{' ' * 15}ESTATÍSTICAS GERAIS{' ' * 16}
{'═'*48}
                                                       
  📊 RESULTADOS TOTAIS                                 
  ├─ Total de Pedidos:  {stats['total_pedidos']:>6}{' ' * 30}
  ├─ Total de Vendas:   R$ {stats['total_vendas']:>10,.2f}{' ' * 20}
  ├─ Total de Lucro:    R$ {stats['total_lucro']:>10,.2f}{' ' * 20}
  └─ Ticket Médio:      R$ {stats['ticket_medio']:>10,.2f}{' ' * 20}
                                                       
  📈 DISTRIBUIÇÃO POR STATUS                           
"""
        for status, count in stats['status_count'].items():
            texto += f"║  ├─ {status:<12}: {count:>3} pedidos{' ' * 31}\n"
        
        texto += f"""
                                                       
{'═'*48}╝
"""
        
        self.stats_text.setText(texto)

    def setup_update_system(self):
        """Configura o sistema de atualizações"""
        self.update_manager = UpdateManager(os.path.dirname(os.path.abspath(__file__)))
        
        # Verificar atualizações em background (apenas se já passou 24h)
        if self.update_manager.should_check_for_updates():
            self.update_manager.check_for_updates(self)
        
        # Criar ação no menu para verificar manualmente
        self.create_update_menu()

    def create_update_menu(self):
        """Cria menu de atualizações na barra de menu"""
        menubar = self.menuBar()
        
        # Menu Ajuda
        ajuda_menu = menubar.addMenu("Ajuda")
        
        # Ação de verificar atualizações
        check_update_action = ajuda_menu.addAction("Verificar Atualizações")
        check_update_action.triggered.connect(self.manual_update_check)
        
        ajuda_menu.addSeparator()
        
        # Ação sobre
        about_action = ajuda_menu.addAction("Sobre")
        about_action.triggered.connect(self.show_about)

    def manual_update_check(self):
        """Verifica manualmente por atualizações"""
        self.update_manager.check_for_updates(self, show_no_update_msg=True)

    def show_about(self):
        """Mostra diálogo sobre com informações da versão"""
        QMessageBox.about(
            self,
            "Sobre o Impressão 3D Pro",
            f"""
            <h3>Impressão 3D Pro Calculator</h3>
            <p>Versão: {self.update_manager.current_version}</p>
            <p>Calculadora profissional para precificação de impressões 3D</p>
            <br>
            <p>© 2024 - Todos os direitos reservados</p>
            <p>Desenvolvido com Python e PySide6</p>
            """
        )
