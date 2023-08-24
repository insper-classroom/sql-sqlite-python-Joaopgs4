import sqlite3
from db.db_utils import *

#Declaração de valores
conn = sqlite3.connect('db/database_alunos.db')
cursor = conn.cursor()
table_dict = {'Nome': 'TEXT NOT NULL', 'Curso': 'TEXT NOT NULL', 'AnoIngresso': 'INTEGER'}
estudantes = [
    ("Ana Silva", "Computação", 2019),
    ("Pedro Mendes", "Física", 2021),
    ("Carla Souza", "Computação", 2020),
    ("João Alves", "Matemática", 2018),
    ("Maria Oliveira", "Química", 2022),
]


#Criação de tablea unica
create_table(cursor, 'Estudantes', table_dict)
#Adição de dados na tabela, adiciona apenas informações unicas para organizar a DB e testes.
add_to_table_unique(cursor, 'Estudantes', ['Nome', 'Curso', 'AnoIngresso'], estudantes)

#Até aqui o código printa todos os estudantes. Primeiro tópico pedido na parte 1
conn.commit()
print_table(cursor, 'Estudantes')
print()

#Printa os estudantes entre 2019-2020
#Utiliza a função Filter Table, mas ela consegue filtrar e printar apenas um filtro por vez. O usuario deve no dicionario escolher a comparação do filtro.
filter_table(cursor, 'Estudantes', 'AnoIngresso', {'2019': '=', '2020': '='})
print()

#Edita um valor da tabela, no caso esta editando o curso de um estudante para Medicina. Podemos ver que até é criado um novo elemento
#no ID 6 com o mesmo aluno e curso antigo, pois agora existe um elemento diferente, então ele é considerado unico.
table_edit(conn, cursor, 'Estudantes', 'Curso', 'Medicina', 4)
print_table(cursor, 'Estudantes')
print()

#Novamente editei o mesmo usuario de ID 4, mas dessa vez não foi criado um novo usuario no ID 7, pois ele não seria unico
#(o usuario de ID 6 esta inalterado)
table_edit(conn, cursor, 'Estudantes', 'AnoIngresso', '2077', 4)
print_table(cursor, 'Estudantes')
print()

#Deleta um elemento da tabela a partir do ID, no caso apaguei o ID 5
table_remove(cursor, 'Estudantes', 5)
print_table(cursor, 'Estudantes')
print()

#Filtra a tabela por valores maiores que 2019
filter_table(cursor, 'Estudantes', 'AnoIngresso', {'2019': '>'})
print()

#Aqui todos os cursos de todos os estudantes de computação é reescrito. Não achei necessario uma função separada
cursor.execute("UPDATE Estudantes SET AnoIngresso = 2018 WHERE Curso='Computação'")
conn.commit()
print_table(cursor, 'Estudantes')
print()