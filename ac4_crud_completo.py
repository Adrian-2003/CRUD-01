# Avaliação Continuada 4 - 1 ponto
# PROJETO DE VENDAS - parte 2
# Exercicios de CRUD completo (Produtos, Vendedores e Vendas)
# Entrega - dia 24/05/2026


#Ejercicio 9,10,11, --- lo hice con bastante ayuda de la ia ps me resulto muy dificil....tengo q practicar mas



#Libreria

import mysql.connector
from mysql.connector import Error
from datetime import datetime

from time import sleep

#Enlazar con mysql

def conectar():
    """Retorna uma conexao com o banco de dados MySQL."""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="projeto_vendas_eletronicos_unifecaf"
        )
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# PRODUTOS

def criar_produto():
    # Exercicio 1: cadastrar um novo produto na tabela produtos (descricao, preco).
    descricao = input("Descricão do produto: ").strip()
    if not descricao:
        print("A descricão não pode ser vazia.")
        return

    try:
        preco = float(input("Preço do produto: R$ ").replace(",", "."))
        if preco < 0:
            print("O preço não pode ser negativo.")
            return
    except ValueError:
        print("Preço invalido... Informe um numero.")
        return

    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO produtos (descricao, preco) VALUES (%s, %s)",
            (descricao, preco)
        )
        conexao.commit()
        print(f"Produto '{descricao}' cadastrado com sucesso. ID: {cursor.lastrowid}")
    except Error as e:
        print(f"Erro ao cadastrar produto: {e}")
    finally:
        cursor.close()
        conexao.close()


def listar_produtos():
    # Exercicio 2: listar todos os produtos cadastrados com id, descricao e preco.
    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, descricao, preco FROM produtos ORDER BY id")
        produtos = cursor.fetchall()

        if not produtos:
            print("Nenhum produto cadastrado.")
            return

        print(f"\n{'ID':<6} {'Descricao':<35} {'Preco':>10}")
        print("-" * 53)
        for produto in produtos:
            print(f"{produto[0]:<6} {produto[1]:<35} R$ {produto[2]:>7.2f}")
    except Error as e:
        print(f"Erro ao listar produtos: {e}")
    finally:
        cursor.close()
        conexao.close()


def atualizar_produto():
    # Exercicio 3: atualizar descricao e/ou preco de um produto existente por id.
    listar_produtos() #llamo a la definicio de arriba

    try:
        produto_id = int(input("\nID do produto a atualizar: "))
    except ValueError:
        print("ID invalido.")
        return

    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT descricao, preco FROM produtos WHERE id = %s", (produto_id,)
        )
        produto = cursor.fetchone()

        if not produto:
            print("Produto não encontrado.")
            return

        print(f"Produto atual: {produto[0]} | R$ {produto[1]:.2f}")
        print("Deixe em branco para manter o valor atual.")

        nova_descricao = input(f"Nova descrição [{produto[0]}]: ").strip()
        novo_preco_str = input(f"Novo preço [{produto[1]:.2f}]: ").strip().replace(",", ".")

        nova_descricao = nova_descricao if nova_descricao else produto[0]

        if novo_preco_str:
            try:
                novo_preco = float(novo_preco_str)
                if novo_preco < 0:
                    print("O preço não pode ser negativo.")
                    return
            except ValueError:
                print("Preço invalido.")
                return
        else:
            novo_preco = produto[1]

        cursor.execute(
            "UPDATE produtos SET descricao = %s, preco = %s WHERE id = %s",
            (nova_descricao, novo_preco, produto_id)
        )
        conexao.commit()
        print("Produto atualizado com sucesso.")
    except Error as e:
        print(f"Erro ao atualizar produto: {e}")
    finally:
        cursor.close()
        conexao.close()


