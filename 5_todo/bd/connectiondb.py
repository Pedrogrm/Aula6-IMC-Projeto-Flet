import sqlite3  # Importa o módulo sqlite3 para trabalhar com banco de dados SQLite

# Classe que gerencia o banco de dados para as tarefas (ToDo)
class DataBase:
    def __init__(self):
        """Inicializa a classe do banco de dados e cria a tabela de tarefas se ela não existir"""
        # Executa o comando SQL para criar a tabela 'tasks', caso ela não exista
        self.dbExecute('CREATE TABLE IF NOT EXISTS tasks("task" TEXT NOT NULL UNIQUE, "status" TEXT NOT NULL)')

    def dbExecute(self, query, params=[]):
        """
        Executa comandos SQL no banco de dados.
        
        query: String contendo o comando SQL.
        params: Lista de parâmetros para o comando (usada em consultas preparadas para evitar SQL injection).
        """
        # Conecta ao banco de dados SQLite localizado em 'bd/database.sqlite'
        with sqlite3.connect('bd/database.sqlite') as con:
            cur = con.cursor()  # Cria um cursor para executar comandos SQL
            # Executa o comando SQL com os parâmetros fornecidos
            cur.execute(query, params)
            con.commit()  # Confirma as mudanças no banco de dados
            # Retorna os resultados da consulta, caso haja (fetchall retorna todas as linhas)
            return cur.fetchall()

    def addTasks(self, name, value):
        """
        Adiciona uma nova tarefa ao banco de dados.
        
        name: Nome da tarefa.
        value: Status da tarefa ('incomplete' ou 'complete').
        """
        # Insere a nova tarefa no banco de dados
        self.dbExecute('INSERT INTO tasks("task", "status") VALUES(?, ?)', params=[name, value])
        print('Adicionado ao Banco de Dados - Ok')  # Exibe uma mensagem de sucesso

    def updateTasks(self, value, task):
        """
        Atualiza o status de uma tarefa no banco de dados.
        
        value: Novo status da tarefa ('incomplete' ou 'complete').
        task: Nome da tarefa que será atualizada.
        """
        # Atualiza o status da tarefa no banco de dados
        self.dbExecute('UPDATE "tasks" SET "status" = ? WHERE "task" = ?', params=[value, task])
        print('Atualizado com sucesso')  # Exibe uma mensagem de sucesso

    def searchItens(self, query):
        """
        Busca tarefas no banco de dados com base em uma consulta SQL.
        
        query: Comando SQL para buscar tarefas.
        Retorna uma lista de tarefas correspondentes.
        """
        # Executa a consulta SQL e retorna as tarefas encontradas
        tasks = self.dbExecute(query)
        return tasks

    def deleteTasks(self, task):
        """
        Exclui uma tarefa do banco de dados.
        
        task: Nome da tarefa a ser excluída.
        """
        # Remove a tarefa do banco de dados
        self.dbExecute('DELETE FROM "tasks" WHERE "task" = ?', params=[task])
        print('Tarefa excluída com sucesso')  # Exibe uma mensagem de sucesso