# pomodoro_timer.py
import tkinter as tk
from tkinter import messagebox
import threading
import os
from sound_manager import SoundManager

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Pomodoro')
        self.root.geometry('600x1000')
        self.root.configure(background='#c95e54')

        # Initialize sound manager
        self.sound_manager = SoundManager()

        # Timer settings (in minutes)
        self.pomodoro_duration = 25
        self.short_break_duration = 5
        self.long_break_duration = 15

        # Timer state (in seconds)
        self.current_duration = self.pomodoro_duration * 60
        self.timer_running = False
        self.timer_id = None

        # Active mode
        self.mode = 'Pomodoro'  # or 'Short Break' or 'Long Break'

        # Initialize UI
        self.create_widgets()
        self.update_time_display()

        self.root.mainloop()

    def create_widgets(self):
        # Settings button
        self.settings_button = tk.Button(
            self.root, text='Settings', highlightbackground='#c95e54',
            command=self.open_settings)
        self.settings_button.pack(pady=20)

        # Main frame
        self.main_frame = tk.Frame(self.root, background='#ce6e66')
        self.main_frame.pack()

        # Mode buttons
        self.pomodoro_button = tk.Button(
            self.main_frame, text='Pomodoro', highlightbackground='#ce6e66',
            command=self.activate_pomodoro)
        self.pomodoro_button.grid(row=0, column=0)

        self.short_break_button = tk.Button(
            self.main_frame, text='Short Break', highlightbackground='#ce6e66',
            command=self.activate_short_break)
        self.short_break_button.grid(row=0, column=1)

        self.long_break_button = tk.Button(
            self.main_frame, text='Long Break', highlightbackground='#ce6e66',
            command=self.activate_long_break)
        self.long_break_button.grid(row=0, column=2)

        # Time display
        self.time_display = tk.Label(
            self.main_frame, font=("Arial", 100), fg='#fff', background='#ce6e66')
        self.time_display.grid(row=1, column=0, columnspan=3)

        # Start/Stop button
        self.start_stop_button = tk.Button(
            self.main_frame, text='Start', highlightbackground='#ce6e66',
            command=lambda: [self.sound_manager.play_sound('click'), self.start_stop_timer()])
        self.start_stop_button.grid(row=2, column=1)

    def start_stop_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_stop_button.config(text='Stop')
            self.cancel_timer()
            self.run_timer()
        else:
            self.timer_running = False
            self.start_stop_button.config(text='Start')
            self.cancel_timer()

    def run_timer(self):
        if not self.timer_running:
            return

        if self.current_duration >= 0:
            self.update_time_display()
            self.timer_id = self.root.after(1000, self.countdown)
        else:
            self.timer_running = False
            self.start_stop_button.config(text='Start')
            self.timer_id = None
            # Play finish sound
            self.sound_manager.play_sound('finish')
            # Reset the timer for the current mode
            self.current_duration = self.get_mode_duration() * 60
            self.update_time_display()

    def countdown(self):
        if not self.timer_running:
            return
        self.current_duration -= 1
        self.run_timer()

    def update_time_display(self):
        if self.current_duration >= 0:
            minutes, seconds = divmod(self.current_duration, 60)
            time_formatted = f"{int(minutes):02}:{int(seconds):02}"
        else:
            time_formatted = "00:00"
        self.time_display.config(text=time_formatted)

    def cancel_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def change_theme(self, root_bg, frame_bg):
        self.root.configure(background=f'#{root_bg}')
        self.settings_button.configure(highlightbackground=f'#{root_bg}')
        self.main_frame.configure(background=f'#{frame_bg}')
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(highlightbackground=f'#{frame_bg}')
        self.time_display.configure(background=f'#{frame_bg}')

    def activate_pomodoro(self):
        self.mode = 'Pomodoro'
        self.change_theme('c95e54', 'ce6e66')
        self.reset_timer(self.pomodoro_duration * 60)

    def activate_short_break(self):
        self.mode = 'Short Break'
        self.change_theme('5d8f94', '6e9a9f')
        self.reset_timer(self.short_break_duration * 60)

    def activate_long_break(self):
        self.mode = 'Long Break'
        self.change_theme('527ba0', '6588aa')
        self.reset_timer(self.long_break_duration * 60)

    def reset_timer(self, duration):
        self.timer_running = False
        self.cancel_timer()
        self.start_stop_button.config(text='Start')
        self.current_duration = duration
        self.update_time_display()

    def get_mode_duration(self):
        if self.mode == 'Pomodoro':
            return self.pomodoro_duration
        elif self.mode == 'Short Break':
            return self.short_break_duration
        elif self.mode == 'Long Break':
            return self.long_break_duration

    def open_settings(self):
        if hasattr(self, 'settings_window') and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("390x650")
        self.settings_window.configure(background='#ffffff')
        self.settings_window.protocol("WM_DELETE_WINDOW", self.settings_window.destroy)

        tk.Label(self.settings_window, text="Time (minutes)", font=("Arial", 20),
                 fg='#555555', background='#ffffff').pack()

        # Pomodoro time setting
        tk.Label(self.settings_window, text="Pomodoro", font=("Arial", 15), fg='#555555',
                 background='#ffffff', width=120).pack(pady=10)
        self.pomodoro_entry = tk.Entry(self.settings_window, font=(
            'Arial', 15), bg='#EEEEEE', bd=2, justify='center', fg='#000000')
        self.pomodoro_entry.insert(0, str(self.pomodoro_duration))
        self.pomodoro_entry.pack()
        tk.Button(self.settings_window, text='Set', highlightbackground='#ffffff',
                  command=self.set_pomodoro_time).pack(pady=5)

        # Short Break time setting
        tk.Label(self.settings_window, text="Short Break", font=("Arial", 15), fg='#555555',
                 background='#ffffff', width=120).pack(pady=10)
        self.short_break_entry = tk.Entry(self.settings_window, font=(
            'Arial', 15), bg='#EEEEEE', bd=2, justify='center', fg='#000000')
        self.short_break_entry.insert(0, str(self.short_break_duration))
        self.short_break_entry.pack()
        tk.Button(self.settings_window, text='Set', highlightbackground='#ffffff',
                  command=self.set_short_break_time).pack(pady=5)

        # Long Break time setting
        tk.Label(self.settings_window, text="Long Break", font=("Arial", 15), fg='#555555',
                 background='#ffffff', width=120).pack(pady=10)
        self.long_break_entry = tk.Entry(self.settings_window, font=(
            'Arial', 15), bg='#EEEEEE', bd=2, justify='center', fg='#000000')
        self.long_break_entry.insert(0, str(self.long_break_duration))
        self.long_break_entry.pack()
        tk.Button(self.settings_window, text='Set', highlightbackground='#ffffff',
                  command=self.set_long_break_time).pack(pady=5)

    def set_pomodoro_time(self):
        time = self.get_time_from_entry(self.pomodoro_entry)
        if time is not None:
            self.pomodoro_duration = time
            if self.mode == 'Pomodoro':
                self.reset_timer(self.pomodoro_duration * 60)

    def set_short_break_time(self):
        time = self.get_time_from_entry(self.short_break_entry)
        if time is not None:
            self.short_break_duration = time
            if self.mode == 'Short Break':
                self.reset_timer(self.short_break_duration * 60)

    def set_long_break_time(self):
        time = self.get_time_from_entry(self.long_break_entry)
        if time is not None:
            self.long_break_duration = time
            if self.mode == 'Long Break':
                self.reset_timer(self.long_break_duration * 60)

    def get_time_from_entry(self, entry):
        try:
            time = int(entry.get())
            if time <= 0:
                raise ValueError("Time must be greater than zero.")
            if time > 999:
                time = 999
                messagebox.showwarning("Maximum Time Exceeded",
                                       "Maximum allowed time is 999 minutes. Time has been set to 999 minutes.")
            return time
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number greater than zero.")
            return None
