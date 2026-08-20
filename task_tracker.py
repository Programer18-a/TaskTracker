import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime

APP_NAME = "Task Tracker"

DATA_DIR = Path.home() / "TaskTracker"
DATA_FILE = DATA_DIR / "tasks.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)

BG = "#0b1120"
SIDEBAR = "#111827"
CARD = "#172033"
CARD_HOVER = "#1e293b"

TEXT = "#f8fafc"
MUTED = "#94a3b8"

ACCENT = "#38bdf8"
ACCENT_DARK = "#0284c7"

GREEN = "#22c55e"
GREEN_DARK = "#166534"

YELLOW = "#f59e0b"
YELLOW_DARK = "#92400e"

RED = "#ef4444"
RED_DARK = "#991b1b"

BLUE = "#60a5fa"

TODO = "todo"
IN_PROGRESS = "in-progress"
DONE = "done"

STATUS_NAMES = {
    TODO: "TODO",
    IN_PROGRESS: "IN PROGRESS",
    DONE: "DONE"
}

STATUS_ICONS = {
    TODO: "○",
    IN_PROGRESS: "◐",
    DONE: "✓"
}

STATUS_COLORS = {
    TODO: YELLOW,
    IN_PROGRESS: BLUE,
    DONE: GREEN
}

def current_time():
    return datetime.now().isoformat(timespec="seconds")


def format_date(value):
    if not value:
        return "-"

    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%d.%m.%Y %H:%M")
    except ValueError:
        return value


def load_tasks():


    if not DATA_FILE.exists():
        save_tasks([])
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        return data

    except (OSError, json.JSONDecodeError):
        messagebox.showerror(
            APP_NAME,
            "Не удалось прочитать tasks.json.\n\n"
            "Файл может быть повреждён."
        )
        return []


def save_tasks(tasks):

    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                tasks,
                file,
                ensure_ascii=False,
                indent=4
            )

    except OSError as error:
        messagebox.showerror(
            APP_NAME,
            f"Не удалось сохранить задачи:\n\n{error}"
        )


def next_id(tasks):
    if not tasks:
        return 1

    return max(
        task.get("id", 0)
        for task in tasks
    ) + 1

