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
        row = self.my_cursor.fetchone()
        if row is not None and row[0] == 0:

            self.my_cursor.execute("ALTER TABLE vdata ADD COLUMN check_out TIMESTAMP")
            print("New column 'check_out' added successfully.")
        else:
            print("Column 'check_out' already exists in the table.")

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
                
    def checkout_visitors(self, id):
      
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            query = "UPDATE vdata SET check_out = NOW() WHERE id = %s"
            self.my_cursor.execute (query, (id,))
            self.conn.commit()
            print(f"Visitor with ID {id} has been successfully checked out at ")
        except mysql.connector.Error as e:
            print("Error checking out visitor: ", {e})  

   
    def run(self):
        while True:
            print("\n1. Log Visitor")
            print("2. Display Visitors")
            print("3. Check-out")
            print("4. Exit")

            choice = input("Enter your choice (1/2/3/4): ")

            if choice == '1':
                name = input("Enter visitor's name: ")
                purpose = input("Enter purpose of visit: ")
                self.log_visitor(name, purpose)
            elif choice == '2':
                self.display_visitors()
            elif choice =='3':
                id = int(input("Enter visitor ID to check out: "))
                self.checkout_visitors(id)
            elif choice == '4':
                print("Exiting Visitor Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    vms = VisitorManagementSystem()
    vms.run()