def excluir_produto():
    # Exercicio 4: excluir um produto por id, tratando dependencias em vendas_produtos.
    listar_produtos()

    try:
        produto_id = int(input("\nID do produto a excluir: "))
    except ValueError:
        print("ID invalido.")
        return

    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT descricao FROM produtos WHERE id = %s", (produto_id,))
        produto = cursor.fetchone()

        if not produto:
            print("Produto não encontrado.")
            return

        cursor.execute(
            "SELECT COUNT(*) FROM vendas_produtos WHERE id_produto = %s", (produto_id,)
        )
        total_vinculos = cursor.fetchone()[0]

        if total_vinculos > 0:
            confirmacao = input(
                f"O produto '{produto[0]}' esta vinculado a {total_vinculos} venda(s). "
                "Excluir igualmente? (s/n): "
            ).strip().lower()
            if confirmacao != "s":
                print("Exclusão cancelada.")
                return
            cursor.execute(
                "DELETE FROM vendas_produtos WHERE id_produto = %s", (produto_id,)
            )

        cursor.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
        conexao.commit()
        print(f"Produto '{produto[0]}' excluido com sucesso.")
    except Error as e:
        print(f"Erro ao excluir produto: {e}")
    finally:
        cursor.close()
        conexao.close()


# VENDEDORES

def criar_vendedor():
    # Exercicio 5: cadastrar um novo vendedor na tabela vendedores.
    nome = input("Nome do vendedor: ").strip()
    if not nome:
        print("O nome não pode ser vazio.")
        return

    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO vendedores (nome) VALUES (%s)", (nome,))
        conexao.commit()
        print(f"Vendedor '{nome}' cadastrado com sucesso. ID: {cursor.lastrowid}")
    except Error as e:
        print(f"Erro ao cadastrar vendedor: {e}")
    finally:
        cursor.close()
        conexao.close()


def listar_vendedores():
    # Exercicio 6: listar todos os vendedores cadastrados.
    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome FROM vendedores ORDER BY id")
        vendedores = cursor.fetchall()

        if not vendedores:
            print("Nenhum vendedor cadastrado.")
            return

        print(f"\n{'ID':<6} {'Nome':<30}")
        print("-" * 36)
        for vendedor in vendedores:
            print(f"{vendedor[0]:<6} {vendedor[1]:<30}")
    except Error as e:
        print(f"Erro ao listar vendedores: {e}")
    finally:
        cursor.close()
        conexao.close()


def atualizar_vendedor():
    # Exercicio 7: atualizar o nome de um vendedor existente por id.
    listar_vendedores()

    try:
        vendedor_id = int(input("\nID do vendedor a atualizar: "))
    except ValueError:
        print("ID invalido.")
        return

    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM vendedores WHERE id = %s", (vendedor_id,))
        vendedor = cursor.fetchone()

        if not vendedor:
            print("Vendedor não encontrado.")
            return

        novo_nome = input(f"Novo nome [{vendedor[0]}]: ").strip()
        if not novo_nome:
            print("Nenhuma alteração realizada.")
            return

        cursor.execute(
            "UPDATE vendedores SET nome = %s WHERE id = %s",
            (novo_nome, vendedor_id)
        )
        conexao.commit()
        print("Vendedor atualizado com sucesso.")
    except Error as e:
        print(f"Erro ao atualizar vendedor: {e}")
    finally:
        cursor.close()
        conexao.close()


def excluir_vendedor():
    # Exercicio 8: excluir vendedor por id, validando se possui vendas vinculadas.
    listar_vendedores()

    try:
        vendedor_id = int(input("\nID do vendedor a excluir: "))
    except ValueError:
        print("ID invalido.")
        return

    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM vendedores WHERE id = %s", (vendedor_id,))
        vendedor = cursor.fetchone()

        if not vendedor:
            print("Vendedor não encontrado.")
            return

        cursor.execute(
            "SELECT COUNT(*) FROM vendas WHERE id_vendedor = %s", (vendedor_id,)
        )
        total_vendas = cursor.fetchone()[0]

        if total_vendas > 0:
            print(
                f"Não e possivel excluir '{vendedor[0]}' pois possui "
                f"{total_vendas} venda(s) vinculada(s). "
                "Exclua as vendas antes de remover o vendedor."
            )
            return

        cursor.execute("DELETE FROM vendedores WHERE id = %s", (vendedor_id,))
        conexao.commit()
        print(f"Vendedor '{vendedor[0]}' excluido com sucesso.")
    except Error as e:
        print(f"Erro ao excluir vendedor: {e}")
    finally:
        cursor.close()
        conexao.close()


