# Avaliação Continuada 3 - 1 ponto
# PROJETO DE VENDAS - parte 1
# Exercicios de estatisticas de vendas.
# Entrega - dia 17/05/2026

#Libreria para conectarse con mysql

import mysql.connector
from mysql.connector import Error

from time import sleep

#Conexion 

def conectar():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='projeto_vendas_eletronicos_unifecaf'
        )
        if conexao.is_connected():
            print("Conectado ao MySQL com sucesso!")
            return conexao
    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None


def fechar_conexao(conexao):
    if conexao and conexao.is_connected():
        conexao.close()
        print("Conexão encerrada.")

def total_vendas_periodo():
    # Exercicio 1: calcular o valor total vendido em um periodo usando vendas.valor_final.
    dt_inicio = input("Data inicio (Ano-mes-dia): ").strip()
    dt_fim = input("Data fim (Ano-mes-dia): ").strip()
    conexao = conectar()
    if not conexao:
        return
    try:
        cursor = conexao.cursor()
        sql = """
            SELECT SUM(valor_final)
            FROM vendas
            WHERE DATE(data_e_hora) BETWEEN %s AND %s
        """
        cursor.execute(sql, (dt_inicio, dt_fim))
        resultado = cursor.fetchone()[0] or 0.0
        print(f"---Valor total vendido entre {dt_inicio} e {dt_fim}: R$ {resultado:,.2f}")
    except Error as e_de_error:
        print(f"Error: {e_de_error}")
    finally:
        cursor.close()
        fechar_conexao(conexao)


def qtd_vendas_por_vendedor():
    # Exercicio 2: contar quantas vendas cada vendedor realizou usando vendas.id_vendedor.
    conexao = conectar()
    if not conexao:
        return
    try:
        cursor = conexao.cursor()
        sql = """
            SELECT ve.nome, COUNT(v.id) AS total_vendas
            FROM vendas v
            JOIN vendedores ve ON v.id_vendedor = ve.id
            GROUP BY ve.id, ve.nome
            ORDER BY total_vendas DESC
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        print(f"---{'vendedor':<25} {'Qtd Vendas':>10}")
        print(" " + "-" * 37)
        for nome, qtd in resultados:
            print(f"{nome:<25} {qtd:>10}")
    except Error as e_de_error:
        print(f"---Error: {e_de_error}")
    finally:
        cursor.close()
        fechar_conexao(conexao)


def ticket_medio_geral():
    # Exercicio 3: calcular o ticket medio geral a partir de vendas.valor_final.
    conexao = conectar()
    if not conexao:
        return
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT AVG(valor_final) FROM vendas")
        resultado = cursor.fetchone()[0] or 0.0
        print(f"---Ticket medio geral: R$ {resultado:,.2f}")
    except Error as e_de_error:
        print(f"Error: {e_de_error}")
    finally:
        cursor.close()
        fechar_conexao(conexao)


def ticket_medio_por_vendedor():
    # Exercicio 4: calcular o ticket medio de cada vendedor cruzando vendas e vendedores.
    conexao = conectar()
    if not conexao:
        return
    try:
        cursor = conexao.cursor()
        sql = """
            SELECT ve.nome, AVG(v.valor_final) AS ticket_medio
            FROM vendas v
            JOIN vendedores ve ON v.id_vendedor = ve.id
            GROUP BY ve.id, ve.nome
            ORDER BY ticket_medio DESC
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()

        print(f"{'Vendedor':<25} {'Ticket Medio':>14}")
        print("  " + "-" * 41)
        for nome, ticket in resultados:
            print(f"{nome:<25} R$ {ticket:>10,.2f}")
    except Error as e_de_error:
        print(f"Erro: {e_de_error}")
    finally:
        cursor.close()
        fechar_conexao(conexao)


def produto_mais_vendido_qtd():
    # Exercicio 5: identificar o produto mais vendido por quantidade em vendas_produtos.
    conexao = conectar()
    if not conexao:
        return
    try:
        cursor = conexao.cursor()
        sql = """
            SELECT p.descricao, SUM(vp.quantidade) AS total_qtd
            FROM vendas_produtos vp
            JOIN produtos p ON vp.id_produto = p.id
            GROUP BY p.id, p.descricao
            ORDER BY total_qtd DESC
            LIMIT 1
        """
        cursor.execute(sql)
        resultado = cursor.fetchone()

        if resultado:
            print(f"Produto mais vendido (quantidade): {resultado[0]}")
            print(f"Quantidade total: {resultado[1]} unidades")
        else:
            print("Nenhum dado encontrado.")
    except Error as e_de_error:
        print(f"Erro: {e_de_error}")
    finally:
        cursor.close()
        fechar_conexao(conexao)


