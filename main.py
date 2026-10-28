"""
Tower of Hanoi Visual Simulator
A Python Tkinter project with animated recursive solution, step controls,
minimum move calculation, and a move history panel.

Run: python main.py
Requires: Python 3.8+ (Tkinter is included with most standard Python installations).
"""

import tkinter as tk
from tkinter import ttk, messagebox


class HanoiSimulator:
    BG = "#f4f7fb"
    ROD = "#526579"
    BASE = "#34495e"
    DISK_COLORS = ["#ef476f", "#f78c6b", "#ffd166", "#06d6a0",
                   "#118ab2", "#7b61ff", "#d65db1", "#4d908e",
                   "#f9844a", "#577590"]

    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi — Visual Simulator")
        self.root.geometry("1050x720")
        self.root.minsize(850, 620)
        self.root.configure(bg=self.BG)

        self.disk_count = tk.IntVar(value=4)
        self.speed = tk.IntVar(value=500)
        self.status = tk.StringVar(value="Choose the number of disks, then press Start.")
        self.move_text = tk.StringVar(value="Moves: 0")
        self.minimum_text = tk.StringVar(value="Minimum moves: 15")
        self.step_text = tk.StringVar(value="Step: 0 / 15")

        self.rods = {"A": [], "B": [], "C": []}
        self.moves = []
        self.move_index = 0
        self.after_id = None
        self.running = False
        self.paused = False

        self._build_ui()
        self.reset()

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#183153", height=76)
        header.pack(fill="x")
        tk.Label(header, text="TOWER OF HANOI", font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#183153").pack(pady=(12, 0))
        tk.Label(header, text="Interactive recursive puzzle visualizer",
                 font=("Segoe UI", 10), fg="#dce7f5", bg="#183153").pack()

        controls = tk.Frame(self.root, bg=self.BG, padx=14, pady=10)
        controls.pack(fill="x")
        tk.Label(controls, text="Number of disks:", bg=self.BG,
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        self.disk_box = ttk.Combobox(controls, textvariable=self.disk_count,
                                     values=list(range(1, 11)), width=5, state="readonly")
        self.disk_box.pack(side="left", padx=(7, 15))
        self.disk_box.bind("<<ComboboxSelected>>", lambda _e: self.reset())

        ttk.Button(controls, text="Reset", command=self.reset).pack(side="left", padx=3)
        self.start_button = ttk.Button(controls, text="▶ Start", command=self.start)
        self.start_button.pack(side="left", padx=3)
        self.pause_button = ttk.Button(controls, text="Ⅱ Pause", command=self.pause)
        self.pause_button.pack(side="left", padx=3)
        ttk.Button(controls, text="⏭ Next Move", command=self.next_move).pack(side="left", padx=3)
        ttk.Button(controls, text="⏮ Previous Move", command=self.previous_move).pack(side="left", padx=3)

        speed_frame = tk.Frame(controls, bg=self.BG)
        speed_frame.pack(side="right")
        tk.Label(speed_frame, text="Animation delay (ms)", bg=self.BG).pack()
        ttk.Scale(speed_frame, from_=80, to=1200, variable=self.speed,
                  orient="horizontal", length=150).pack()

        info = tk.Frame(self.root, bg=self.BG, padx=14)
        info.pack(fill="x")
        for var in (self.move_text, self.minimum_text, self.step_text):
            tk.Label(info, textvariable=var, bg="#e3edf8", fg="#183153",
                     font=("Segoe UI", 10, "bold"), padx=12, pady=8).pack(side="left", padx=(0, 8))

        body = tk.Frame(self.root, bg=self.BG, padx=14, pady=10)
        body.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(body, bg="white", highlightthickness=1,
                                highlightbackground="#d8e1ec", height=430)
        self.canvas.pack(side="left", fill="both", expand=True)

        side = tk.Frame(body, bg=self.BG, width=250)
        side.pack(side="right", fill="y", padx=(12, 0))
        tk.Label(side, text="MOVE HISTORY", font=("Segoe UI", 11, "bold"),
                 bg=self.BG, fg="#183153").pack(anchor="w", pady=(0, 6))
        self.history = tk.Listbox(side, width=31, height=20, font=("Consolas", 9),
                                  activestyle="none", bg="white", relief="flat",
                                  highlightthickness=1, highlightbackground="#d8e1ec")
        self.history.pack(fill="both", expand=True)
        tk.Label(side, text="Rules\n• Move one disk at a time.\n• Only the top disk can move.\n• Never place a larger disk on a smaller disk.",
                 justify="left", bg="#e3edf8", fg="#183153",
                 font=("Segoe UI", 9), padx=10, pady=10, wraplength=220).pack(fill="x", pady=(10, 0))

        footer = tk.Frame(self.root, bg="#183153", padx=14, pady=8)
        footer.pack(fill="x")
        tk.Label(footer, textvariable=self.status, bg="#183153", fg="white",
                 font=("Segoe UI", 9)).pack(anchor="w")

    def reset(self):
        self._cancel_animation()
        n = max(1, min(10, int(self.disk_count.get())))
        self.disk_count.set(n)
        self.rods = {"A": list(range(n, 0, -1)), "B": [], "C": []}
        self.moves = []
        self._solve(n, "A", "C", "B")
        self.move_index = 0
        self.running = False
        self.paused = False
        self.history.delete(0, tk.END)
        self.minimum_text.set(f"Minimum moves: {2**n - 1:,}")
        self.status.set("Ready. All disks start on rod A.")
        self._update_labels()
        self.draw()

    def _solve(self, n, source, destination, auxiliary):
        if n == 0:
            return
        self._solve(n - 1, source, auxiliary, destination)
        self.moves.append((source, destination))
        self._solve(n - 1, auxiliary, destination, source)

    def _cancel_animation(self):
        if self.after_id is not None:
            try:
                self.root.after_cancel(self.after_id)
            except tk.TclError:
                pass
            self.after_id = None

    def start(self):
        if self.move_index >= len(self.moves):
            self.reset()
        self.running = True
        self.paused = False
        self.status.set("Animation running…")
        self._animate_next()

    def pause(self):
        if self.running and not self.paused:
            self.paused = True
            self._cancel_animation()
            self.status.set("Paused. Press Start to continue.")
        elif self.running and self.paused:
            self.paused = False
            self.status.set("Animation running…")
            self._animate_next()
        else:
            self.status.set("Press Start to play the solution.")

    def _animate_next(self):
        if not self.running or self.paused:
            return
        if self.move_index >= len(self.moves):
            self.running = False
            self.status.set("Solved! All disks are now on rod C.")
            self._update_labels()
            return
        self._perform_move()
        delay = max(80, int(self.speed.get()))
        self.after_id = self.root.after(delay, self._animate_next)

    def next_move(self):
        self._cancel_animation()
        self.running = False
        self.paused = False
        if self.move_index >= len(self.moves):
            self.status.set("Puzzle is already solved. Press Reset to start again.")
            return
        self._perform_move()

    def previous_move(self):
        self._cancel_animation()
        self.running = False
        self.paused = False
        if self.move_index == 0:
            self.status.set("You are at the first step.")
            return
        source, destination = self.moves[self.move_index - 1]
        disk = self.rods[destination].pop()
        self.rods[source].append(disk)
        self.move_index -= 1
        if self.history.size():
            self.history.delete(tk.END)
        self._update_labels()
        self.draw()
        self.status.set(f"Reversed move {self.move_index + 1}: disk {disk} from {destination} to {source}.")

    def _perform_move(self):
        if self.move_index >= len(self.moves):
            return
        source, destination = self.moves[self.move_index]
        if not self.rods[source]:
            return
        disk = self.rods[source].pop()
        if self.rods[destination] and self.rods[destination][-1] < disk:
            messagebox.showerror("Invalid move", "A larger disk cannot be placed on a smaller disk.")
            self.rods[source].append(disk)
            return
        self.rods[destination].append(disk)
        self.move_index += 1
        message = f"{self.move_index:>4}. Disk {disk}: {source} → {destination}"
        self.history.insert(tk.END, message)
        self.history.selection_clear(0, tk.END)
        self.history.selection_set(tk.END)
        self.history.see(tk.END)
        self._update_labels()
        self.draw()
        self.status.set(f"Moved disk {disk} from rod {source} to rod {destination}.")

    def _update_labels(self):
        self.move_text.set(f"Moves: {self.move_index:,}")
        self.step_text.set(f"Step: {self.move_index:,} / {len(self.moves):,}")

    def draw(self):
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 550)
        height = max(self.canvas.winfo_height(), 350)
        self.canvas.create_text(width / 2, 22, text="Move every disk from A to C",
                                fill="#526579", font=("Segoe UI", 12, "bold"))
        base_y = height - 45
        top_y = 70
        self.canvas.create_rectangle(35, base_y, width - 35, base_y + 10,
                                     fill=self.BASE, outline=self.BASE)
        centers = [width * 0.19, width * 0.50, width * 0.81]
        rod_names = ["A", "B", "C"]
        rod_height = base_y - top_y
        for center, name in zip(centers, rod_names):
            self.canvas.create_rectangle(center - 5, top_y, center + 5, base_y,
                                         fill=self.ROD, outline=self.ROD)
            self.canvas.create_text(center, base_y + 25, text=f"ROD {name}",
                                    fill="#183153", font=("Segoe UI", 11, "bold"))
            disks = self.rods[name]
            max_disk = max(1, int(self.disk_count.get()))
            disk_h = min(28, max(14, (rod_height - 12) / max_disk))
            for level, disk in enumerate(disks):
                y2 = base_y - level * disk_h
                y1 = y2 - disk_h + 2
                disk_width = 36 + (disk / max_disk) * min(width * 0.19, 125)
                color = self.DISK_COLORS[(disk - 1) % len(self.DISK_COLORS)]
                self.canvas.create_rectangle(center - disk_width / 2, y1,
                                             center + disk_width / 2, y2 - 1,
                                             fill=color, outline="#ffffff", width=1)
                self.canvas.create_text(center, (y1 + y2) / 2 - 1, text=str(disk),
                                        fill="#ffffff" if disk not in (3,) else "#183153",
                                        font=("Segoe UI", 9, "bold"))
        self.canvas.create_text(width - 85, 22, text=f"n = {self.disk_count.get()}",
                                fill="#183153", font=("Segoe UI", 10))

    def on_resize(self, _event):
        self.draw()


def main():
    root = tk.Tk()
    app = HanoiSimulator(root)
    app.canvas.bind("<Configure>", app.on_resize)
    root.mainloop()


if __name__ == "__main__":
    main()
