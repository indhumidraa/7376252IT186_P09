
DATA_FILE = "contacts.txt"


def load_contacts():
    contacts = []

    try:
        file = open(DATA_FILE, "r")

        for line in file:
            line = line.strip()

            if line:
                parts = line.split("|")

                if len(parts) == 4:
                    contacts.append(parts)

        file.close()

    except FileNotFoundError:
        file = open(DATA_FILE, "w")
        file.close()

    return contacts


def save_contacts(contacts):
    file = open(DATA_FILE, "w")

    for contact in contacts:
        file.write("|".join(contact) + "\n")

    file.close()


def get_next_id(contacts):
    highest_id = 0

    for contact in contacts:
        if contact[0].isdigit():
            number = int(contact[0])

            if number > highest_id:
                highest_id = number

    return str(highest_id + 1)


def display_contact(contact):
    print("-" * 35)
    print("ID    :", contact[0])
    print("Name  :", contact[1])
    print("Phone :", contact[2])
    print("Email :", contact[3])


def validate_contact(contacts, name, phone, email, current_id=None):
    if not name or not phone or not email:
        print("Error: All fields are required.")
        return False

    if "|" in name or "|" in phone or "|" in email:
        print("Error: The | character is not allowed.")
        return False

    if not phone.isdigit() or len(phone) != 10:
        print("Error: Phone number must contain exactly 10 digits.")
        return False

    if "@" not in email or "." not in email:
        print("Error: Please enter a valid-looking email address.")
        return False

    for contact in contacts:
        if contact[0] != current_id:
            if contact[1].lower() == name.lower():
                print("Error: Contact name already exists.")
                return False

            if contact[2] == phone:
                print("Error: Phone number already exists.")
                return False

            if contact[3].lower() == email.lower():
                print("Error: Email already exists.")
                return False

    return True


def add_contact(contacts):
    print("\n--- Add Contact ---")

    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()

    if not validate_contact(contacts, name, phone, email):
        return

    contact_id = get_next_id(contacts)
    contacts.append([contact_id, name, phone, email])

    save_contacts(contacts)
    print("Contact added successfully!")


def view_contacts(contacts):
    print("\n--- View Contacts ---")

    if not contacts:
        print("No contacts found.")
        return

    for contact in contacts:
        display_contact(contact)

    print("-" * 35)
    print("Total contacts:", len(contacts))


def search_contact(contacts):
    print("\n--- Search Contact ---")
    print("1. Search by name")
    print("2. Search by phone number")

    choice = input("Enter your choice: ").strip()

    if choice not in ("1", "2"):
        print("Invalid choice.")
        return

    search_value = input("Enter search value: ").strip().lower()

    if not search_value:
        print("Search value cannot be empty.")
        return

    found = False

    for contact in contacts:
        if choice == "1" and search_value in contact[1].lower():
            display_contact(contact)
            found = True

        elif choice == "2" and search_value in contact[2]:
            display_contact(contact)
            found = True

    if not found:
        print("Contact not found.")


def edit_contact(contacts):
    print("\n--- Edit Contact ---")

    contact_id = input("Enter contact ID to edit: ").strip()

    if not contact_id:
        print("Contact ID cannot be empty.")
        return

    for contact in contacts:
        if contact[0] == contact_id:
            print("\nCurrent contact:")
            display_contact(contact)

            name = input("Enter new name: ").strip()
            phone = input("Enter new phone number: ").strip()
            email = input("Enter new email: ").strip()

            if not validate_contact(
                contacts, name, phone, email, current_id=contact_id
            ):
                return

            contact[1] = name
            contact[2] = phone
            contact[3] = email

            save_contacts(contacts)
            print("Contact updated successfully!")
            return

    print("Contact ID not found.")


def delete_contact(contacts):
    print("\n--- Delete Contact ---")

    contact_id = input("Enter contact ID to delete: ").strip()

    if not contact_id:
        print("Contact ID cannot be empty.")
        return

    for contact in contacts:
        if contact[0] == contact_id:
            print("\nContact to delete:")
            display_contact(contact)

            confirm = input(
                "Confirm deletion? (yes/no): "
            ).strip().lower()

            if confirm == "yes":
                contacts.remove(contact)
                save_contacts(contacts)
                print("Contact deleted successfully!")
            else:
                print("Deletion cancelled.")

            return

    print("Contact ID not found.")


def main():
    contacts = load_contacts()

    while True:
        print("\n========== CONTACT BOOK ==========")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Edit Contact")
        print("5. Delete Contact")
        print("6. Exit")
        print("==================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_contact(contacts)

        elif choice == "2":
            view_contacts(contacts)

        elif choice == "3":
            search_contact(contacts)

        elif choice == "4":
            edit_contact(contacts)

        elif choice == "5":
            delete_contact(contacts)

        elif choice == "6":
            save_contacts(contacts)
            print("Contacts saved. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1 to 6.")


if __name__ == "__main__":
    main()
