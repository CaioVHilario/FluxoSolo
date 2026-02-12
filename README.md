# FluxoSolo 🚀

FluxoSolo é uma aplicação de inteligência financeira desenvolvida especificamente para trabalhadores autônomos e profissionais liberais. O projeto automatiza a gestão de gastos e receitas a partir da extração direta de extratos bancários em PDF, transformando dados brutos em insights visuais acionáveis.

Este projeto faz parte do meu portfólio de transição de carreira para o Desenvolvimento Backend, aplicando conceitos de processamento de dados, modelagem de banco de dados e automação de tarefas.

## ✨ Funcionalidades

- Extração Inteligente: Leitura de extratos bancários (PDF) utilizando pdfplumber com normalização de dados.

- Data Cleaning: Pipeline de limpeza e padronização de valores monetários e datas com Pandas.

- Persistência Robusta: Gerenciamento de usuários e transações via SQLAlchemy e banco de dados relacional.

- Dashboard Interativo: Visualização de fluxo de caixa e categorização de gastos através do Streamlit.

- Qualidade de Código: Ambiente rigorosamente configurado com ferramentas de linting e testes automatizados.

## 🛠️ Stack Tecnológica

- Linguagem: Python 3.12+

- Gestão de Dependências: Poetry

- Processamento de Dados: Pandas, pdfplumber

- ORM: SQLAlchemy

- Interface: Streamlit

- QA/Tooling: Pytest, Ruff (Linter/Formatter), Taskipy (Task Runner)

## 🏗️ Estrutura do Projeto

```bash
├── app/
│   ├── core/         # Configurações de banco de dados e modelos
│   ├── services/     # Lógica de extração (Parser) e limpeza (Pandas)
│   └── main.py       # Interface Streamlit
├── data/             # Armazenamento local de arquivos (ignorado no git)
├── tests/            # Testes unitários e de integração
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

## 🧪 Testes e Qualidade

Para garantir a confiabilidade do processamento financeiro, o projeto utiliza:

```task lint```: Executa o Ruff para análise estática.

```task test```: Executa o conjunto de testes com Pytest.