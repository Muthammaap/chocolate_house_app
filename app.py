import sqlite3

def connect_db():
    """Connects to the SQLite database."""
    return sqlite3.connect('chocolate_house.db')

def create_flavors_table(conn):
    """Creates a table for flavors in the database."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flavors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            seasonal TEXT NOT NULL
        )
    ''')
    conn.commit()
    print("Flavors table created successfully!")

def create_feedback_table(conn):
    """Creates a table for customer feedback in the database."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flavor_id INTEGER,
            suggestion TEXT,
            allergy_concern TEXT,
            FOREIGN KEY (flavor_id) REFERENCES flavors (id)
        )
    ''')
    conn.commit()
    print("Feedback table created successfully!")

def add_flavor(conn, name, seasonal):
    """Inserts a new flavor into the database."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flavors (name, seasonal) VALUES (?, ?)
    ''', (name, seasonal))
    conn.commit()
    print(f"Flavor '{name}' added successfully!")

def add_feedback(conn, flavor_id, suggestion, allergy_concern):
    """Inserts customer feedback into the database."""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (flavor_id, suggestion, allergy_concern) VALUES (?, ?, ?)
    ''', (flavor_id, suggestion, allergy_concern))
    conn.commit()
    print("Feedback added successfully!")

def display_feedback(conn):
    """Displays all customer feedback from the database."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM feedback')
    feedback_list = cursor.fetchall()
    
    if feedback_list:
        print("Customer Feedback:")
        for feedback in feedback_list:
            print(f"ID: {feedback[0]}, Flavor ID: {feedback[1]}, Suggestion: {feedback[2]}, Allergy Concern: {feedback[3]}")
    else:
        print("No feedback available.")

def delete_feedback(conn, feedback_id):
    """Deletes feedback from the database by ID."""
    cursor = conn.cursor()
    cursor.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
    conn.commit()
    print(f"Feedback with ID {feedback_id} deleted successfully!")

def main():
    """Main function to run the application."""
    print("Hello, Chocolate House!")
    conn = connect_db()
    create_flavors_table(conn)
    create_feedback_table(conn)

    while True:
        print("\nOptions:")
        print("1. Add Flavor")
        print("2. Provide Feedback")
        print("3. Display Feedback")
        print("4. Delete Feedback")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == '1':
            flavor_name = input("Enter the flavor name (or type 'exit' to finish): ")
            if flavor_name.lower() == 'exit':
                continue
            seasonal_status = input("Enter seasonal status (Yes/No): ")
            add_flavor(conn, flavor_name, seasonal_status)

        elif choice == '2':
            flavor_id = int(input("Enter the flavor ID to give feedback for: "))
            suggestion = input("Enter your suggestion: ")
            allergy_concern = input("Enter any allergy concerns: ")
            add_feedback(conn, flavor_id, suggestion, allergy_concern)

        elif choice == '3':
            display_feedback(conn)

        elif choice == '4':
            feedback_id = int(input("Enter the feedback ID to delete: "))
            delete_feedback(conn, feedback_id)

        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
