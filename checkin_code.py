import mysql.connector
import datetime
import random

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
        
    def generate_random_name(self):
        # List of common names
        names = ["Harshal", "Ganesha", "Devyani", "Sampada", "Maithali", "Emily", "Mandira", "Dipali", "Rohan", "Olivia", "Praful", "Akash", "Mahesh", "Tinku", "Rashmi", "Pratik", "Prachit", "Shubham", "Nikunj"]
        # Choose a random name from the list
        return random.choice(names)

    def log_visitor(self, purpose):
        name= self.generate_random_name()
        year = 2023
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Assuming February has 28 days
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        timestamp = datetime.datetime(year, month, day, hour, minute, second)

        insert_query = "INSERT INTO vdata (name, purpose, timestamp) VALUES (%s, %s, %s)"
        data = (name, purpose, timestamp)

        try:
            self.my_cursor.execute(insert_query, data)
            self.conn.commit()
            print(f"{name} logged in at {timestamp} for {purpose}.")
        except mysql.connector.Error as e:
            print(f"Error logging visitor: {e}")

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
                
    def checkout_random_visitor(self, id):
        try:
            query = "SELECT timestamp FROM vdata WHERE id = %s"
            self.my_cursor.execute(query, (id,))
            timestamp = self.my_cursor.fetchone()[0]

            if timestamp:  # If visitor exists
                checkout_time = self.generate_checkout_time(timestamp)
                
                # Ensure checkout time is strictly after login time either date-wise or time-wise
                while checkout_time <= timestamp:
                    checkout_time = self.generate_checkout_time(timestamp)
            
                query = "UPDATE vdata SET check_out = %s WHERE id = %s AND timestamp = %s"
                self.my_cursor.execute(query, (checkout_time, id, timestamp))
                self.conn.commit()
            
                print(f"Visitor with ID {id} has been successfully checked out at {checkout_time}")
            else:
                print(f"No visitor found with ID {id}.")
        except mysql.connector.Error as e:
             print("Error checking out visitor:", e)

    def generate_checkout_time(self, timestamp):
        year = timestamp.year
        month = timestamp.month
        day = timestamp.day
        hour = random.randint(timestamp.hour, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        # Ensure checkout date is strictly after login date
        checkout_date = timestamp.date() + datetime.timedelta(days=random.randint(1, 30))
        
        # Construct the checkout time
        checkout_time = datetime.datetime(checkout_date.year, checkout_date.month, checkout_date.day, hour, minute, second)

        return checkout_time

    def close_connection(self):
        self.my_cursor.close()
        self.conn.close()
        
    
    def run(self):
        while True:
            print("\n1. Log Visitor")
            print("2. Display Visitors")
            print("3. Check-out")
            print("4. Train Decision Tree Classifier")
            print("5. Exit")

            choice = input("Enter your choice (1/2/3/4): ")

            if choice == '1':
                purpose = input("Enter purpose of visit: ")
                self.log_visitor(purpose)
            elif choice == '2':
                self.display_visitors()
            elif choice =='3':
                id = int(input("Enter visitor ID to check out: "))
                self.checkout_random_visitor(id)
            elif choice == '4':
                print("Exiting Visitor Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    vms = VisitorManagementSystem()
    vms.run()
    vms.close_connection()
    