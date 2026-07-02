# 📚 Sistema de Gerenciamento de Biblioteca

## Integrantes

- Guilherme
- Jo
- Rayssa Oliveira Martins das Chagas

---

## Descrição do Sistema

O Sistema de Gerenciamento de Biblioteca foi desenvolvido utilizando a linguagem Python e o banco de dados PostgreSQL, aplicando os principais conceitos de Programação Orientada a Objetos estudados na disciplina. O sistema permite o gerenciamento de livros e revistas, realizando o cadastro dos itens, o controle de empréstimos e o armazenamento das informações em um banco de dados relacional. Além disso, foram implementadas regras de negócio que garantem a integridade dos dados, impedindo, por exemplo, que um item indisponível seja emprestado novamente.

---

## Tecnologias Utilizadas

O projeto foi desenvolvido utilizando a linguagem Python como principal tecnologia para implementação da lógica do sistema. Para a persistência dos dados foi utilizado o PostgreSQL, sendo a conexão realizada por meio da biblioteca 'psycopg2', responsável pela comunicação entre a aplicação e o banco de dados.

---

## Conceitos de Programação Orientada a Objetos

O sistema aplica os seguintes conceitos de POO:

Durante o desenvolvimento do sistema foram aplicados diversos conceitos da Programação Orientada a Objetos. A classe abstrata 'ItemBiblioteca' foi utilizada para definir características comuns entre os itens da biblioteca. As classes Livro e Revista implementam herança ao estender essa classe abstrata, além de demonstrarem polimorfismo por meio da implementação do método 'descrever()'. O encapsulamento foi empregado utilizando o atributo '_disponivel', responsável por controlar a disponibilidade dos itens. Também foi criado um tratamento de exceções personalizado através da classe 'BibliotecaException', garantindo maior segurança durante a execução das operações.

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
