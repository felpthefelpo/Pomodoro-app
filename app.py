import tkinter as tk
from tkinter import messagebox, filedialog
import time
import pygame
from plyer import notification

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("500x400")

        self.selected_sound = None

        self.time_left = 25 * 60  #25 minutos em segundos
        self.running = False

        self.label = tk.Label(root, text="25:00", font=("Helvetica", 48), bg="#363636", fg="white")
        self.label.pack(pady=10)

        self.start_button = tk.Button(root, text="Iniciar", command=self.start_timer)
        self.stop_button = tk.Button(root, text="Parar", command=self.stop_timer)
        self.reset_button = tk.Button(root, text="Reiniciar", command=self.reset_timer)

        self.start_button.pack(pady=5)
        self.stop_button.pack(pady=5)
        self.reset_button.pack(pady=5)

        self.duration_label = tk.Label(root, text="Duração do Pomodoro (minutos):")
        self.duration_label.pack(pady=5)
        self.duration_entry = tk.Entry(root)
        self.duration_entry.insert(0, "25")
        self.duration_entry.pack(pady=5)

        self.root.configure(bg="#363636")
        self.label.configure(fg="white")
        self.start_button.configure(bg="#007acc", fg="white")  
        self.stop_button.configure(bg="#e53935", fg="white")
        self.reset_button.configure(bg="#43a047", fg="white")

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

            pomodoro_duration = int(self.duration_entry.get()) * 60 
            self.time_left = pomodoro_duration
            self.update_display()

    def stop_timer(self):
        self.running = False

    def reset_timer(self):
        self.running = False
        self.time_left = 25 * 60
        self.update_display()

    def update_timer(self):
        if self.running and self.time_left > 0:
            minutes, seconds = divmod(self.time_left, 60)
            self.label.config(text=f"{minutes:02}:{seconds:02}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.running = False
            self.emitir_alerta("Tarefa Pomodoro Concluída")
            self.reset_timer()

    def emitir_alerta(self, tarefa):
        if self.selected_sound:
            pygame.mixer.music.load(self.selected_sound)
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.load("default_sound.mp3")
            pygame.mixer.music.play()
        notification_title = "Tarefa Pomodoro Concluída"
        notification_message = f"É hora de fazer a tarefa: {tarefa}!"
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_name="Pomodoro App",
            timeout=10 
        )

    def choose_sound(self):
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos de som", "*.wav *.mp3")])
        if file_path:
            self.selected_sound = file_path

    def update_display(self):
        minutes, seconds = divmod(self.time_left, 60)
        self.label.config(text=f"{minutes:02}:{seconds:02}")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
