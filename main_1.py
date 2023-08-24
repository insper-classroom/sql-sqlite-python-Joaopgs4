import sqlite3

# Exercício de Python - Sqlite

# Conexão com o banco de dados dentro da pasta "db"
conn = sqlite3.connect('db/database_alunos.db')
cursor = conn.cursor()

# Vamos criar uma tabela chamada "Estudantes" com os seguintes campos:
# ID (chave primária) -  Criado automáticamente pela base de dados
# Nome
# Curso
# Ano de Ingresso

cursor.execute("""
CREATE TABLE IF NOT EXISTS Estudantes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    Curso TEXT NOT NULL,
    AnoIngresso INTEGER
);
""")

#Cria os estudantes
estudantes = [
    ("Ana Silva", "Computação", 2019),
    ("Pedro Mendes", "Física", 2021),
    ("Carla Souza", "Computação", 2020),
    ("João Alves", "Matemática", 2018),
    ("Maria Oliveira", "Química", 2022),
]

#Aplica os estudantes ou adiciona mais
#Deixei comentado para não adicionar multiplos estudantes iguais durante os testes.

# cursor.executemany("""
# INSERT INTO Estudantes (Nome, Curso, AnoIngresso)
# VALUES (?, ?, ?);
# """, estudantes)


#Confirma mudanças, como no github
conn.commit()

#Exibe a tabela

#Exibe todos alunos
cursor.execute("SELECT * FROM Estudantes")
print(cursor.fetchall())

#White Space
print()

#Exibe Alunos de 2019-2020
cursor.execute("SELECT * FROM Estudantes WHERE AnoIngresso = 2019 OR AnoIngresso = 2020")
print(cursor.fetchall())

#White Space
print()

#Edita o Ano de Ingresso de um estudante
cursor.execute("UPDATE Estudantes SET AnoIngresso = 5024 WHERE Nome = 'João Alves'")
conn.commit()

cursor.execute("SELECT * FROM Estudantes")
print(cursor.fetchall())

#Deleta um estudante pelo ID
cursor.execute("DELETE FROM Estudantes WHERE id=4")
cursor.execute("SELECT * FROM Estudantes")
print(cursor.fetchall())

#Mostra estudantes ingressados após 2019
cursor.execute("SELECT * FROM Estudantes WHERE AnoIngresso >= 2019 AND Curso = 'Computação'")
print(cursor.fetchall())

#Muda o ano de ingresso de todos alunos
cursor.execute("UPDATE Estudantes SET AnoIngresso = 2018 WHERE Curso='Computação'")
cursor.execute("SELECT * FROM Estudantes WHERE Curso = 'Computação'")
print(cursor.fetchall())

