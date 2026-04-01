"""
Gerenciamento do banco de dados SQLite
"""
import sqlite3
from datetime import datetime
from PySide6.QtCore import QObject, Signal

class BancoDados(QObject):
    """Classe para gerenciar operações com o banco de dados"""
    
    # Sinais para comunicação com a interface
    dados_atualizados = Signal()
    
    def __init__(self, arquivo="impressao_3d.db"):
        super().__init__()
        self.arquivo = arquivo
        self.criar_tabelas()
    
    def conectar(self):
        """Retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.arquivo)
    
    def criar_tabelas(self):
        """Cria as tabelas necessárias"""
        with self.conectar() as conn:
            cursor = conn.cursor()
            
            # Tabela de pedidos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente TEXT NOT NULL,
                    data_pedido TEXT NOT NULL,
                    data_entrega TEXT,
                    status TEXT DEFAULT 'Pendente',
                    peso_material REAL,
                    tempo_impressao REAL,
                    custo_material REAL,
                    custo_eletricidade REAL,
                    custo_tempo REAL,
                    custo_design REAL,
                    custo_total REAL,
                    valor_venda REAL,
                    lucro REAL,
                    observacoes TEXT
                )
            ''')
            
            # Tabela de configurações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuracoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chave TEXT UNIQUE,
                    valor TEXT,
                    descricao TEXT
                )
            ''')
            
            conn.commit()
    
    def salvar_pedido(self, dados):
        """Salva um novo pedido"""
        with self.conectar() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO pedidos (
                    cliente, data_pedido, status, peso_material, tempo_impressao,
                    custo_material, custo_eletricidade, custo_tempo, custo_design,
                    custo_total, valor_venda, lucro, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                dados['cliente'],
                datetime.now().strftime('%Y-%m-%d'),
                dados.get('status', 'Pendente'),
                dados['peso_material'],
                dados['tempo_impressao'],
                dados['custo_material'],
                dados['custo_eletricidade'],
                dados['custo_tempo'],
                dados['custo_design'],
                dados['custo_total'],
                dados['valor_venda'],
                dados['lucro'],
                dados.get('observacoes', '')
            ))
            
            conn.commit()
            self.dados_atualizados.emit()
            return cursor.lastrowid
    
    def listar_pedidos(self, filtros=None):
        """Lista todos os pedidos"""
        with self.conectar() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM pedidos ORDER BY data_pedido DESC"
            cursor.execute(query)
            
            colunas = [descricao[0] for descricao in cursor.description]
            resultados = []
            
            for row in cursor.fetchall():
                resultados.append(dict(zip(colunas, row)))
            
            return resultados
    
    def obter_pedido(self, pedido_id):
        """Obtém um pedido específico"""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,))
            
            row = cursor.fetchone()
            if row:
                colunas = [descricao[0] for descricao in cursor.description]
                return dict(zip(colunas, row))
            return None
    
    def atualizar_status(self, pedido_id, novo_status):
        """Atualiza o status de um pedido"""
        with self.conectar() as conn:
            cursor = conn.cursor()
            
            data_entrega = None
            if novo_status == 'Entregue':
                data_entrega = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute('''
                UPDATE pedidos 
                SET status = ?, data_entrega = ?
                WHERE id = ?
            ''', (novo_status, data_entrega, pedido_id))
            
            conn.commit()
            self.dados_atualizados.emit()
            return cursor.rowcount > 0
    
    def excluir_pedido(self, pedido_id):
        """Exclui um pedido"""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
            conn.commit()
            self.dados_atualizados.emit()
            return cursor.rowcount > 0
    
    def salvar_configuracao(self, chave, valor, descricao=""):
        """Salva uma configuração"""
        with self.conectar() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO configuracoes (chave, valor, descricao)
                VALUES (?, ?, ?)
                ON CONFLICT(chave) DO UPDATE SET valor = ?, descricao = ?
            ''', (chave, valor, descricao, valor, descricao))
            
            conn.commit()
    
    def obter_configuracao(self, chave, padrao=""):
        """Obtém uma configuração"""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,))
            row = cursor.fetchone()
            return row[0] if row else padrao
    
    def obter_estatisticas(self):
        """Obtém estatísticas dos pedidos"""
        with self.conectar() as conn:
            cursor = conn.cursor()
            
            # Total de pedidos
            cursor.execute("SELECT COUNT(*) FROM pedidos")
            total_pedidos = cursor.fetchone()[0]
            
            # Total de vendas
            cursor.execute("SELECT SUM(valor_venda) FROM pedidos WHERE status = 'Entregue'")
            total_vendas = cursor.fetchone()[0] or 0
            
            # Total de lucro
            cursor.execute("SELECT SUM(lucro) FROM pedidos WHERE status = 'Entregue'")
            total_lucro = cursor.fetchone()[0] or 0
            
            # Ticket médio
            ticket_medio = total_vendas / total_pedidos if total_pedidos > 0 else 0
            
            # Pedidos por status
            cursor.execute("SELECT status, COUNT(*) FROM pedidos GROUP BY status")
            status_count = dict(cursor.fetchall())
            
            return {
                'total_pedidos': total_pedidos,
                'total_vendas': total_vendas,
                'total_lucro': total_lucro,
                'ticket_medio': ticket_medio,
                'status_count': status_count
            }
        