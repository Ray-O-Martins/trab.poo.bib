from abc import ABC, abstractmethod
import psycopg2


# TRATAMENTO DE EXCEÇÕES

class BibliotecaException(Exception):
    """Classe base para exceções da biblioteca."""
    pass


# CLASSE ABSTRATA

class ItemBiblioteca(ABC):
    def __init__(self, titulo, isbn, disponivel=True):
        self.titulo = titulo
        self.isbn = isbn
        self._disponivel = disponivel

    @abstractmethod
    def descrever(self):
        pass

    def __str__(self):
        status = "Disponível" if self._disponivel else "Emprestado"
        return f"{self.titulo} | ISBN: {self.isbn} | {status}"


# HERANÇA

class Livro(ItemBiblioteca):

    def __init__(self, titulo, isbn, autor, disponivel=True):
        super().__init__(titulo, isbn, disponivel)
        self.autor = autor

    def descrever(self):
        return f"Livro: {self.titulo} - Autor: {self.autor}"


class Revista(ItemBiblioteca):

    def __init__(self, titulo, isbn, edicao, disponivel=True):
        super().__init__(titulo, isbn, disponivel)
        self.edicao = edicao

    def descrever(self):
        return f"Revista: {self.titulo} - Edição {self.edicao}"


# USUÁRIO

class Usuario:

    def __init__(self, nome, id_usuario):
        self.nome = nome
        self.id_usuario = id_usuario

    def __str__(self):
        return f"{self.nome} ({self.id_usuario})"


# EMPRÉSTIMO

class Emprestimo:

    def __init__(self, usuario, item, banco):

        self.usuario = usuario
        self.item = item

        if not item._disponivel:
            raise BibliotecaException(
                f"O item '{item.titulo}' já está emprestado."
            )

        item._disponivel = False

        banco.registrar_emprestimo_no_banco(
            usuario.id_usuario,
            item.isbn
        )

    def __str__(self):
        return f"{self.item.titulo} emprestado para {self.usuario.nome}"


# BANCO DE DADOS

