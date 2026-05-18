import tkinter as tk
from tkinter import ttk, messagebox
import time
import winsound
import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path.home() / ".tomato_clock_stats.json"

MODE_WORK = "work"
MODE_BREAK = "break"
BG_COLOR = "#2d2d2d"
FONT_FAMILY = "Segoe UI"
COLOR_WORK = "#ff6b6b"
COLOR_BREAK = "#4ecdc4"
COLOR_RESET = "#6c757d"


class TomatoClock:
    WORK_MIN = 25
    BREAK_MIN = 5
    SOUND_FREQ = 880
    SOUND_DURATION = 500

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tomato Clock")
        self.root.geometry("360x500")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        self.work_min = self.WORK_MIN
        self.break_min = self.BREAK_MIN
        self.mode = MODE_WORK
        self.remaining = self.work_min * 60
        self.running = False
        self.paused = False
        self.sessions_today = 0
        self.start_time = None
        self._after_id = None

        self._load_stats()
        self._setup_ui()
        self._update_display()

    def _bg_frame(self, parent, **kw):
        return tk.Frame(parent, bg=BG_COLOR, **kw)

    def _bg_label(self, parent, text="", **kw):
        return tk.Label(parent, text=text, font=(FONT_FAMILY, 9), bg=BG_COLOR, **kw)

    def _setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        header = self._bg_frame(self.root, pady=15)
        header.pack(fill="x")

        self._bg_label(header, text="🍅", font=(FONT_FAMILY, 40)).pack()
        self._bg_label(header, text="Tomato Clock", font=(FONT_FAMILY, 16, "bold"),
                 fg="#e0e0e0").pack()

        self.timer_frame = self._bg_frame(self.root, pady=10)
        self.timer_frame.pack(fill="x")

        self.mode_label = self._bg_label(self.timer_frame, text="WORK",
                                    font=(FONT_FAMILY, 11, "bold"), fg=COLOR_WORK)
        self.mode_label.pack()

        self.timer_label = self._bg_label(self.timer_frame, text="25:00",
                                     font=(FONT_FAMILY, 56, "bold"), fg="#ffffff")
        self.timer_label.pack(pady=5)

        self.progress = ttk.Progressbar(self.timer_frame, length=280, mode="determinate")
        self.progress.pack(pady=5)

        self.controls = self._bg_frame(self.root, pady=15)
        self.controls.pack(fill="x")

        self.start_btn = self._create_button(self.controls, "▶  Start", COLOR_BREAK,
                                              self._toggle_start)
        self.start_btn.pack(side="left", expand=True, padx=5)

        self.reset_btn = self._create_button(self.controls, "⟲  Reset", COLOR_RESET,
                                              self._reset)
        self.reset_btn.pack(side="left", expand=True, padx=5)

        settings_frame = self._bg_frame(self.root, pady=5)
        settings_frame.pack(fill="x")

        self._bg_label(settings_frame, text="Work (min):", fg="#aaa"
                 ).grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.work_spin = tk.Spinbox(settings_frame, from_=1, to=120, width=4,
                                     font=(FONT_FAMILY, 10), justify="center")
        self.work_spin.delete(0, "end")
        self.work_spin.insert(0, str(self.work_min))
        self.work_spin.grid(row=0, column=1, padx=5, pady=2)

        self._bg_label(settings_frame, text="Break (min):", fg="#aaa"
                 ).grid(row=0, column=2, padx=5, pady=2, sticky="e")
        self.break_spin = tk.Spinbox(settings_frame, from_=1, to=60, width=4,
                                      font=(FONT_FAMILY, 10), justify="center")
        self.break_spin.delete(0, "end")
        self.break_spin.insert(0, str(self.break_min))
        self.break_spin.grid(row=0, column=3, padx=5, pady=2)

        settings_frame.grid_columnconfigure(1, weight=1)
        settings_frame.grid_columnconfigure(3, weight=1)

        self.stats_frame = self._bg_frame(self.root, pady=15)
        self.stats_frame.pack(fill="x", side="bottom")

        self.session_label = self._bg_label(self.stats_frame,
                                       text=self._session_text(),
                                       font=(FONT_FAMILY, 11), fg="#aaa")
        self.session_label.pack()

        self.root.bind("<space>", lambda e: self._toggle_start())
        self.root.bind("<r>", lambda e: self._reset())

    def _create_button(self, parent, text, color, command):
        btn = tk.Button(parent, text=text, font=("Segoe UI", 11, "bold"),
                        fg="white", bg=color, command=command,
                        relief="flat", padx=15, pady=8, cursor="hand2",
                        activebackground=self._lighten(color),
                        activeforeground="white", bd=0)
        btn.bind("<Enter>", lambda e: btn.configure(bg=self._lighten(color)))
        btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        return btn

    @staticmethod
    def _lighten(hex_color, factor=0.15):
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _read_settings(self):
        try:
            w = int(self.work_spin.get())
            b = int(self.break_spin.get())
            if w < 1 or b < 1:
                raise ValueError
            self.work_min = w
            self.break_min = b
            return True
        except ValueError:
            messagebox.showerror("Invalid", "Durations must be positive integers")
            return False

    def _toggle_start(self):
        if not self.running and not self.paused:
            if not self._read_settings():
                return
            self.mode = MODE_WORK
            self.remaining = self.work_min * 60
            self.mode_label.configure(text="WORK", fg=COLOR_WORK)
            self.running = True
            self.paused = False
            self.start_time = time.time()
            self._update_display()
            self._tick()
        elif self.running and not self.paused:
            self.paused = True
            self.start_btn.configure(text="▶  Resume", bg=COLOR_BREAK)
        elif self.running and self.paused:
            self.paused = False
            self.start_time = time.time() - (self.work_min * 60 - self.remaining)
            self.start_btn.configure(text="⏸  Pause", bg="#ffa726")
            self._tick()

    def total_seconds(self):
        return (self.work_min * 60) if self.mode == MODE_WORK else (self.break_min * 60)

    def _tick(self):
        if not self.running or self.paused:
            return

        elapsed = time.time() - (self.start_time or time.time())
        total = self.total_seconds()
        self.remaining = max(0, total - elapsed)

        self._update_display(total)

        if self.remaining <= 0:
            self._timer_done()
            return

        self._after_id = self.root.after(200, self._tick)

    def _update_display(self, total=None):
        mins, secs = divmod(int(self.remaining), 60)
        self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")

        if total is None:
            total = self.total_seconds()
        if total > 0:
            self.progress["value"] = ((total - self.remaining) / total) * 100
        else:
            self.progress["value"] = 0

    def _timer_done(self):
        self._beep()
        self.root.attributes("-topmost", True)
        self.root.attributes("-topmost", False)

        if self.mode == MODE_WORK:
            self.sessions_today += 1
            self._save_stats()
            self.mode = MODE_BREAK
            self.remaining = self.break_min * 60
            self.mode_label.configure(text="BREAK", fg=COLOR_BREAK)
            messagebox.showinfo("Work Done!",
                                f"🍅 Session {self.sessions_today} complete!\n"
                                f"Time for a {self.break_min}-minute break.")
        else:
            self.mode = MODE_WORK
            self.remaining = self.work_min * 60
            self.mode_label.configure(text="WORK", fg=COLOR_WORK)
            messagebox.showinfo("Break Over", "Back to work! 💪")

        self.running = False
        self.paused = False
        self.start_time = None
        self.start_btn.configure(text="▶  Start", bg=COLOR_BREAK)
        self._update_display()
        self._update_stats_display()

    def _beep(self):
        try:
            winsound.Beep(self.SOUND_FREQ, self.SOUND_DURATION)
            self.root.after(200, lambda: winsound.Beep(660, 300))
        except Exception:
            print("\a")

    def _reset(self):
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        self.running = False
        self.paused = False
        self.start_time = None
        self._read_settings()
        self.mode = MODE_WORK
        self.remaining = self.work_min * 60
        self.mode_label.configure(text="WORK", fg=COLOR_WORK)
        self.start_btn.configure(text="▶  Start", bg=COLOR_BREAK)
        self._update_display()
        self._update_stats_display()

    def _session_text(self):
        return f"🍅 Today: {self.sessions_today} session{'s' if self.sessions_today != 1 else ''} completed"

    def _update_stats_display(self):
        self.session_label.configure(text=self._session_text())

    def _load_stats(self):
        try:
            data = json.loads(DATA_FILE.read_text())
            if data.get("date") == datetime.now().strftime("%Y-%m-%d"):
                self.sessions_today = data.get("sessions", 0)
        except Exception:
            pass

    def _save_stats(self):
        try:
            DATA_FILE.write_text(json.dumps({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "sessions": self.sessions_today,
            }))
        except Exception:
            pass

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    TomatoClock().run()