# VENDAS

def criar_venda_com_itens():
    # Exercicio 9: criar uma venda e inserir itens na tabela vendas_produtos com quantidade e valores.
    listar_vendedores()

    try:
        vendedor_id = int(input("\nID do vendedor responsavel: "))
    except ValueError:
        print("ID invalido.")
        return

    try:
        desconto = float(input("Desconto (R$) [0 para nenhum]: ").replace(",", "."))
        if desconto < 0:
            print("Desconto não pode ser negativo.")
            return
    except ValueError:
        print("Valor invalido.")
        return

    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM vendedores WHERE id = %s", (vendedor_id,))
        if not cursor.fetchone():
            print("Vendedor não encontrado.")
            return

        data_e_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO vendas (id_vendedor, data_e_hora, desconto, valor_final) "
            "VALUES (%s, %s, %s, %s)",
            (vendedor_id, data_e_hora, desconto, 0)
        )
        conexao.commit()
        venda_id = cursor.lastrowid
        print(f"Venda criada com ID {venda_id}. Agora adicione os itens.")

        valor_total_itens = 0.0

        while True:
            print("\n--- Adicionar item (deixe o ID em branco para finalizar) ---")
            listar_produtos()

            produto_id_str = input("\nID do produto: ").strip()
            if not produto_id_str:
                break

            try:
                produto_id = int(produto_id_str)
            except ValueError:
                print("ID invalido.")
                continue

            cursor.execute(
                "SELECT descricao, preco FROM produtos WHERE id = %s", (produto_id,)
            )
            produto = cursor.fetchone()
            if not produto:
                print("Produto não encontrado.")
                continue

            # Verifico si el producto ya fue incluido en esta venta

            cursor.execute(
                "SELECT id_produto FROM vendas_produtos "
                "WHERE id_venda = %s AND id_produto = %s",
                (venda_id, produto_id)
            )
            if cursor.fetchone():
                print("Este produto ja foi adicionado nesta venda.")
                continue

            try:
                quantidade = int(input(f"Quantidade de '{produto[0]}': "))
                if quantidade <= 0:
                    print("A quantidade deve ser maior que zero.")
                    continue
            except ValueError:
                print("Quantidade invalida.")
                continue

            #creo nuevas variables para esta def en especifico

            valor_unitario = float(produto[1])
            valor_item = valor_unitario * quantidade
            valor_total_itens += valor_item

            cursor.execute(
                "INSERT INTO vendas_produtos "
                "(id_venda, id_produto, quantidade, valor_unitario, valor_total) "
                "VALUES (%s, %s, %s, %s, %s)",
                (venda_id, produto_id, quantidade, valor_unitario, valor_item)
            )
            conexao.commit()
            print(
                f"Item adicionado: {produto[0]} x{quantidade} "
                f"= R$ {valor_item:.2f}"
            )

        valor_final = max(valor_total_itens - desconto, 0)
        cursor.execute(
            "UPDATE vendas SET valor_final = %s WHERE id = %s",
            (valor_final, venda_id)
        )
        conexao.commit()
        print(
            f"\nVenda finalizada."
            f"\n  Total dos itens : R$ {valor_total_itens:.2f}"
            f"\n  Desconto        : R$ {desconto:.2f}"
            f"\n  Valor final     : R$ {valor_final:.2f}"
        )
    except Error as e:
        print(f"Erro ao criar venda: {e}")
    finally:
        cursor.close()
        conexao.close()


