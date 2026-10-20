import mysql.connector
from mysql.connector import Error


class Contact:
    """Represents one contact."""

    def __init__(self, name, phone, email, contact_id=None):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def display(self):
        print("-" * 40)
        print("ID    :", self.contact_id)
        print("Name  :", self.name)
        print("Phone :", self.phone)
        print("Email :", self.email)


class ContactBook:
    """Manages contacts and MySQL database operations."""

    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gowri@123",
            database="contact_book_db"
        )
        self.cursor = self.db.cursor()

    @staticmethod
    def get_valid_contact_details():
        name = input("Enter name: ").strip()
        phone = input("Enter phone number: ").strip()
        email = input("Enter email: ").strip()

        if not name or not phone or not email:
            print("All fields are required.")
            return None

        if len(phone) != 10 or not phone.isdigit():
            print("Phone number must contain exactly 10 digits.")
            return None

        if "@" not in email or "." not in email:
            print("Enter a valid-looking email address.")
            return None

        return name, phone, email

    def add_contact(self):
        print("\n--- Add Contact ---")
        details = self.get_valid_contact_details()

        if details is None:
            return

        try:
            query = (
                "INSERT INTO contacts (name, phone, email) "
                "VALUES (%s, %s, %s)"
            )
            self.cursor.execute(query, details)
            self.db.commit()
            print("Contact added successfully!")

        except Error as error:
            self.db.rollback()
            if error.errno == 1062:
                print("Name, phone, or email already exists.")
            else:
                print("Could not add contact:", error)

    def view_contacts(self):
        self.cursor.execute(
            "SELECT contact_id, name, phone, email "
            "FROM contacts ORDER BY contact_id"
        )
        rows = self.cursor.fetchall()

        print("\n--- Contact List ---")
        if not rows:
            print("No contacts found.")
            return

        for row in rows:
            contact = Contact(row[1], row[2], row[3], row[0])
            contact.display()

    def search_contact(self):
        print("\n1. Search by name")
        print("2. Search by phone")
        choice = input("Choose: ").strip()

        if choice == "1":
            value = input("Enter name to search: ").strip()
            query = (
                "SELECT contact_id, name, phone, email FROM contacts "
                "WHERE name LIKE %s ORDER BY contact_id"
            )
            parameter = ("%" + value + "%",)

        elif choice == "2":
            value = input("Enter phone number to search: ").strip()
            query = (
                "SELECT contact_id, name, phone, email FROM contacts "
                "WHERE phone LIKE %s ORDER BY contact_id"
            )
            parameter = ("%" + value + "%",)

        else:
            print("Invalid choice.")
            return

        if not value:
            print("Search value cannot be empty.")
            return

        self.cursor.execute(query, parameter)
        rows = self.cursor.fetchall()

        if not rows:
            print("Contact not found.")
            return

        for row in rows:
            Contact(row[1], row[2], row[3], row[0]).display()

    def edit_contact(self):
        try:
            contact_id = int(input("Enter contact ID to edit: "))
            if contact_id <= 0:
                print("ID must be positive.")
                return
        except ValueError:
            print("Enter a valid numeric ID.")
            return

        self.cursor.execute(
            "SELECT contact_id, name, phone, email "
            "FROM contacts WHERE contact_id = %s",
            (contact_id,)
        )
        row = self.cursor.fetchone()

        if row is None:
            print("Contact not found.")
            return

        contact = Contact(row[1], row[2], row[3], row[0])
        contact.display()

        print("\nWhat do you want to edit?")
        print("1. Name")
        print("2. Phone")
        print("3. Email")
        print("4. All details")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                value = input("Enter new name: ").strip()
                if not value:
                    print("Name cannot be empty.")
                    return

                query = "UPDATE contacts SET name = %s WHERE contact_id = %s"
                values = (value, contact_id)

            elif choice == "2":
                value = input("Enter new phone number: ").strip()
                if len(value) != 10 or not value.isdigit():
                    print("Phone number must contain exactly 10 digits.")
                    return

                query = "UPDATE contacts SET phone = %s WHERE contact_id = %s"
                values = (value, contact_id)

            elif choice == "3":
                value = input("Enter new email: ").strip()
                if "@" not in value or "." not in value:
                    print("Enter a valid-looking email address.")
                    return

                query = "UPDATE contacts SET email = %s WHERE contact_id = %s"
                values = (value, contact_id)

            elif choice == "4":
                details = self.get_valid_contact_details()
                if details is None:
                    return

                query = (
                    "UPDATE contacts SET name = %s, phone = %s, email = %s "
                    "WHERE contact_id = %s"
                )
                values = details + (contact_id,)

            else:
                print("Invalid choice.")
                return

            self.cursor.execute(query, values)
            self.db.commit()

            if self.cursor.rowcount == 0:
                print("No changes made.")
            else:
                print("Contact updated successfully!")

        except Error as error:
            self.db.rollback()
            if error.errno == 1062:
                print("That name, phone, or email already belongs to another contact.")
            else:
                print("Could not update contact:", error)

    def delete_contact(self):
        try:
            contact_id = int(input("Enter contact ID to delete: "))
            if contact_id <= 0:
                print("ID must be positive.")
                return
        except ValueError:
            print("Enter a valid numeric ID.")
            return

        self.cursor.execute(
            "SELECT contact_id, name, phone, email "
            "FROM contacts WHERE contact_id = %s",
            (contact_id,)
        )
        row = self.cursor.fetchone()

        if row is None:
            print("Contact not found.")
            return

        Contact(row[1], row[2], row[3], row[0]).display()
        confirm = input("Are you sure you want to delete this contact? (yes/no): ")
        if confirm.strip().lower() != "yes":
            print("Deletion cancelled.")
            return

        try:
            self.cursor.execute(
                "DELETE FROM contacts WHERE contact_id = %s",
                (contact_id,)
            )
            self.db.commit()
            print("Contact deleted successfully!")

        except Error as error:
            self.db.rollback()
            print("Could not delete contact:", error)

    def close(self):
        self.cursor.close()
        self.db.close()


def main():
    book = None

    try:
        book = ContactBook()
        print("Connected to the Contact Book database.")

        while True:
            print("\n===== CONTACT BOOK =====")
            print("1. Add Contact")
            print("2. View Contacts")
            print("3. Search Contact")
            print("4. Edit Contact")
            print("5. Delete Contact")
            print("6. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                book.add_contact()
            elif choice == "2":
                book.view_contacts()
            elif choice == "3":
                book.search_contact()
            elif choice == "4":
                book.edit_contact()
            elif choice == "5":
                book.delete_contact()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Select 1 to 6.")

    except Error as error:
        print("MySQL connection or database error:", error)

    finally:
        if book is not None:
            book.close()


if __name__ == "__main__":
    main()
