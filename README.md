# 📚 Sistema de Gerenciamento de Biblioteca

## Integrantes

- Nome do Integrante 1
- Nome do Integrante 2
- Nome do Integrante 3

---

## Descrição do Sistema

O Sistema de Gerenciamento de Biblioteca foi desenvolvido em Python utilizando Programação Orientada a Objetos (POO) e PostgreSQL.

O sistema permite o cadastro e gerenciamento de livros e revistas, controle de empréstimos, armazenamento das informações em banco de dados relacional e aplicação de regras de negócio para garantir a integridade dos dados.

---

## Tecnologias Utilizadas

- Python 3
- PostgreSQL
- Biblioteca psycopg2

---

## Conceitos de Programação Orientada a Objetos

O sistema aplica os seguintes conceitos de POO:

- Classes e Objetos
- Encapsulamento
- Herança
- Polimorfismo
- Classe Abstrata
- Tratamento de Exceções

---

## Funcionalidades

- Cadastro de livros
- Cadastro de revistas
- Cadastro de usuários
- Listagem de itens cadastrados
- Busca de itens por ISBN
- Atualização de informações dos itens
- Exclusão de itens
- Registro de empréstimos
- Controle de disponibilidade dos itens

---

## Estrutura do Projeto

```text
biblioteca/
│
├── bib.py
├── README.md
└── requirements.txt
```

---

## Banco de Dados

O sistema utiliza PostgreSQL para armazenar as informações.

### Tabelas

- tabela_itens
- tabela_emprestimos

---


## Regras de Negócio

| Código | Regra de Negócio | Implementação |
|:------:|------------------|---------------|
| *RN01* | Não permitir que um item já emprestado seja emprestado novamente. | O sistema verifica o atributo _disponivel. Caso o item esteja indisponível, uma BibliotecaException é lançada. |
| *RN02* | Após a realização de um empréstimo, o item torna-se indisponível. | O atributo _disponivel é alterado para False, indicando que o item está emprestado. |
| *RN03* | Todo empréstimo deve ser registrado no banco de dados. | O método registrar_emprestimo_no_banco() registra o empréstimo e atualiza o status do item no PostgreSQL. |
| *RN04* | Cada item da biblioteca deve possuir um ISBN único. | O banco utiliza o ISBN como chave primária. Caso o ISBN já exista, a cláusula ON CONFLICT (isbn) evita a duplicação do registro. |
| *RN05* | As tabelas do banco de dados devem existir antes da utilização do sistema. | O método preparar_banco() cria automaticamente as tabelas utilizando CREATE TABLE IF NOT EXISTS. |
| *RN06* | Apenas itens da biblioteca podem ser emprestados. | O empréstimo recebe objetos derivados da classe abstrata ItemBiblioteca, como Livro e Revista. |
| *RN07* | Apenas itens disponíveis podem ter seu status alterado para emprestado. | A disponibilidade do item é alterada somente após a validação do empréstimo, garantindo a consistência das informações. |
---

## Como Executar

### Pré-requisitos

- Python 3 instalado.
- PostgreSQL instalado.
- Biblioteca `psycopg2` instalada.

### Instalação

Instale a dependência:

```bash
pip install psycopg2
```

### Configuração

No arquivo `bib.py`, configure os dados de conexão com o PostgreSQL:

- Host
- Database
- User
- Password
- Port

### Execução

Execute o comando abaixo no terminal:

```bash
python bib.py
```

Ao iniciar o sistema, as tabelas serão criadas automaticamente caso ainda não existam no banco de dados.

---

## Observações

Este projeto foi desenvolvido para a disciplina de Engenharia de Software, utilizando Programação Orientada a Objetos e PostgreSQL, conforme os requisitos propostos pelo professor.
