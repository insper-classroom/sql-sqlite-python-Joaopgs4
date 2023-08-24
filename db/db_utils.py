import sqlite3
#Fiz os códigos maximizando versatilidade, para poderem ser usados em diferentes arquivos, em diferentes DB, com diferentes tabelas
#em cada DB

#Printa uma tabela completa da DB baseada no nome fornecido
def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    print(cursor.fetchall())


#Cria uma tabela (caso não haja uma de nome igual existente) e configura seus campos de acordo com os campos passados no dicionario
#O dicionario deve estar no formato: {'Campo1': 'Tipo de Dado', 'Campo2': 'Tipo de Dado', etc...}
def create_table(cursor, table_name, fields_dictionary):
    dict_last_item = list(fields_dictionary)[-1]
    table_text = ''

    for field in fields_dictionary:
        if field != dict_last_item:
            table_text += f'{field} {fields_dictionary[field]}, \n'
        else:
            table_text += f'{field} {fields_dictionary[field]}'

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        {table_text}
    );
    """)



#Aqui nesta função eu simplifico um pouco a função de adicionar elementos a uma table, ainda é necessario passar varios parametros
#Mas sinto que o código fica mais organizado
def add_to_table(cursor, table_name, table_fields_list, items_tuple_list):
    table_fields_str = ''
    fields_counter = ''

    for field in table_fields_list:
        #É importante verificar se é o ultimo elemento ou não, para a adição da virgula. Caso a virgula seja adicionada
        #E nenhum elemento acompanhe, o código retorna um erro
        if field != table_fields_list[len(table_fields_list)-1]:
            table_fields_str += f'{field}, '
            fields_counter += '?, '
        else:
                table_fields_str += f'{field}'
                fields_counter += '?'


    cursor.executemany(f"""
    INSERT INTO {table_name} ({table_fields_str})
    VALUES ({fields_counter});
    """, items_tuple_list)

#Uma versão do código anterior que faz a mesma coisa, porem adiciona apenas caso os campos informado não existam na Tabela
def add_to_table_unique(cursor, table_name, table_fields_list, items_tuple_list):
    unique_items = []

    for item in items_tuple_list:
        where_filter = ''
        for field in table_fields_list:
            #Aqui o field = ? serve como placeholder para valores que ainda serão imputados, para uma interação dinamica com a DB
            if field != table_fields_list[len(table_fields_list)-1]:
                where_filter += f'{field} = ? AND '
            else:
                where_filter += f'{field} = ?'

        #Filtra a se um item ja esta na tabela
        query_filter = f"""
        SELECT * FROM {table_name}
        WHERE {where_filter}
        """

        cursor.execute(query_filter, item)
        non_unique_item = cursor.fetchone()

        if not non_unique_item:
            unique_items.append(item)

    add_to_table(cursor, table_name, table_fields_list, unique_items)


#Função que edita um elemento de alguma tabela a partir do ID e campo para ser editado. Esses requisitos são necessarios para manter
#um bom controle de quem esta sendo editado na DB, sem editar o campo ou id errado. Tambem fornece mais versatilidade para a função
#em um grande projeto, pois se pedirmos informações muito especificas(como nome do estudante) a função se tornaria inutil ou confusa
#para o uso em uma tabela de lista de compras, por exemplo.

#O id deve vir no final, pois ele é opcional e caso não seja fornecido altera o valor de toda a tabela
def table_edit(conn, cursor, table_name, field, new_value, id_table=0):
    if id_table == 0:
        cursor.execute(f"UPDATE {table_name} SET {field} = '{new_value}'")
    else:
        cursor.execute(f"UPDATE {table_name} SET {field} = '{new_value}' WHERE id = {id_table}")
    conn.commit()


#Remove um item da tabela pelo ID. Achei o código muito breve para ser necessario, apenas fica mais confortavel pelo nome da função
#que é mais intuitivo.
def table_remove(cursor, table_name, id):
    cursor.execute(f"DELETE FROM {table_name} WHERE id={id}")


#Filtra a tabela por algum elemento escolhido, porem consegue filtrar apenas por um elemento por vez.
def filter_table(cursor, table_name, table_element, filter):
    query_filter = ''
    last_key = list(filter)[-1]

    for element in filter.keys():
        if element != last_key:
            query_filter += f'{table_element} {filter[element]} {element} OR '
        else:
            query_filter += f'{table_element} {filter[element]} {element}'

    cursor.execute(f"SELECT * FROM {table_name} WHERE {query_filter}")
    print(cursor.fetchall())



