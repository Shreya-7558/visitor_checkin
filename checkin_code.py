import mysql.connector
import datetime

class VisitorManagementSystem:
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost", user="root", password="", database="visitor")
        self.my_cursor = self.conn.cursor()
        self.create_table_if_not_exists()
        
    def create_table_if_not_exists(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS vdata (
            id INT AUTO_INCREMENT ,
            name VARCHAR(255) NOT NULL PRIMARY KEY,
            purpose VARCHAR(255) NOT NULL,
            timestamp DATETIME NOT NULL
        );
        """
        self.my_cursor.execute(create_table_query)
        self.conn.commit()

    def log_visitor(self, name, purpose):
        timestamp = datetime.datetime.now()
        insert_query = "INSERT INTO vdata (name, purpose, timestamp) VALUES (%s, %s, %s)"
        data = (name, purpose, timestamp)
        self.my_cursor.execute(insert_query, data)
        self.conn.commit()
        print(f"{name} logged in at {timestamp} for {purpose}.")

    def display_visitors(self):
        select_query = "SELECT * FROM vdata"
        self.my_cursor.execute(select_query)
        result = self.my_cursor.fetchall()

        if not result:
            print("No visitors at the moment.")
        else:
            print("\nVisitor Log:")
            for row in result:
                print(f"ID: {row[0]} | Name: {row[1]} | Purpose: {row[2]} | Time: {row[3]}")

    def run(self):
        while True:
            print("\n1. Log Visitor")
            print("2. Display Visitors")
            print("3. Exit")

            choice = input("Enter your choice (1/2/3): ")

            if choice == '1':
                name = input("Enter visitor's name: ")
                purpose = input("Enter purpose of visit: ")
                self.log_visitor(name, purpose)
            elif choice == '2':
                self.display_visitors()
            elif choice == '3':
                print("Exiting Visitor Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    vms = VisitorManagementSystem()
    vms.run()