def produto_mais_rentavel_valor():
    # Exercicio 6: identificar o produto que gerou maior faturamento somando vendas_produtos.valor_total.
    conexao = conectar()
    if not conexao:
        return
    try:
        cursor = conexao.cursor()
        sql = """
            SELECT p.descricao, SUM(vp.valor_total) AS faturamento
            FROM vendas_produtos vp
            JOIN produtos p ON vp.id_produto = p.id
            GROUP BY p.id, p.descricao
            ORDER BY faturamento DESC
            LIMIT 1
        """
        cursor.execute(sql)
        resultado = cursor.fetchone()

        if resultado:
            print(f"Produto mais rentavel: {resultado[0]}")
            print(f"Faturamento total: R$ {resultado[1]:,.2f}")
        else:
            print("Nenhum dado encontrado.")
    except Error as e_de_error:
        print(f"Erro: {e_de_error}")
    finally:
        cursor.close()
        fechar_conexao(conexao)


def total_descontos_aplicados():
    # Exercicio 7: somar todos os descontos concedidos usando vendas.desconto.
    conexao = conectar()
    if not conexao:
        return
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT SUM(desconto) FROM vendas")
        resultado = cursor.fetchone()[0] or 0.0
        print(f"Total de descontos aplicados: R$ {resultado:,.2f}")
    except Error as e_de_error:
        print(f"Erro: {e_de_error}")
    finally:
        cursor.close()
        fechar_conexao(conexao)


def percentual_desconto_medio():
    # Exercicio 8: calcular o percentual medio de desconto comparando desconto e valor_final das vendas.
    conexao = conectar()
    if not conexao:
        return
    try:
        cursor = conexao.cursor()
        sql = """
            SELECT AVG(
            CASE
            WHEN (valor_final + desconto) > 0
            THEN (desconto / (valor_final + desconto)) * 100
            ELSE 0
            END
            ) AS perc_medio
            FROM vendas
        """
        cursor.execute(sql)
        resultado = cursor.fetchone()[0] or 0.0
        print(f"Percentual medio de desconto: {resultado:.2f}%")
    except Error as e_de_error:
        print(f"Erro: {e_de_error}")
    finally:
        cursor.close()
        fechar_conexao(conexao)


def faturamento_por_dia():
    # Exercicio 9: agrupar o faturamento por dia com base em vendas.data_e_hora e vendas.valor_final.
    conexao = conectar()
    if not conexao:
        return
    try:
        cursor = conexao.cursor()
        sql = """
            SELECT DATE(data_e_hora) AS dia, SUM(valor_final) AS faturamento
            FROM vendas
            GROUP BY dia
            ORDER BY dia
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()

        print(f"{'Data':<14} {'Faturamento':>14}")
        print("  " + "-" * 30)
        for dia, faturamento in resultados:
            print(f"{str(dia):<14} R$ {faturamento:>10,.2f}")
    except Error as e_de_error:
        print(f"Erro: {e_de_error}")
    finally:
        cursor.close()
        fechar_conexao(conexao)


def top_3_vendedores_faturamento():
    # Exercicio 10: listar os 3 vendedores com maior faturamento total no periodo.
    conexao = conectar()
    if not conexao:
        return
    try:
        cursor = conexao.cursor()
        sql = """
            SELECT ve.nome, SUM(v.valor_final) AS faturamento_total
            FROM vendas v
            JOIN vendedores ve ON v.id_vendedor = ve.id
            GROUP BY ve.id, ve.nome
            ORDER BY faturamento_total DESC
            LIMIT 3
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()

        print(f"{'#':<4} {'Vendedor':<25} {'Faturamento':>14}")
        print("  " + "-" * 45)
        posicoes = ["1o", "2o", "3o"]
        for i, (nome, fat) in enumerate(resultados):
            print(f"  {posicoes[i]:<4} {nome:<25} R$ {fat:>10,.2f}")
    except Error as e_de_error:
        print(f"Erro: {e_de_error}")
    finally:
        cursor.close()
        fechar_conexao(conexao)


def menu_relatorios():
    opcoes = {
        "1": ("Total de vendas por periodo", total_vendas_periodo),
        "2": ("Quantidade de vendas por vendedor", qtd_vendas_por_vendedor),
        "3": ("Ticket medio geral", ticket_medio_geral),
        "4": ("Ticket medio por vendedor", ticket_medio_por_vendedor),
        "5": ("Produto mais vendido por quantidade", produto_mais_vendido_qtd),
        "6": ("Produto mais rentavel por faturamento", produto_mais_rentavel_valor),
        "7": ("Total de descontos aplicados", total_descontos_aplicados),
        "8": ("Percentual medio de desconto", percentual_desconto_medio),
        "9": ("Faturamento por dia", faturamento_por_dia),
        "10": ("Top 3 vendedores por faturamento", top_3_vendedores_faturamento),
    }

    while True:
        print("\n=== MENU AC3 - RELATORIOS ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Voltar")

        print("11 - Fechar o Programa")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Voltando ao menu principal.")
            break

        if escolha == "11":
            print("“Obrigado pela visita, volte sempre!”----FECHANDO O PROGRAMA.....")
            sleep(2)
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nGerando relatorio: {descricao}")
            resultado = funcao()

            if resultado is None:
                print("Relatorio em estrutura base (return vazio).")
            else:
                print(resultado)
        else:
            print("Opcao invalida. Tente novamente.")

#Esto me evita q el archivo se ejecute solo.....

if __name__ == "__main__":
    menu_relatorios()           
