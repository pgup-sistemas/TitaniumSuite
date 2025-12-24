import threading
from concurrent.futures import ThreadPoolExecutor
import time
from typing import Callable, Any, List

class TaskQueue:
    """
    Gerenciador de fila de tarefas para processamento em segundo plano.
    Usa ThreadPoolExecutor para não bloquear a interface principal (GUI).
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern para garantir que só haja uma fila."""
        if cls._instance is None:
            cls._instance = super(TaskQueue, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, max_workers: int = 4):
        if self._initialized:
            return
            
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks: List[Any] = [] # Lista de Future objects
        self.task_id_counter = 0
        self.progress_callback: Callable[[int, str, str], None] = lambda id, status, msg: print(f"Task {id}: {status} - {msg}")
        self._initialized = True

    def set_progress_callback(self, callback: Callable[[int, str, str], None]):
        """Define a função de callback para atualizar a interface com o progresso."""
        self.progress_callback = callback

    def submit_task(self, func: Callable, *args, **kwargs) -> int:
        """
        Submete uma função para ser executada em uma thread separada.
        Retorna o ID da tarefa.
        """
        self.task_id_counter += 1
        task_id = self.task_id_counter
        
        # Nome da tarefa para exibição na interface
        task_name = kwargs.pop('task_name', f"Tarefa {task_id}")
        
        # Função wrapper para gerenciar o ciclo de vida da tarefa
        def task_wrapper():
            self.progress_callback(task_id, "INICIADA", f"Executando {task_name}...")
            try:
                result = func(*args, **kwargs)
                self.progress_callback(task_id, "CONCLUÍDA", f"{task_name} finalizada com sucesso.")
                return result
            except Exception as e:
                self.progress_callback(task_id, "ERRO", f"{task_name} falhou: {e}")
                raise e
        
        future = self.executor.submit(task_wrapper)
        self.tasks.append(future)
        
        # Adiciona um callback para remover a tarefa da lista quando terminar
        future.add_done_callback(lambda f: self.tasks.remove(f))
        
        return task_id

    def get_active_tasks(self) -> List[str]:
        """Retorna uma lista de strings com o status das tarefas ativas."""
        active_tasks = []
        for task in self.tasks:
            if task.running():
                active_tasks.append(f"Executando: {task.arg_name}") # Assumindo que task_wrapper armazena o nome
            elif task.done():
                try:
                    task.result()
                    active_tasks.append(f"Concluída: {task.arg_name}")
                except Exception as e:
                    active_tasks.append(f"Erro: {task.arg_name} - {e}")
        return active_tasks

# Exemplo de uso (apenas para teste)
if __name__ == "__main__":
    def tarefa_demorada(segundos, nome):
        print(f"[{nome}] Iniciada. Vai durar {segundos}s.")
        time.sleep(segundos)
        print(f"[{nome}] Concluída.")
        return f"Resultado de {nome}"

    def meu_callback(id, status, msg):
        print(f"*** CALLBACK - ID {id} | STATUS {status} | MSG: {msg} ***")

    queue = TaskQueue()
    queue.set_progress_callback(meu_callback)

    print("Submetendo Tarefa 1...")
    queue.submit_task(tarefa_demorada, 5, "Limpeza de Disco", task_name="Limpeza de Disco")

    print("Submetendo Tarefa 2...")
    queue.submit_task(tarefa_demorada, 2, "Compressão de Imagens", task_name="Compressão de Imagens")

    # Simula o loop principal da GUI
    print("Loop principal da GUI continua rodando...")
    time.sleep(1)
    print("Loop principal da GUI continua rodando...")
    time.sleep(1)
    print("Loop principal da GUI continua rodando...")
    time.sleep(1)
    
    # Espera as tarefas terminarem (em um app real, a GUI faria isso)
    # for task in queue.tasks:
    #     task.result()
    
    print("Fim do script.")
