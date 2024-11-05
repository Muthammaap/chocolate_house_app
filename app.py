import streamlit as st
import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('chocolate_house.db')

# Check if tables exist; create them if they don't
def initialize_database():
    cursor = conn.cursor()

    # Table for flavors
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flavors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            seasonal INTEGER NOT NULL
        )
    ''')

    # Table for ingredients
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity_in_stock REAL NOT NULL,
            unit TEXT NOT NULL
        )
    ''')

    # Table for customer suggestions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flavor_suggestion TEXT NOT NULL,
            allergy_concern TEXT
        )
    ''')

    conn.commit()

# Initialize the database
initialize_database()

# Helper function to display the structure of any table
def check_table_structure(table_name):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    structure = cursor.fetchall()
    st.write(f"Table Structure for {table_name}:")
    st.write(structure)

# Display Flavors
def display_flavors():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flavors')
    flavors = cursor.fetchall()
    df = pd.DataFrame(flavors, columns=["ID", "Name", "Seasonal"])
    st.write("Available Flavors:")
    st.table(df)

# Display Ingredients
def display_ingredients():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ingredients')
    ingredients = cursor.fetchall()
    df = pd.DataFrame(ingredients, columns=["ID", "Name", "Quantity in Stock", "Unit"])
    st.write("Ingredient Inventory:")
    st.table(df)

# Display Customer Suggestions
def display_suggestions():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer_suggestions')
    suggestions = cursor.fetchall()
    df = pd.DataFrame(suggestions, columns=["ID", "Flavor Suggestion", "Allergy Concern"])
    st.write("Customer Suggestions:")
    st.table(df)

# Streamlit App Layout
st.title("Chocolate House Management System")

# Sidebar menu
option = st.sidebar.selectbox("Select an option", ["View Flavors", "Add Flavor", "Delete Flavor", "Update Flavor",
                                                   "Manage Ingredients", "Customer Suggestions"])

# Flavor Management
if option == "View Flavors":
    display_flavors()

elif option == "Add Flavor":
    flavor_name = st.text_input("Enter the name of the flavor:")
    seasonal = st.radio("whether the entered flavor seasonal?", ("Yes=1", "No=0"))
    if st.button("Add Flavor"):
        cursor = conn.cursor()
        cursor.execute('INSERT INTO flavors (name, seasonal) VALUES (?, ?)', (flavor_name, 1 if seasonal == "Yes" else 0))
        conn.commit()
        st.success(f"Flavor '{flavor_name}' added successfully!")
        display_flavors()

elif option == "Delete Flavor":
    display_flavors()
    flavor_id = st.number_input("Enter flavor ID  to delete:", min_value=1, step=1)
    if st.button("Delete Flavor"):
        cursor = conn.cursor()
        cursor.execute('DELETE FROM flavors WHERE id = ?', (flavor_id,))
        conn.commit()
        st.success(f"Flavor with ID {flavor_id} deleted successfully!")
        display_flavors()

elif option == "Update Flavor":
    display_flavors()
    flavor_id = st.number_input("Enter the flavor Id to be  updated:", min_value=1, step=1)
    new_flavor_name = st.text_input("Enter new flavor name:")
    new_seasonal = st.radio("whether the entered flavor seasonal?", ("Yes=1", "No=0"))
    if st.button("Update Flavor"):
        cursor = conn.cursor()
        cursor.execute('UPDATE flavors SET name = ?, seasonal = ? WHERE id = ?', 
                       (new_flavor_name, 1 if new_seasonal == "Yes" else 0, flavor_id))
        conn.commit()
        st.success(f"Flavor with ID {flavor_id} updated successfully!")
        display_flavors()

# Ingredient Management
elif option == "Manage Ingredients":
    sub_option = st.radio("Select Ingredient Option", ["View Ingredients", "Add Ingredient", "Update Ingredient Quantity"])
    
    if sub_option == "View Ingredients":
        display_ingredients()

    elif sub_option == "Add Ingredient":
        ingredient_name = st.text_input("Ingredient Name:")
        quantity = st.number_input("Quantity in Stock:", min_value=0.0, step=0.1)
        unit = st.text_input("Unit (e.g., grams, kg, liters):")
        if st.button("Add Ingredient"):
            cursor = conn.cursor()
            cursor.execute('INSERT INTO ingredients (name, quantity_in_stock, unit) VALUES (?, ?, ?)', 
                           (ingredient_name, quantity, unit))
            conn.commit()
            st.success(f"Ingredient '{ingredient_name}' added successfully with quantity {quantity} {unit}.")
            display_ingredients()

    elif sub_option == "Update Ingredient Quantity":
        display_ingredients()
        ingredient_id = st.number_input("Enter the id  of the ingredient to be updated:", min_value=1, step=1)
        new_quantity = st.number_input("New quantity in stock:", min_value=0.0, step=0.1)
        if st.button("Update Quantity"):
            cursor = conn.cursor()
            cursor.execute('UPDATE ingredients SET quantity_in_stock = ? WHERE id = ?', 
                           (new_quantity, ingredient_id))
            conn.commit()
            st.success(f"Ingredient ID {ingredient_id} updated to new quantity {new_quantity}.")
            display_ingredients()

# Customer Suggestions
elif option == "Customer Suggestions":
    sub_option = st.radio("Select Option", ["View Suggestions", "Add Suggestion"])

    if sub_option == "View Suggestions":
        display_suggestions()

    elif sub_option == "Add Suggestion":
        flavor_suggestion = st.text_input("Flavor suggestion:")
        allergy_concern = st.text_input("Allergy Concern (if any):")
        if st.button("Submit Suggestion"):
            cursor = conn.cursor()
            cursor.execute('INSERT INTO customer_suggestions (flavor_suggestion, allergy_concern) VALUES (?, ?)', 
                           (flavor_suggestion, allergy_concern))
            conn.commit()
            st.success("Thank you for your suggestion!")
            display_suggestions()

# Close the database connection (optional)
conn.close()
