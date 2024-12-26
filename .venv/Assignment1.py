import os  # Importing the OS module to perform system-level operations like clearing the console
import json  # To save and load data in JSON format
book_library = []  # An empty list to store all book records as dictionaries

# Use Function to check positive integer input
def check_positive_integer(user_input):
    while True:  # Repeat until valid input is provided
        try:
            number = int(input(user_input))  # Prompt the user for input and convert to an integer
            if number < 0:  # Check if the number is negative
                print(colored_text("Error! You write negative number. Please enter a non-negative number.", "red"))
            else:
                return number  # Return the valid positive integer
        except ValueError:  # this is case where input cannot be converted to an integer, and write string
            print(colored_text("Error! You write invalid data. Please enter a valid number. It should be a positive integer.", "red"))

# Function to change font colors for user-friendly design
def colored_text(text, color):
    colors = {  # Dictionary. Define ANSI escape codes for different colors
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"  # Return text written text in the specified color code, get is a method of dictionary

# Function to clear the console
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')  # We import os, so we can clear console, 'cls' for Windows and 'clear' for other systems

# Function to save library data to a JSON file
def save_library_to_file():
    with open('library_data.json', 'w') as file:     # Open (or create) 'library_data.json' in write mode
        json.dump(book_library, file, indent=4)       # Write the book_library list as JSON to the file with indentation for readability
    print(colored_text("Library data has been saved successfully!", "cyan"))    # Notify the user that the data has been saved successfully


# Function to load library data from a JSON file
def load_library_from_file():
    global book_library    # Access the global book_library variable to modify it
    try:
        with open('library_data.json', 'r') as file:     # Open 'library_data.json' in read mode
            book_library = json.load(file)   # Load the JSON data from the file into the book_library list
        print(colored_text("Library data has been loaded successfully!", "cyan"))   # Notify the user that the data has been loaded successfully
    except FileNotFoundError:   # Handle the case where the file does not exist
        print(colored_text("No previous library data found. Starting with an empty library.", "yellow"))  # Inform the user that no data file exists and an empty library will be used


# Function to clear the library database
def clear_database():
    global book_library    # Access the global book_library variable to modify it
    book_library = []    # Reset the book_library list to an empty list
    if os.path.exists('library_data.json'):     # Check if the 'library_data.json' file exists in the current directory
        os.remove('library_data.json') # Delete the 'library_data.json' file if it exists
    print(colored_text("Library database has been cleared successfully!", "red"))  # The message notifying the user that the library database has been cleared successfully

# Function to add a book
def add_book_to_library():
    book_title = input("Enter book title: ").strip()  # Get book title and remove extra spaces at the beginning anf at the end
    book_author = input("Enter author name: ").strip()  # Get author name and remove extra spaces
    publication_year = check_positive_integer("Enter publication year: ")  # Get published year of book and ensure the year is a positive integer
    number_of_copies = check_positive_integer("Enter number of copies: ")  # Get copies of book and ensure the number of copies is positive

    for item in book_library:  # Iterate over all books in the library
        if item['book_title'].lower() == book_title.lower():  # Check if the book already exists (When a user enters a book title, they might not match the exact capitalization of the title stored in the library.)
            item['available_copies'] += number_of_copies  # Update the number of copies if the entered title of book already existing in library
            print(colored_text(f"Updated the number of copies for '{book_title}'.", "green"))
            return  # Exit the function once the book is updated

    # Add the new book to the library if it doesn't already exist
    book_library.append({
        'book_title': book_title,
        'book_author': book_author,
        'publication_year': publication_year,
        'available_copies': number_of_copies
    })
    print(colored_text(f"Book '{book_title}' has been added to the book library.", "cyan"))

# Function to search for a book
def find_book():
    search_title = input("Enter book title to search: ").strip()  # Get the title of book to search book in library
    results = [item for item in book_library if search_title.lower() in item['book_title'].lower()]  # Find books in library
    if results:  # If there are matching results
        print(colored_text(f"Found {len(results)} result(s):", "green"))
        for item in results:  # Show message about finding book in library, it can show each matching book, so there can be more than one option
            print(f"Title: {item['book_title']}, Author: {item['book_author']}, Year: {item['publication_year']}, Copies Available: {item['available_copies']}")
    else:  # If no matches are found
        print(colored_text("The book was not found. Please make sure that you entered correct title of book.", "red"))

# Function to borrow a book
def borrow_book():
    borrow_title = input("Enter book title to borrow: ").strip()  # Get the title of the book to borrow
    for item in book_library:  # Iterate over all books in the library
        if item['book_title'].lower() == borrow_title.lower():  # Check if the book exists in library (When a user enters a book title, they might not match the exact capitalization of the title stored in the library)
            if item['available_copies'] > 0:  # Check if there are available copies
                item['available_copies'] -= 1  # Decrease the number of available copies by 1 (decrement number of copies)
                print(colored_text(f"You have successfully borrowed '{borrow_title}'. Enjoy your reading!", "green"))
                return
            else:  # If no copies are available
                print(colored_text(f"Sorry, all copies of '{borrow_title}' are currently borrowed. But we have another interesting books, you can see the list of available copies in 5 option. ", "yellow"))
                return
    print(colored_text(f"'{borrow_title}' not found in the library.", "red"))  # If the book is not found by title of book

# Function to return a book
def return_book():
    return_title = input("Enter book title to return: ").strip()  # Get the title of the book to return
    for item in book_library:  # Iterate over all books in the library
        if item['book_title'].lower() == return_title.lower():  # Check if the book exists (When a user enters a book title, they might not match the exact capitalization of the title stored in the library)
            item['available_copies'] += 1  # Increase the number of available copies by 1 (increment number of copies)
            print(colored_text(f"Thank you for returning '{return_title}'. book. We hope you liked this book!", "green"))
            return
    print(colored_text(f"'{return_title}' is not recognized as part of our book system in  library. Please check the title of book.", "red"))  # If the book is not found

# Function to view all books
def show_information_book():
    if not book_library:  # If the library is empty
        print(colored_text("No books are currently in the library system.", "yellow"))
        return

    # Print table headers with aligned columns, using tabular format
    print(colored_text(f"{'Title':<40} {'Author':<30} {'Year':<10} {'Copies':<50}", "blue"))
    print(colored_text("-" * 90, "magenta"))  # Print a separator line
    for item in book_library:  # Display details of each book in the library
        print(f"{item['book_title']:<40} {item['book_author']:30} {item['publication_year']:<10} {item['available_copies']:<50}")

# Count total books in library (additional function that I add)
def total_books():
    total = sum(item['available_copies'] for item in book_library)  # Calculate the total number of available copies
    print(colored_text(f"The total number of books in the library is: {total}", "cyan"))  # Display the total number of copies of all books

# Main program loop
def main_program():
    load_library_from_file()  # Load data at the start
    user_name = input("Please enter your name: ").strip()  # Get the user's name
    print(colored_text(f"\nHello, Dear {user_name}. Welcome to Book Library!", "magenta"))  # Greet the user
    print(colored_text(f"\nInstruction: You can see 8 choices for you. Please choose the action that you want to do in number.", "red")) #Show some instructions

    while True:  # Loop until the user chooses to exit
        # Display menu options
        print(colored_text("\n1. Add a Book", "blue"))
        print(colored_text("2. Search for a Book", "blue"))
        print(colored_text("3. Borrow a Book", "blue"))
        print(colored_text("4. Return a Book", "blue"))
        print(colored_text("5. View All Books", "blue"))
        print(colored_text("6. Total Number of Books", "blue"))
        print(colored_text("7. Clear Library Database", "blue"))
        print(colored_text("8. Exit", "blue"))

        # Prompt the user to select an option
        user_choice = input(colored_text("\nWhat you want to do? (choose a number): ", "cyan")).strip()  #user input the choice
        if user_choice == '1':
            add_book_to_library()  # Add a new book to the library
        elif user_choice == '2':
            find_book()  # Search for a book
        elif user_choice == '3':
            borrow_book()  # Borrow a book
        elif user_choice == '4':
            return_book()  # Return a borrowed book
        elif user_choice == '5':
            show_information_book()  # Display all books in the library
        elif user_choice == '6':
            total_books()  # Display the total number of books
        elif user_choice == '7':
            clear_database()  #Clear the existing database, clear all data
        elif user_choice == '8':
            save_library_to_file() #save all data to the file
            print(colored_text("Exiting the program. Thank you for using our Book Library! See you soon! Goodbye!", "magenta"))  # Exit the program
            break
        else:
            print(colored_text("Error! You choose invalid data. Please select a valid option.", "red"))  # This message shows if user enter invalid number that not in the range of option

# Run the program
if __name__ == "__main__":
    main_program()  # Start the main program loop