class BancoDeDados:

    def __init__(self):

        self.config = {
            "host": "localhost",
            "database": "postgres",
            "user": "postgres",
            "password": "@@@toyas2",
            "port": 5432
        }

    def conectar(self):
        return psycopg2.connect(**self.config)

    def preparar_banco(self):

        sql = """

        CREATE TABLE IF NOT EXISTS tabela_itens(

            isbn VARCHAR(50) PRIMARY KEY,
            titulo VARCHAR(255),
            tipo VARCHAR(30),
            autor VARCHAR(255),
            edicao INT,
            disponivel BOOLEAN DEFAULT TRUE

        );

        CREATE TABLE IF NOT EXISTS tabela_emprestimos(

            id SERIAL PRIMARY KEY,
            id_usuario VARCHAR(50),
            isbn_item VARCHAR(50)
            REFERENCES tabela_itens(isbn)

        );

        """

        with self.conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

            conn.commit()


    def salvar_item(self, item):

        autor = item.autor if isinstance(item, Livro) else None
        edicao = item.edicao if isinstance(item, Revista) else None

        tipo = "Livro" if isinstance(item, Livro) else "Revista"

        sql = """
        INSERT INTO tabela_itens
        (isbn,titulo,tipo,autor,edicao,disponivel)

        VALUES(%s,%s,%s,%s,%s,%s)

        ON CONFLICT(isbn)
        DO UPDATE SET

        titulo=EXCLUDED.titulo,
        tipo=EXCLUDED.tipo,
        autor=EXCLUDED.autor,
        edicao=EXCLUDED.edicao,
        disponivel=EXCLUDED.disponivel;
        """

        with self.conectar() as conn:
            with conn.cursor() as cur:

                cur.execute(sql,(
                    item.isbn,
                    item.titulo,
                    tipo,
                    autor,
                    edicao,
                    item._disponivel
                ))

            conn.commit()

    # LISTAR ITENS

    def listar_itens(self):

        with self.conectar() as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT isbn, titulo, tipo, autor, edicao, disponivel
                    FROM tabela_itens
                    ORDER BY titulo;
                """)

                return cur.fetchall()

    # BUSCAR ITEM

    def buscar_item(self, isbn):

        with self.conectar() as conn:
            with conn.cursor() as cur:

                cur.execute("""

                    SELECT *
                    FROM tabela_itens
                    WHERE isbn=%s;

                """,(isbn,))

                return cur.fetchone()

    # ATUALIZAR ITEM

    def atualizar_item(self, isbn, novo_titulo):

        with self.conectar() as conn:
            with conn.cursor() as cur:

                cur.execute("""

                    UPDATE tabela_itens
                    SET titulo=%s
                    WHERE isbn=%s;

                """,(novo_titulo,isbn))

            conn.commit()

    # EXCLUIR ITEM

    def excluir_item(self,isbn):

        with self.conectar() as conn:
            with conn.cursor() as cur:

                cur.execute("""

                    DELETE FROM tabela_itens
                    WHERE isbn=%s;

                """,(isbn,))

            conn.commit()

    # REGISTRAR EMPRÉSTIMO

    def registrar_emprestimo_no_banco(self,id_usuario,isbn):

        with self.conectar() as conn:
            with conn.cursor() as cur:

                cur.execute("""

                    INSERT INTO tabela_emprestimos
                    (id_usuario,isbn_item)
                    VALUES(%s,%s);

                """,(id_usuario,isbn))

                cur.execute("""

                    UPDATE tabela_itens
                    SET disponivel=FALSE
                    WHERE isbn=%s;

                """,(isbn,))

            conn.commit()

# MENU

def menu():

    print("\n  BIBLIOTECA:  ")
    print("1 - Cadastrar Livro.")
    print("2 - Cadastrar Revista.")
    print("3 - Listar Itens.")
    print("4 - Buscar Item.")
    print("5 - Atualizar Item.")
    print("6 - Excluir Item.")
    print("7 - Realizar Empréstimo.")
    print("0 - Sair.")

    return input("Escolha uma opção: ")

# PROGRAMA PRINCIPAL

if __name__ == "__main__":

    banco = BancoDeDados()
    banco.preparar_banco()

    while True:

        opcao = menu()

        try:

            if opcao == "1":

                titulo = input("Título: ")
                isbn = input("ISBN: ")
                autor = input("Autor: ")

                livro = Livro(titulo, isbn, autor)

                banco.salvar_item(livro)

                print("\nLivro cadastrado com sucesso!")

            elif opcao == "2":

                titulo = input("Título: ")
                isbn = input("ISBN: ")
                edicao = int(input("Edição: "))

                revista = Revista(titulo, isbn, edicao)

                banco.salvar_item(revista)

                print("\nRevista cadastrada com sucesso!")

            elif opcao == "3":

                itens = banco.listar_itens()

                if not itens:
                    print("\nNenhum item cadastrado.")

                else:

                    print("\n ITENS ")

                    for item in itens:

                        print(
                            f"""
ISBN: {item[0]}
Título: {item[1]}
Tipo: {item[2]}
Autor: {item[3]}
Edição: {item[4]}
Disponível: {item[5]}
-------------------------------------
"""
                        )

            elif opcao == "4":

                isbn = input("Informe o ISBN: ")

                item = banco.buscar_item(isbn)

                if item:

                    print("\nItem encontrado:")

                    print(item)

                else:

                    print("\nItem não encontrado.")

            elif opcao == "5":

                isbn = input("ISBN do item: ")

                novo = input("Novo título: ")

                banco.atualizar_item(isbn, novo)

                print("\nItem atualizado com sucesso!")

            elif opcao == "6":

                isbn = input("ISBN do item: ")

                banco.excluir_item(isbn)

                print("\nItem removido com sucesso!")

            elif opcao == "7":

                nome = input("Nome do usuário: ")

                id_usuario = input("ID do usuário: ")

                isbn = input("ISBN do livro: ")

                dados = banco.buscar_item(isbn)

                if dados is None:

                    print("\nLivro não encontrado.")

                    continue

                if dados[2] == "Livro":

                    item = Livro(
                        dados[1],
                        dados[0],
                        dados[3],
                        dados[5]
                    )

                else:

                    item = Revista(
                        dados[1],
                        dados[0],
                        dados[4],
                        dados[5]
                    )

                usuario = Usuario(nome, id_usuario)

                emprestimo = Emprestimo(
                    usuario,
                    item,
                    banco
                )

                print()

                print(emprestimo)

            elif opcao == "0":

                print("\nSistema encerrado.")

                break

            else:

                print("\nOpção inválida!")

        except BibliotecaException as erro:

            print(f"\nErro: {erro}")

        except Exception as erro:

            print(f"\nErro inesperado: {erro}")
