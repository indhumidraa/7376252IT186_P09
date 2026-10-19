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


def add_contact(contacts):
    print("\n--- Add Contact ---")

    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()

    if not name or not phone or not email:
        print("All fields are required.")
        return

    for contact in contacts:
        if contact[2] == phone:
            print("Phone number already exists.")
            return

    contact_id = str(len(contacts) + 1)

    contact = [contact_id, name, phone, email]
    contacts.append(contact)

    save_contacts(contacts)
    print("Contact added successfully!")


def view_contacts(contacts):
    print("\n--- Contact List ---")

    if not contacts:
        print("No contacts found.")
        return

    for contact in contacts:
        print("-" * 30)
        print("ID    :", contact[0])
        print("Name  :", contact[1])
        print("Phone :", contact[2])
        print("Email :", contact[3])


def main():
    contacts = load_contacts()

    while True:
        print("\n===== CONTACT BOOK =====")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_contact(contacts)

        elif choice == "2":
            view_contacts(contacts)

        elif choice == "3":
            save_contacts(contacts)
            print("Contacts saved. Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


main()
