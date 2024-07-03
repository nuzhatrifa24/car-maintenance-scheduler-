import json
import os


class CarMaintenanceScheduler:
    def __init__(self):
        # Attempt to use __file__ if available, otherwise default to a safe path (e.g., current working directory)
        try:
            self.base_dir = os.path.dirname(__file__)
        except NameError:
            # Fallback to the current working directory if __file__ is not defined
            self.base_dir = os.getcwd()

        self.data_file = os.path.join(self.base_dir, 'car_maintenance_data.json')
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {
                'maintenance_tasks': {},
                'last_performed_mileage': {},
                'current_mileage': 0,
            }

    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def update_mileage(self):
        try:
            new_mileage = int(input("Enter current mileage: "))
            self.data['current_mileage'] = new_mileage
            self.save_data()
            print("Current mileage updated.")
        except ValueError:
            print("Invalid mileage. Please enter a number.")

    def add_maintenance_task(self):
        task_name = input("Enter the name of the new maintenance task: ")
        try:
            interval = int(input("Enter the maintenance interval (in miles): "))
            self.data['maintenance_tasks'][task_name] = interval
            self.data['last_performed_mileage'][task_name] = 0
            self.save_data()
            print(f"{task_name} added to maintenance tasks.")
        except ValueError:
            print("Invalid interval. Please enter a number.")

    def remove_maintenance_task(self):
        task_name = input("Enter the name of the maintenance task to remove: ")
        if task_name in self.data['maintenance_tasks']:

            del self.data['maintenance_tasks'][task_name]
            del self.data['last_performed_mileage'][task_name]
            self.save_data()
            print(f"{task_name} removed from maintenance tasks.")
        else:
            print("Task not found.")

    def mark_task_completed(self):
        task_name = input("Enter the name of the maintenance task you completed: ")
        if task_name in self.data['maintenance_tasks']:
            self.data['last_performed_mileage'][task_name] = self.data['current_mileage']
            self.save_data()
            print(f"Marked {task_name} as completed.")
        else:
            print("Task not found.")

    def modify_task_intervals(self):
        task_name = input("Enter the name of the maintenance task to modify: ")
        if task_name in self.data['maintenance_tasks']:
            try:
                new_interval = int(input("Enter the new maintenance interval (in miles): "))
                self.data['maintenance_tasks'][task_name] = new_interval
                self.save_data()
                print(f"Interval for {task_name} updated.")
            except ValueError:
                print("Invalid interval. Please enter a number.")
        else:
            print("Task not found.")

    def check_due_tasks(self):
        due_tasks = [task for task, interval in self.data['maintenance_tasks'].items()
                     if self.data['current_mileage'] >= self.data['last_performed_mileage'][task] + interval]
        if due_tasks:
            print("The following maintenance tasks are due:")
            for task in due_tasks:
                print(f"- {task}")
        else:
            print("No maintenance tasks are due.")

    def notify_due_tasks(self):
        due_tasks = [task for task, interval in self.data['maintenance_tasks'].items()
                     if self.data['current_mileage'] >= self.data['last_performed_mileage'][task] + interval]
        if due_tasks:
            print("Notification: The following maintenance tasks are due:")
            for task in due_tasks:
                print(f"- {task}")
        else:
            print("Notification: No maintenance tasks are due.")


def main():
    scheduler = CarMaintenanceScheduler()
    while True:
        print("\nCar Maintenance Scheduler")
        print("1. Update current mileage")
        print("2. Mark a maintenance task as completed")
        print("3. Modify maintenance task intervals")
        print("4. Check due maintenance tasks")
        print("5. Add a maintenance task")
        print("6. Remove a maintenance task")
        print("7. Notify due maintenance tasks")
        print("8. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            scheduler.update_mileage()
        elif choice == '2':
            scheduler.mark_task_completed()
        elif choice == '3':
            scheduler.modify_task_intervals()
        elif choice == '4':
            scheduler.check_due_tasks()
        elif choice == '5':
            scheduler.add_maintenance_task()
        elif choice == '6':
            scheduler.remove_maintenance_task()
        elif choice == '7':
            scheduler.notify_due_tasks()
        elif choice == '8':
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == '__main__':
    main()