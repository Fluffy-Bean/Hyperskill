from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from models import Task, create_db


class ToDoList:
    def __init__(self):
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        self.session = sessionmaker(bind=self.engine)
        self.session = self.session()

        create_db(self.engine)

        self.main_menu()

    def main_menu(self):
        print("\n1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add a task")
        print("6) Delete a task")
        print("0) Exit")

        _ = input()

        if _ == "1":
            self.display_today_tasks()
        elif _ == "2":
            self.display_week_tasks()
        elif _ == "3":
            self.display_all_tasks()
        elif _ == "4":
            self.missed_tasks()
        elif _ == "5":
            self.add_task()
        elif _ == "6":
            self.delete_task()
        elif _ == "0":
            print("Bye!")
            exit()

    def display_today_tasks(self):
        today = datetime.today().date()
        tasks = self.session.query(Task).filter(Task.deadline == today).all()

        print(f"\nToday {today.day} {today.strftime('%b')}:")

        if not tasks:
            print("Nothing to do!")
        else:
            [print(f"{task.id}) {task.task}") for task in tasks]

        self.main_menu()

    def display_week_tasks(self):
        today = datetime.today().date()
        today_in_a_week = today + timedelta(days=7)
        tasks = self.session.query(Task).\
            filter(Task.deadline.between(today, today_in_a_week)).\
            order_by(Task.deadline).all()

        for i in range(7):
            day = today + timedelta(days=i)
            print(f"\n{day.strftime('%A')} {day.day} {day.strftime('%b')}:")
            if not tasks:
                print("Nothing to do!")
            else:
                [print(f"{task.id}) {task.task}") for task in tasks]

        self.main_menu()

    def display_all_tasks(self):
        tasks = self.session.query(Task).order_by(Task.deadline).all()

        print("\nAll tasks:")

        if not tasks:
            print("Nothing to do!")
        else:
            [print(f"{task.id}. {task.task}. {task.deadline.day} {task.deadline.strftime('%b')}") for task in tasks]

        self.main_menu()

    def add_task(self):
        print("\nEnter task")
        task = input().strip()
        print("Enter deadline")
        deadline = input().strip()

        self.session.add(Task(task=task, deadline=datetime.strptime(deadline, "%Y-%m-%d").date()))
        self.session.commit()

        print("The task has been added!")

        self.main_menu()

    def missed_tasks(self):
        tasks = self.session.query(Task).filter(Task.deadline < datetime.today().date()).all()

        print("\nMissed tasks:")
        if not tasks:
            print("Nothing is missed!")
        else:
            [print(f"{task.id}. {task.task}. {task.deadline.day} {task.deadline.strftime('%b')}") for task in tasks]

        self.main_menu()

    def delete_task(self):
        tasks = self.session.query(Task).order_by(Task.deadline).all()

        print("\nChoose the number of the task you want to delete:")
        if not tasks:
            print("Nothing to delete!")
            return

        [print(f"{task.id}. {task.task}. {task.deadline.day} {task.deadline.strftime('%b')}") for task in tasks]
        _ = int(input())

        self.session.delete(tasks[_ - 1])
        self.session.commit()

        print("The task has been deleted!")

        self.main_menu()


if __name__ == "__main__":
    todo = ToDoList()
