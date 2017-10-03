import sys
from query import Query
import psycopg2

con = psycopg2.connect(
    host=sys.argv[1], database=sys.argv[4], user=sys.argv[2], password=sys.argv[3])
cur = con.cursor()


def clear():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


def wait():
    print("Pressione [ENTER] para continuar...")
    raw_input()


def queryA():
    clear()
    choice = raw_input("Informe o ID > ")
    clear()
    id = int(int(choice))
    print("Processando, aguarde...")
    cur.execute(Query.SELECT_A % (id, id))
    recset = cur.fetchall()
    print("------------------------------------------------------------\nDate\t\tRating\tVotes\tHelpful\tBy\n------------------------------------------------------------")
    for rec in recset:
        print(str(rec[3])+'\t'+str(rec[4])+'\t'+str(rec[5])+'\t'+str(rec[6])+'\t'+str(rec[8]))


def queryB():
    clear()
    choice = raw_input("Informe o ID > ")
    clear()
    id = int(int(choice))
    print("Processando, aguarde...")
    cur.execute(Query.SELECT_B % (id))
    recset = cur.fetchall()
    #pro_id |pro_asin   |pro_title|pro_salesrank |
    print("------------------------------------------------------------\nID\t\tASIN\t\tTitle\t\t\tSales Rank\n------------------------------------------------------------")
    for rec in recset:
        print(str(rec[0])+'\t'+str(rec[1])+'\t'+str(rec[2])+'\t\t'+str(rec[3]))


def queryC():
    clear()
    choice = raw_input("Informe o ID > ")
    clear()
    id = int(int(choice))
    print("Processando, aguarde...")
    cur.execute(Query.SELECT_C % (id))
    recset = cur.fetchall()
    print("------------------------------------------------------------\nDate\t\tRating Average\n------------------------------------------------------------")
    for rec in recset:
        print(str(rec[0])+'\t'+str(rec[1]))


def queryD():
    print("Perform query D")


def queryE():
    clear()
    print("Processando, aguarde... (pode demorar bastante...)")
    cur.execute(Query.SELECT_E)
    recset = cur.fetchall()
    print("------------------------------------------------------------\nTitle\t\t\t\t\t\t\tRating Average\n------------------------------------------------------------")
    for rec in recset:
        print(str(rec[0])+'\t\t\t'+str(rec[1]))


def queryF():
    clear()
    print("Processando, aguarde... (pode demorar bastante...)")
    cur.execute(Query.SELECT_F)
    recset = cur.fetchall()
    print("------------------------------------------------------------\nID\tTitle\t\t\t\t\t\t\tRating Average\n------------------------------------------------------------")
    for rec in recset:
        print(str(rec[0])+'\t'+str(rec[1])+'\t\t\t'+str(rec[2]))


def queryG():
    print("Perform query G")


def incorrect():
    print("Escolha um item do menu referenciado por uma letra (ex : A)")


queryDestiny = {
    'A': queryA,
    'B': queryB,
    'C': queryC,
    'D': queryD,
    'E': queryE,
    'F': queryF,
    'G': queryG,
}

while 1:
    print("[Amazon product co-purchasing network metadata]")
    print("Escolha a operacao: \n")
    print("(A) listar os 5 comentarios mais uteis e com maior avaliacao e os 5 comentarios mais uteis e com menor avaliacao")
    print("(B) listar os produtos similares com maiores vendas do que ele")
    print("(C) mostrar a evolucao diaria das medias de avaliacao ao longo do intervalo de tempo coberto no arquivo de entrada")
    print("(D) Listar os 10 produtos lideres de venda em cada grupo de produtos")
    print("(E) Listar os 10 produtos com a maior media de avaliacoes uteis positivas por produto")
    print("(F) Listar a 5 categorias de produto com a maior media de avaliacoes uteis positivas por produto")
    print("(G) Listar os 10 clientes que mais fizeram comentarios por grupo de produto")
    print("\n(X) Sair")

    choice = raw_input("> ")
    if(choice == 'X'):
        break

    clear()
    functionQuery = queryDestiny.get(choice, incorrect)
    functionQuery()
    wait()
    clear()
