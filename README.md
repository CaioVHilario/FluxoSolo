# FluxoSolo 🚀

**FluxoSolo** é um pipeline de ETL (*Extract, Transform, Load*) e dashboard financeiro desenvolvido para transformar o caos de extratos bancários em inteligência de negócio para trabalhadores autônomos e profissionais liberais.

Diferente de planilhas manuais, o FluxoSolo automatiza a ingestão de dados brutos (PDF/CSV), aplicando regras de normalização e persistência em um banco de dados relacional para análise histórica e visualização de fluxo de caixa.

---

## 🛠️ Engenharia e Arquitetura de Dados

O diferencial técnico deste projeto reside na sua **escalabilidade e aplicação de padrões de projeto**:

* **Abstração de Parsers:** Utilização de **Classes Abstratas (ABC)** para definir o contrato de extração. Isso permite que novos bancos (Sicoob, NuBank, BB) sejam adicionados apenas implementando métodos específicos, mantendo o núcleo da aplicação (Core) intacto.
* **Resiliência de Ingestão:** Lógica avançada para lidar com variações de *encoding* (UTF-8 e Latin-1) e caracteres invisíveis de sistema (BOM), garantindo a leitura correta de extratos de bancos tradicionais e fintechs.
* **Camada de Persistência:** Implementação de um ORM com **SQLAlchemy** para garantir a integridade referencial e facilitar futuras migrações de banco de dados (ex: SQLite para PostgreSQL).
* **Data Cleaning:** Pipeline com Pandas para limpeza de caracteres especiais, conversão de tipos (casting) e padronização de sinais monetários para análise estatística.

## ✨ Funcionalidades Principais

* ✅ **Ingestão Multi-formato:** Suporte a extratos em PDF (via `pdfplumber`) e CSV.
* ✅ **ETL Automático:** Normalização de datas e valores para um formato padrão de banco de dados.
* ✅ **Dashboard Interativo:** Visualização dinâmica de Receitas vs. Despesas e categorização de fluxo com **Plotly**.
* ✅ **Validação de Dados:** Interface que apresenta um *preview* dos dados limpos antes da persistência final no banco.

## 🧰 Stack Tecnológica

* **Linguagem:** Python 3.12+
* **Gestão de Dependências:** Poetry
* **Processamento de Dados:** Pandas, pdfplumber
* **Banco de Dados:** SQLAlchemy, SQLite
* **Interface e Visualização:** Streamlit, Plotly
* **Qualidade de Código:** Pytest, Ruff (Linter/Formatter), Taskipy

## 🏗️ Estrutura do Projeto

```bash
├── fluxosolo/
│   ├── core/         # Configurações de engine, modelos e sessões de banco
│   ├── data/         # Extratos gerados para teste da aplicação
│   ├── models/       # Criação da tabela do banco de dados
│   ├── services/     # Lógica de negócio: Parsers (Abstract Classes) e pipeline ETL
│   ├── views/        # Frontend Streamlit e componentes de visualização
│   └── app.py        # Ponto de entrada da aplicação
├── tests/            # Testes unitários focados na lógica de limpeza de dados
├── migrations/       # Migração de banco de dados via alembic
└── pyproject.toml    # Configuração de ferramentas e dependências
```

## 🚀 Como Executar

Pré-requisitos: Ter o Python e o Poetry instalados.

### Clone o repositório:

```bash
    git clone https://github.com/seu-usuario/fluxosolo.git
    cd fluxosolo
```

### Instale as dependências:
    
```bash
    poetry install
```

### Execute a aplicação:

```bash
    poetry run task run
```

## Próximos passos

[ ] Normalização para 3NF: Reestruturação do esquema SQL para garantir integridade referencial e eficiência.

[ ] Consolidação de Cartão de Crédito: Lógica de merge para evitar dupla contagem entre pagamento de fatura e transações individuais.

[ ] Expansão da Biblioteca de Parsers: Implementação de conectores para Inter, Santander e Itaú.

[ ] Advanced Analytics: Dashboard com filtros dinâmicos por período, banco e centro de custos.
