'''
Componente de UI para exibir o progresso das tarefas em segundo plano.
'''
import customtkinter as ctk
from src.utils.task_queue import TaskQueue

class TaskProgressPanel(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.task_queue = TaskQueue()
        self.task_widgets = {}

        self.configure(fg_color="transparent")

        # Título do painel
        self.title_label = ctk.CTkLabel(self, text="Fila de Tarefas", font=ctk.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=5, padx=10, anchor="w")

        # Frame com scroll para as tarefas
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="", fg_color="#2b2b2b")
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Configura o callback da fila de tarefas para atualizar este painel
        self.task_queue.set_progress_callback(self.update_task_progress)

    def update_task_progress(self, task_id: int, status: str, message: str):
        '''
        Callback que a TaskQueue chama para atualizar a UI.
        Esta função será executada em uma thread de background, então precisamos
        agendar a atualização da UI na thread principal usando `after`.
        '''
        self.after(0, self._update_ui, task_id, status, message)

    def _update_ui(self, task_id: int, status: str, message: str):
        '''Atualiza os widgets da interface gráfica na thread principal.'''
        if task_id not in self.task_widgets:
            # Cria um novo frame para a tarefa se for a primeira vez que a vemos
            task_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#333333", corner_radius=5)
            task_frame.pack(fill="x", expand=True, padx=5, pady=3)
            
            label = ctk.CTkLabel(task_frame, text=f"Iniciando...", anchor="w", font=ctk.CTkFont(size=12))
            label.pack(fill="x", padx=10, pady=2)
            
            progress = ctk.CTkProgressBar(task_frame, height=5)
            progress.pack(fill="x", padx=10, pady=(0, 5))
            progress.set(0)
            progress.start()

            self.task_widgets[task_id] = {"frame": task_frame, "label": label, "progress": progress}

        # Atualiza o widget existente
        widget_info = self.task_widgets[task_id]
        widget_info["label"].configure(text=message)

        if status == "CONCLUÍDA":
            widget_info["progress"].stop()
            widget_info["progress"].set(1)
            widget_info["frame"].configure(fg_color="green")
            # Remove a tarefa da lista após um tempo
            self.after(5000, lambda: self._remove_task_widget(task_id))

        elif status == "ERRO":
            widget_info["progress"].stop()
            widget_info["progress"].set(1)
            widget_info["frame"].configure(fg_color="red")
            # Não remove a tarefa com erro para que o usuário possa ver

    def _remove_task_widget(self, task_id):
        if task_id in self.task_widgets:
            self.task_widgets[task_id]["frame"].destroy()
            del self.task_widgets[task_id]