def listar_vendas_completas():
    # Exercicio 10: listar vendas com vendedor e itens (produto, quantidade, valor_unitario, valor_total).
    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT v.id, vd.nome, v.data_e_hora, v.desconto, v.valor_final
            FROM vendas v
            JOIN vendedores vd ON vd.id = v.id_vendedor
            ORDER BY v.id
            """
        )
        vendas = cursor.fetchall()

        if not vendas:
            print("Nenhuma venda cadastrada.")
            return

        for venda in vendas:
            venda_id, vendedor_nome, data_e_hora, desconto, valor_final = venda
            print(
                f"\nVenda ID: {venda_id} | Vendedor: {vendedor_nome} | "
                f"Data: {data_e_hora} | "
                f"Desconto: R$ {desconto:.2f} | Valor Final: R$ {valor_final:.2f}"
            )
            print(f"  {'Produto':<30} {'Quantidade':>5} {'Unit (R$)':>10} {'Total (R$)':>11}")
            print("  " + "-" * 58)

            cursor.execute(
                """
                SELECT p.descricao, vp.quantidade, vp.valor_unitario, vp.valor_total
                FROM vendas_produtos vp
                JOIN produtos p ON p.id = vp.id_produto
                WHERE vp.id_venda = %s
                """,
                (venda_id,)
            )
            itens = cursor.fetchall()

            if not itens:
                print("  Sem itens registrados.")
            else:
                for item in itens:
                    print(
                        f"  {item[0]:<30} {item[1]:>5} "
                        f"{item[2]:>10.2f} {item[3]:>11.2f}"
                    )
    except Error as e:
        print(f"Erro ao listar vendas: {e}")
    finally:
        cursor.close()
        conexao.close()


def atualizar_venda_e_itens():
    # Exercicio 11: atualizar dados da venda (desconto/valor_final) e seus itens.
    listar_vendas_completas()   #vuelvo a llamar a la def q nesesito

    try:
        venda_id = int(input("\nID da venda a atualizar: "))
    except ValueError:
        print("ID invalido.")
        return

    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT desconto, valor_final FROM vendas WHERE id = %s", (venda_id,)
        )
        venda = cursor.fetchone()

        if not venda:
            print("Venda não encontrada.")
            return

        print(
            f"Desconto atual: R$ {venda[0]:.2f} | "
            f"Valor final atual: R$ {venda[1]:.2f}"
        )
        print("Deixe em branco para manter o valor atual.")

        novo_desconto_str = (
            input(f"Novo desconto [{venda[0]:.2f}]: ").strip().replace(",", ".")
        )
        if novo_desconto_str:
            try:
                novo_desconto = float(novo_desconto_str)
                if novo_desconto < 0:
                    print("Desconto não pode ser negativo.")
                    return
            except ValueError:
                print("Valor invalido.")
                return
        else:
            novo_desconto = float(venda[0])

        # Editar las cantidades de los itens existentes
        cursor.execute(
            """
            SELECT vp.id_produto, p.descricao, vp.quantidade, vp.valor_unitario
            FROM vendas_produtos vp
            JOIN produtos p ON p.id = vp.id_produto
            WHERE vp.id_venda = %s
            """,
            (venda_id,)
        )
        itens = cursor.fetchall()

        nova_soma = 0.0
        if itens:
            print("\nItens atuais (deixe em branco para manter a quantidade):")
            for item in itens:
                id_produto, descricao, qtd_atual, unit = item
                nova_qtd_str = input(
                    f"  '{descricao}' | Quantidade atual: {qtd_atual} | Nova Quantidade: "
                ).strip()

                if nova_qtd_str:
                    try:
                        nova_qtd = int(nova_qtd_str)
                        if nova_qtd <= 0:
                            print("  Quantidade invalida, mantendo valor atual.")
                            nova_qtd = qtd_atual
                    except ValueError:
                        print("  Quantidade invalida, mantendo valor atual.")
                        nova_qtd = qtd_atual
                else:
                    nova_qtd = qtd_atual

                novo_total_item = nova_qtd * float(unit)
                cursor.execute(
                    "UPDATE vendas_produtos SET quantidade = %s, valor_total = %s "
                    "WHERE id_venda = %s AND id_produto = %s",
                    (nova_qtd, novo_total_item, venda_id, id_produto)
                )
                nova_soma += novo_total_item
        else:
            cursor.execute(
                "SELECT COALESCE(SUM(valor_total), 0) "
                "FROM vendas_produtos WHERE id_venda = %s",
                (venda_id,)
            )
            nova_soma = float(cursor.fetchone()[0])

        novo_valor_final = max(nova_soma - novo_desconto, 0)
        cursor.execute(
            "UPDATE vendas SET desconto = %s, valor_final = %s WHERE id = %s",
            (novo_desconto, novo_valor_final, venda_id)
        )
        conexao.commit()
        print(
            f"Venda atualizada."
            f"\n  Total itens : R$ {nova_soma:.2f}"
            f"\n  Desconto    : R$ {novo_desconto:.2f}"
            f"\n  Valor final : R$ {novo_valor_final:.2f}"
        )
    except Error as e:
        print(f"Erro ao atualizar venda: {e}")
    finally:
        cursor.close()
        conexao.close()


def excluir_venda():
    # Exercicio 12: excluir uma venda por id removendo primeiro os itens de vendas_produtos.
    listar_vendas_completas()   #vuelvo a llamar a mi def

    try:
        venda_id = int(input("\nID da venda a excluir: "))
    except ValueError:
        print("ID invalido.")
        return

    conexao = conectar()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM vendas WHERE id = %s", (venda_id,))
        if not cursor.fetchone():
            print("Venda nao encontrada.")
            return

        confirmacao = input(f"Confirma a exclusão da venda {venda_id} e todos os seus itens? (s/n): ").strip().lower()
        if confirmacao != "s":
            print("Exclusao cancelada.")
            return

        cursor.execute(
            "DELETE FROM vendas_produtos WHERE id_venda = %s", (venda_id,)
        )
        cursor.execute("DELETE FROM vendas WHERE id = %s", (venda_id,))
        conexao.commit()
        print(f"Venda {venda_id} e seus itens excluidos com sucesso.")
    except Error as e:
        print(f"Erro ao excluir venda: {e}")
    finally:
        cursor.close()
        conexao.close()


def menu():
    opcoes = {
        "1": ("Criar produto", criar_produto),
        "2": ("Listar produtos", listar_produtos),
        "3": ("Atualizar produto", atualizar_produto),
        "4": ("Excluir produto", excluir_produto),
        "5": ("Criar vendedor", criar_vendedor),
        "6": ("Listar vendedores", listar_vendedores),
        "7": ("Atualizar vendedor", atualizar_vendedor),
        "8": ("Excluir vendedor", excluir_vendedor),
        "9": ("Criar venda com itens", criar_venda_com_itens),
        "10": ("Listar vendas completas", listar_vendas_completas),
        "11": ("Atualizar venda e itens", atualizar_venda_e_itens),
        "12": ("Excluir venda", excluir_venda),
    }

    while True:
        print("\n=== MENU AC4 - CRUD COMPLETO ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Voltar")

        print("13 - Fechar o Programa")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Voltando ao menu principal.")
            break

        if escolha == "13":
            print("“Obrigado pela visita, volte sempre!”----FECHANDO O PROGRAMA.....")
            sleep(3.5)
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nSelecionado: {descricao}")
            funcao()
            print("Exercicio em estrutura base (return vazio).")
        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    menu()            
