import sys
import requests.graphql_client as graphql_client
import requests.rest_client as rest_client
import requests.grpc_client as grpc_client
import requests.soap_client as soap_client


def menu_graphql():
    print("\n--- GraphQL ---")
    print("1. Listar livros\n2. Obter livro\n3. Adicionar livro\n4. Atualizar livro\n5. Eliminar livro\n6. Voltar")
    while True:
        op = input("Escolha uma opção: ")
        if op == '1': graphql_client.gql_listar()
        elif op == '2': graphql_client.gql_obter(int(input("ID: ")))
        elif op == '3':
            id = int(input("ID: "))
            t = input("Título: ")
            d = input("Descrição: ")
            e = input("Estado: ")
            graphql_client.gql_adicionar(id, t, d, e)
        elif op == '4':
            id = int(input("ID: "))
            t = input("Novo título (ou deixe vazio): ") or None
            d = input("Nova descrição (ou deixe vazio): ") or None
            e = input("Novo estado (ou deixe vazio): ") or None
            graphql_client.gql_atualizar(id, t, d, e)
        elif op == '5': graphql_client.gql_eliminar(int(input("ID: ")))
        elif op == '6': break
        else: print("Opção inválida!")

def menu_rest():
    print("\n--- REST ---")
    print("1. Listar livros\n2. Obter livro\n3. Adicionar livro\n4. Atualizar livro\n5. Eliminar livro\n6. Voltar")
    while True:
        op = input("Escolha uma opção: ")
        if op == '1': rest_client.get_all_books()
        elif op == '2': rest_client.get_book_by_id(int(input("ID: ")))
        elif op == '3': rest_client.create_book()
        elif op == '4': rest_client.update_book(int(input("ID: ")))
        elif op == '5': rest_client.delete_book(int(input("ID: ")))
        elif op == '6': break
        else: print("Opção inválida!")

def menu_soap():
    print("\n--- SOAP ---")
    print("1. Listar livros\n2. Obter livro\n3. Adicionar livro\n4. Eliminar livro\n5. Voltar")
    while True:
        op = input("Escolha uma opção: ")
        if op == '1': soap_client.listar_livros()
        elif op == '2': soap_client.obter_livro(int(input("ID: ")))
        elif op == '3':
            id = int(input("ID: "))
            t = input("Título: ")
            d = input("Descrição: ")
            e = input("Estado: ")
            soap_client.adicionar_livro(id, t, d, e)
        elif op == '4': soap_client.eliminar_livro(int(input("ID: ")))
        elif op == '5': break
        else: print("Opção inválida!")

def main():
    while True:
        print("\n=== Menu Principal ===")
        print("1. GraphQL\n2. REST\n3. gRPC\n4. SOAP\n5. Sair")
        op = input("Escolha o serviço: ")
        if op == '1': menu_graphql()
        elif op == '2': menu_rest()
        elif op == '3': grpc_client.main()  # Chama o menu do gRPC
        elif op == '4': menu_soap()
        elif op == '5': print("A sair..."); sys.exit(0)
        else: print("Opção inválida!")

if __name__ == "__main__":
    main()