class TaskTracker(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("1100x720")
        self.minsize(900, 600)

        self.configure(bg=BG)

        self.tasks = load_tasks()

        self.current_filter = "all"
        self.search_text = tk.StringVar()

        self.setup_styles()
        self.create_interface()

        self.search_text.trace_add(
            "write",
            lambda *_: self.refresh_tasks()
        )

        self.refresh_tasks()

        # Горячие клавиши
        self.bind(
            "<Control-n>",
            lambda event: self.add_task()
        )

        self.bind(
            "<Control-f>",
            lambda event: self.search_entry.focus_set()
        )

        self.bind(
            "<Delete>",
            lambda event: self.delete_selected()
        )

    def setup_styles(self):

        style = ttk.Style(self)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=CARD,
            foreground=TEXT,
            fieldbackground=CARD,
            borderwidth=0,
            rowheight=48,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=SIDEBAR,
            foreground=MUTED,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI Semibold", 9)
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#26364f")
            ],
            foreground=[
                ("selected", TEXT)
            ]
        )

        style.configure(
            "Vertical.TScrollbar",
            background=SIDEBAR,
            troughcolor=BG,
            bordercolor=BG,
            arrowcolor=MUTED
        )

    def create_button(
        self,
        parent,
        text,
        command,
        background=ACCENT,
        foreground="#06111d",
        width=None
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=background,
            fg=foreground,
            activebackground=background,
            activeforeground=foreground,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            font=("Segoe UI Semibold", 10),
            padx=14,
            pady=8
        )

        if width:
            button.config(width=width)

        return button

    def create_interface(self):

        header = tk.Frame(
            self,
            bg=BG
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(24, 12)
        )

        title_frame = tk.Frame(
            header,
            bg=BG
        )

        title_frame.pack(
            side="left"
        )

        tk.Label(
            title_frame,
            text="✓",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 27, "bold")
        ).pack(
            side="left",
            padx=(0, 10)
        )

        title_text = tk.Frame(
            title_frame,
            bg=BG
        )

        title_text.pack(
            side="left"
        )

        tk.Label(
            title_text,
            text="TASK TRACKER",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI Semibold", 23)
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_text,
            text="Offline task management",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w"
        )

        tk.Label(
            header,
            text="LOCAL • OFFLINE",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI Semibold", 9)
        ).pack(
            side="right",
            pady=12
        )

        toolbar = tk.Frame(
            self,
            bg=BG
        )

        toolbar.pack(
            fill="x",
            padx=30,
            pady=10
        )

        search_frame = tk.Frame(
            toolbar,
            bg=CARD
        )

        search_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 12)
        )

        tk.Label(
            search_frame,
            text="⌕",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 16)
        ).pack(
            side="left",
            padx=(12, 5)
        )

        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_text,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT,
            selectbackground=ACCENT_DARK,
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 11)
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10,
            padx=(0, 10)
        )

        self.create_button(
            toolbar,
            "+ Add task",
            self.add_task
        ).pack(
            side="right"
        )

        main = tk.Frame(
            self,
            bg=BG
        )

        main.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(5, 15)
        )

        sidebar = tk.Frame(
            main,
            bg=SIDEBAR,
            width=210
        )

        sidebar.pack(
            side="left",
            fill="y",
            padx=(0, 18)
        )

        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="FILTER",
            bg=SIDEBAR,
            fg=MUTED,
            font=("Segoe UI Semibold", 9)
        ).pack(
            anchor="w",
            padx=20,
            pady=(22, 10)
        )

        self.filter_buttons = {}

        filters = [
            ("all", "◉   All tasks"),
            (TODO, "○   Todo"),
            (IN_PROGRESS, "◐   In progress"),
            (DONE, "✓   Completed")
        ]

        for status, label in filters:

            button = tk.Button(
                sidebar,
                text=label,
                command=lambda s=status: self.set_filter(s),
                bg=SIDEBAR,
                fg=TEXT,
                activebackground=CARD_HOVER,
                activeforeground=TEXT,
                relief="flat",
                borderwidth=0,
                anchor="w",
                padx=20,
                pady=12,
                cursor="hand2",
                font=("Segoe UI", 10)
            )

            button.pack(
                fill="x"
            )

            self.filter_buttons[status] = button

        self.statistics = tk.Label(
            sidebar,
            bg=SIDEBAR,
            fg=MUTED,
            justify="left",
            anchor="w",
            font=("Segoe UI", 9),
            padx=20
        )

        self.statistics.pack(
            fill="x",
            pady=(35, 0)
        )


        content = tk.Frame(
            main,
            bg=BG
        )

        content.pack(
            side="left",
            fill="both",
            expand=True
        )

        columns = (
            "id",
            "description",
            "status",
            "created",
            "updated"
        )

        self.task_table = ttk.Treeview(
            content,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.task_table.heading(
            "id",
            text="ID"
        )

        self.task_table.heading(
            "description",
            text="TASK"
        )

        self.task_table.heading(
            "status",
            text="STATUS"
        )

        self.task_table.heading(
            "created",
            text="CREATED"
        )

        self.task_table.heading(
            "updated",
            text="UPDATED"
        )


        self.task_table.column(
            "id",
            width=55,
            anchor="center"
        )

        self.task_table.column(
            "description",
            width=350,
            anchor="w"
        )

        self.task_table.column(
            "status",
            width=125,
            anchor="center"
        )

        self.task_table.column(
            "created",
            width=145,
            anchor="center"
        )

        self.task_table.column(
            "updated",
            width=145,
            anchor="center"
        )


        scrollbar = ttk.Scrollbar(
            content,
            orient="vertical",
            command=self.task_table.yview
        )

        self.task_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.task_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.task_table.bind(
            "<Double-1>",
            lambda event: self.edit_selected()
        )



        footer = tk.Frame(
            self,
            bg=BG
        )

        footer.pack(
            fill="x",
            padx=30,
            pady=(0, 25)
        )


        self.create_button(
            footer,
            "Edit",
            self.edit_selected,
            "#263449",
            TEXT
        ).pack(
            side="left",
            padx=(0, 8)
        )

        self.create_button(
            footer,
            "In progress",
            lambda: self.change_selected_status(IN_PROGRESS),
            "#263449",
            TEXT
        ).pack(
            side="left",
            padx=8
        )

        self.create_button(
            footer,
            "Done",
            lambda: self.change_selected_status(DONE),
            GREEN_DARK,
            TEXT
        ).pack(
            side="left",
            padx=8
        )

        self.create_button(
            footer,
            "Delete",
            self.delete_selected,
            RED_DARK,
            TEXT
        ).pack(
            side="right"
        )

    def set_filter(self, status):

        self.current_filter = status

        self.refresh_tasks()


    def get_filtered_tasks(self):

        result = self.tasks

        if self.current_filter != "all":

            result = [
                task
                for task in result
                if task.get("status") == self.current_filter
            ]


        query = self.search_text.get().strip().lower()

        if query:

            result = [
                task
                for task in result
                if query in task.get(
                    "description",
                    ""
                ).lower()
            ]


        return result

    def refresh_tasks(self):

        for item in self.task_table.get_children():

            self.task_table.delete(item)


        tasks = self.get_filtered_tasks()


        for task in tasks:

            status = task.get(
                "status",
                TODO
            )

            status_name = STATUS_NAMES.get(
                status,
                status
            )

            self.task_table.insert(
                "",
                "end",
                iid=str(task["id"]),
                values=(
                    task["id"],
                    task.get(
                        "description",
                        ""
                    ),
                    status_name,
                    format_date(
                        task.get(
                            "createdAt"
                        )
                    ),
                    format_date(
                        task.get(
                            "updatedAt"
                        )
                    )
                ),
                tags=(status,)
            )

        self.task_table.tag_configure(
            TODO,
            foreground=YELLOW
        )

        self.task_table.tag_configure(
            IN_PROGRESS,
            foreground=BLUE
        )

        self.task_table.tag_configure(
            DONE,
            foreground=GREEN
        )

        total = len(self.tasks)

        todo_count = sum(
            task.get("status") == TODO
            for task in self.tasks
        )

        progress_count = sum(
            task.get("status") == IN_PROGRESS
            for task in self.tasks
        )

        done_count = sum(
            task.get("status") == DONE
            for task in self.tasks
        )

        self.statistics.config(
            text=(
                f"TOTAL\n"
                f"{total}\n\n"

                f"TODO\n"
                f"{todo_count}\n\n"

                f"IN PROGRESS\n"
                f"{progress_count}\n\n"

                f"COMPLETED\n"
                f"{done_count}"
            )
        )

        for status, button in self.filter_buttons.items():

            if status == self.current_filter:

                button.config(
                    bg="#263449"
                )

            else:

                button.config(
                    bg=SIDEBAR
                )

    def add_task(self):

        self.open_task_dialog()

    def open_task_dialog(self, task=None):

        dialog = tk.Toplevel(self)

        dialog.title(
            "Edit task"
            if task
            else "New task"
        )

        dialog.geometry(
            "520x300"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.configure(
            bg=SIDEBAR
        )

        dialog.transient(
            self
        )

        dialog.grab_set()

        tk.Label(
            dialog,
            text=(
                "Edit task"
                if task
                else "New task"
            ),
            bg=SIDEBAR,
            fg=TEXT,
            font=("Segoe UI Semibold", 19)
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 18)
        )

        tk.Label(
            dialog,
            text="Description",
            bg=SIDEBAR,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=30
        )

        description = tk.Entry(
            dialog,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 12)
        )

        description.pack(
            fill="x",
            padx=30,
            pady=(7, 20),
            ipady=11
        )


        if task:

            description.insert(
                0,
                task.get(
                    "description",
                    ""
                )
            )


        description.focus_set()

        buttons = tk.Frame(
            dialog,
            bg=SIDEBAR
        )

        buttons.pack(
            fill="x",
            padx=30
        )


        def save():

            text = description.get().strip()

            if not text:

                messagebox.showwarning(
                    APP_NAME,
                    "Описание задачи не может быть пустым.",
                    parent=dialog
                )

                return


            if task:

                task["description"] = text

                task["updatedAt"] = current_time()

            else:

                timestamp = current_time()

                new_task = {
                    "id": next_id(self.tasks),

                    "description": text,

                    "status": TODO,

                    "createdAt": timestamp,

                    "updatedAt": timestamp
                }

                self.tasks.append(
                    new_task
                )


            save_tasks(
                self.tasks
            )

            self.refresh_tasks()

            dialog.destroy()


        self.create_button(
            buttons,
            "Cancel",
            dialog.destroy,
            "#263449",
            TEXT
        ).pack(
            side="right",
            padx=(8, 0)
        )


        self.create_button(
            buttons,
            "Save",
            save
        ).pack(
            side="right"
        )


        dialog.bind(
            "<Return>",
            lambda event: save()
        )

        dialog.bind(
            "<Escape>",
            lambda event: dialog.destroy()
        )

    def get_selected_task(self):

        selection = self.task_table.selection()

        if not selection:

            messagebox.showinfo(
                APP_NAME,
                "Сначала выберите задачу."
            )

            return None


        task_id = int(
            selection[0]
        )


        for task in self.tasks:

            if task.get("id") == task_id:

                return task


        return None

    def edit_selected(self):

        task = self.get_selected_task()

        if task:

            self.open_task_dialog(
                task
            )

    def change_selected_status(self, status):

        task = self.get_selected_task()

        if not task:

            return


        task["status"] = status

        task["updatedAt"] = current_time()


        save_tasks(
            self.tasks
        )

        self.refresh_tasks()

    def delete_selected(self):

        task = self.get_selected_task()

        if not task:

            return


        confirmed = messagebox.askyesno(
            "Delete task",
            (
                "Вы действительно хотите удалить задачу?\n\n"
                f"{task.get('description', '')}"
            ),
            parent=self
        )


        if not confirmed:

            return


        self.tasks.remove(
            task
        )

        save_tasks(
            self.tasks
        )

        self.refresh_tasks()

if __name__ == "__main__":

    app = TaskTracker()

    app.mainloop()