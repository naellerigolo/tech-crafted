import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview

# Initialize database
def init_db():
    conn = sqlite3.connect("fitness_tracker_ui.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS workouts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        workout_type TEXT,
                        duration INTEGER,
                        calories INTEGER)''')
    conn.commit()
    conn.close()

# Add workout to the database
def add_workout():
    workout_type = workout_type_entry.get()
    duration = duration_entry.get()
    calories = calories_entry.get()

    if not (workout_type and duration and calories):
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    try:
        duration = int(duration)
        calories = int(calories)
    except ValueError:
        messagebox.showerror("Input Error", "Duration and Calories must be numbers.")
        return

    conn = sqlite3.connect("fitness_tracker_ui.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO workouts (date, workout_type, duration, calories) VALUES (?, ?, ?, ?)",
                   (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), workout_type, duration, calories))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Workout added successfully!")
    workout_type_entry.delete(0, END)
    duration_entry.delete(0, END)
    calories_entry.delete(0, END)
    view_workouts()

# View all workouts in the treeview
def view_workouts():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("fitness_tracker_ui.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workouts")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", END, values=row)

# Initialize the main app window
def main_app():
    global workout_type_entry, duration_entry, calories_entry, tree

    root = Tk()
    root.title("Fitness Tracker")
    root.geometry("600x400")

    # Input Section
    input_frame = Frame(root)
    input_frame.pack(pady=10)

    Label(input_frame, text="Workout Type:").grid(row=0, column=0, padx=5, pady=5)
    workout_type_entry = Entry(input_frame)
    workout_type_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(input_frame, text="Duration (min):").grid(row=1, column=0, padx=5, pady=5)
    duration_entry = Entry(input_frame)
    duration_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(input_frame, text="Calories Burned:").grid(row=2, column=0, padx=5, pady=5)
    calories_entry = Entry(input_frame)
    calories_entry.grid(row=2, column=1, padx=5, pady=5)

    Button(input_frame, text="Add Workout", command=add_workout).grid(row=3, column=0, columnspan=2, pady=10)

    # Treeview Section
    tree_frame = Frame(root)
    tree_frame.pack(pady=10)

    tree = Treeview(tree_frame, columns=("ID", "Date", "Workout", "Duration", "Calories"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Date", text="Date")
    tree.heading("Workout", text="Workout")
    tree.heading("Duration", text="Duration (min)")
    tree.heading("Calories", text="Calories")
    tree.column("ID", width=30)
    tree.column("Date", width=150)
    tree.column("Workout", width=100)
    tree.column("Duration", width=100)
    tree.column("Calories", width=100)
    tree.pack()

    view_workouts()

    root.mainloop()

# Run the app
if __name__ == "__main__":
    init_db()
    main_app()