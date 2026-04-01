<div align="center">

# 🖨️ Impressão 3D Pro Calculator

### *Calculadora Profissional para Precificação de Impressões 3D*

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.0+-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

</div>

---

## 📸 Screenshots

<div align="center">
  <img src="screenshots/calculadora.png" alt="Calculadora" width="45%">
  <img src="screenshots/pedidos.png" alt="Lista de Pedidos" width="45%">
  <br>
  <img src="screenshots/relatorios.png" alt="Relatórios" width="45%">
  <img src="screenshots/configuracoes.png" alt="Configurações" width="45%">
</div>

---

## 🎯 Sobre o Projeto

O **Impressão 3D Pro Calculator** é um aplicativo desktop completo desenvolvido em Python com PySide6 (Qt) para profissionais e entusiastas de impressão 3D. Ele automatiza todo o processo de precificação, considerando todos os custos envolvidos e gerando relatórios profissionais.

### ✨ Características Principais

- **🎨 Interface Moderna** - Tema escuro profissional com gradientes e animações suaves
- **⚡ Cálculos Inteligentes** - Considera material, energia, tempo de máquina, design e margem de lucro
- **📊 Gerenciamento Completo** - CRUD completo de pedidos com controle de status
- **📈 Relatórios Detalhados** - Estatísticas em tempo real e análise de desempenho
- **💾 Banco de Dados Local** - SQLite para armazenamento seguro e rápido
- **🔧 Configurável** - Valores padrão personalizáveis para cada usuário
- **🎨 Cores por Status** - Visualização intuitiva dos pedidos por status
- **📱 Responsivo** - Interface que se adapta a diferentes tamanhos de tela

---

## 🚀 Funcionalidades

### 📊 **Cálculo de Peças**
- Cálculo preciso de custos (material, energia, tempo)
- Margem de lucro personalizável
- Campo para custo de design
- Resultados detalhados em tempo real

### 📋 **Gerenciamento de Pedidos**
- Lista completa de todos os pedidos
- Filtros por status e cliente
- Alteração de status com um clique
- Visualização detalhada de cada pedido
- Exclusão segura com confirmação

### 📈 **Relatórios e Estatísticas**
- Total de vendas realizadas
- Lucro total acumulado
- Ticket médio por pedido
- Distribuição por status
- Top clientes (próximas atualizações)

### ⚙️ **Configurações**
- Valores padrão personalizáveis
- Configurações salvas localmente
- Interface intuitiva

---

## 📦 Tecnologias Utilizadas

| Tecnologia | Versão | Descrição |
|------------|--------|-------------|
| **Python** | 3.7+ | Linguagem de programação |
| **PySide6** | 6.0+ | Framework Qt para interface gráfica |
| **SQLite3** | 3.x | Banco de dados embutido |
| **Qt Style Sheets** | - | Estilização da interface |

---

## 🔧 Instalação

### Pré-requisitos

- Python 3.7 ou superior instalado
- Pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/impressao-3d-pro-calculator.git
cd impressao-3d-pro-calculator

Crie um ambiente virtual (recomendado)

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Instale as dependências

bash
pip install PySide6
Execute o aplicativo

bash
python main.py
Nota: O banco de dados será criado automaticamente na primeira execução.

🎮 Como Usar
1. Calcular uma Peça
Preencha os dados do cliente

Informe peso do material (gramas)

Digite o tempo de impressão (horas e/ou minutos)

Preencha os custos (material, energia, taxa horária)

Adicione custo de design (opcional)

Defina a margem de lucro desejada

Clique em "CALCULAR PREÇO"

Visualize o resultado detalhado

Clique em "SALVAR PEDIDO" para registrar

2. Gerenciar Pedidos
Na aba "PEDIDOS", visualize todos os pedidos

Use os botões para:

👁️ Ver Detalhes - Informações completas do pedido

🔄 Alterar Status - Atualize o andamento

🗑️ Excluir - Remova pedidos (com confirmação)

⟳ Atualizar - Recarregue a lista

3. Status Disponíveis
Status	Cor	Descrição
🟠 Pendente	Laranja	Aguardando início da impressão
🔵 Em andamento	Azul	Impressão em progresso
🟣 Concluído	Roxo	Peça pronta para entrega
🟢 Entregue	Verde	Pedido finalizado
4. Configurar Padrões
Na aba "CONFIGURAÇÕES", você pode definir:

Custo padrão do material (R$/kg)

Consumo médio da impressora (watts)

Custo da energia elétrica (R$/kWh)

Taxa horária de trabalho (R$/hora)

Margem de lucro padrão (%)

📊 Fórmulas Utilizadas
Cálculo de Custos
text
Custo do Material = (Peso em gramas / 1000) × Custo por kg

Consumo de Energia = (Potência em watts × Tempo em horas) / 1000
Custo de Energia = Consumo em kWh × Custo por kWh

Custo do Tempo = Tempo em horas × Taxa horária

Custo Total = Custo Material + Custo Energia + Custo Tempo + Custo Design

Lucro = Custo Total × (Margem de Lucro / 100)

Valor de Venda = Custo Total + Lucro
🗂️ Estrutura do Projeto
text
impressao-3d-pro-calculator/
│
├── main.py                 # Ponto de entrada do aplicativo
├── calculadora.py          # Lógica de cálculos
├── banco_dados.py          # Gerenciamento do banco de dados
├── interface.py            # Interface gráfica com PySide6
├── impressao_3d.db         # Banco de dados SQLite (criado automaticamente)
│
├── screenshots/            # Imagens para documentação
│   ├── calculadora.png
│   ├── pedidos.png
│   ├── relatorios.png
│   └── configuracoes.png
│
└── README.md               # Documentação
🤝 Contribuindo
Contribuições são muito bem-vindas! Siga estes passos:

Fork o projeto

Crie sua branch de feature

bash
git checkout -b feature/nova-funcionalidade
Commit suas mudanças

bash
git commit -m 'feat: Adiciona nova funcionalidade incrível'
Push para a branch

bash
git push origin feature/nova-funcionalidade
Abra um Pull Request

Sugestões de Melhorias
Exportar relatórios para PDF

Gráficos de vendas mensais

Backup automático do banco de dados

Múltiplos perfis de impressora

Suporte a diferentes tipos de filamento

Modo escuro/claro alternável

Notificações de pedidos pendentes

Importação/exportação de dados em CSV

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

👨‍💻 Autor
JoaoLendengues

https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white

🙏 Agradecimentos
Qt for Python - Framework incrível para interfaces

SQLite - Banco de dados leve e eficiente

Comunidade Python pelo suporte e bibliotecas

⭐ Mostre seu Apoio
Se este projeto te ajudou, dê uma ⭐ no repositório! Isso me motiva a continuar melhorando.

<div align="center"> <sub>Feito com ❤️ para a comunidade de impressão 3D</sub> </div> ```