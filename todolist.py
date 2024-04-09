from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_string)
        the_cursor.execute('INSERT INTO tasks VALUES (?)', (task_string,))
        the_connection.commit()  # Commit changes to the database
        list_update()
        task_field.delete(0, 'end')

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

def delete_task():
    try:
        selection = task_listbox.curselection()
        if selection:
            index = selection[0]
            task_value = task_listbox.get(index)
            tasks.remove(task_value)
            the_cursor.execute('DELETE FROM tasks WHERE title = ?', (task_value,))
            the_connection.commit()  # Commit changes to the database
            list_update()
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box:
        tasks.clear()
        the_cursor.execute('DELETE FROM tasks')
        the_connection.commit()  # Commit changes to the database
        list_update()

def clear_list():
    task_listbox.delete(0, 'end')

def close():
    print(tasks)
    guiWindow.destroy()

def retrieve_database():
    tasks.clear()
    for row in the_cursor.execute('SELECT title FROM tasks'):
        tasks.append(row[0])
    list_update()

if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("To-Do List")
    guiWindow.geometry("665x400+550+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#F0F8FF")  # Light Blue background

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')

    tasks = []

    functions_frame = Frame(guiWindow, bg="#ADD8E6")  # Light Blue Frame
    functions_frame.pack(side="top", expand=True, fill="both")

    task_label = Label(functions_frame, text="TO-DO-LIST \n Enter the Task Title:",
                       font=("Arial", "14", "bold"),
                       background="#ADD8E6",  # Light Blue Background
                       foreground="#000000"  # black Text
                       )
    task_label.place(x=20, y=30)

    task_field = Entry(
        functions_frame,
        font=("Arial", "14"),
        width=42,
        foreground="black",
        background="white",
    )
    task_field.place(x=180, y=30)

    add_button = Button(
        functions_frame,
        text="Add",
        width=15,
        bg='#ffa500', font=("Arial", "14", "bold"),  # Orange Button
        command=add_task,

    )
    del_button = Button(
        functions_frame,
        text="Remove",
        width=15,
        bg='#FFA500', font=("Arial", "14", "bold"),  # Orange Button
        command=delete_task,
    )
    del_all_button = Button(
        functions_frame,
        text="Delete All",
        width=15,
        font=("Arial", "14", "bold"),
        bg='#FFA500',  # Orange Button
        command=delete_all_tasks
    )

    exit_button = Button(
        functions_frame,
        text="Exit / Close",
        width=52,
        bg='#FFA500', font=("Arial", "14", "bold"),  # Orange Button
        command=close
    )
    add_button.place(x=18, y=80)
    del_button.place(x=240, y=80)
    del_all_button.place(x=460, y=80)
    exit_button.place(x=17, y=330)

    task_listbox = Listbox(
        functions_frame,
        width=70,
        height=9,
        font="bold",
        selectmode='SINGLE',
        background="WHITE",
        foreground="BLACK",
        selectbackground="#FF8C00",
        selectforeground="BLACK"
    )
    task_listbox.place(x=17, y=140)

    retrieve_database()
    guiWindow.mainloop()
    the_connection.close()  # Close the database connection
