
def load_contacts():
    contacts = []

    try:
        with open("contacts.txt", "r") as file:
            for line in file:
                parts = line.strip().split("|")

                if len(parts) == 3:
                    contacts.append({
                        "name": parts[0],
                        "phone": parts[1],
                        "email": parts[2]
                    })
    except FileNotFoundError:
        with open("contacts.txt", "w") as file:
            pass

    return contacts


def save_contacts(contacts):
    with open("contacts.txt", "w") as file:
        for contact in contacts:
            file.write(
                contact["name"] + "|" +
                contact["phone"] + "|" +
                contact["email"] + "\n"
            )


def get_contact_details():
    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()

    if not name or not phone or not email:
        print("All fields are required.")
        return None

    if "|" in name or "|" in phone or "|" in email:
        print("The | character is not allowed.")
        return None

    if len(phone) != 10 or not phone.isdigit():
        print("Phone number must contain exactly 10 digits.")
        return None

    if "@" not in email or "." not in email:
        print("Enter a valid-looking email address.")
        return None

    return {"name": name, "phone": phone, "email": email}


def add_contact(contacts):
    print("\n--- Add Contact ---")
    contact = get_contact_details()

    if contact is None:
        return

    for existing in contacts:
        if (existing["name"].lower() == contact["name"].lower()
                or existing["phone"] == contact["phone"]
                or existing["email"].lower() == contact["email"].lower()):
            print("Name, phone, or email already exists.")
            return

    contacts.append(contact)
    save_contacts(contacts)
    print("Contact added successfully!")


def view_contacts(contacts):
    print("\n--- Contact List ---")

    if not contacts:
        print("No contacts found.")
        return

    for index, contact in enumerate(contacts, start=1):
        print("-" * 35)
        print("ID    :", index)
        print("Name  :", contact["name"])
        print("Phone :", contact["phone"])
        print("Email :", contact["email"])


def search_contact(contacts):
    print("\n1. Search by name")
    print("2. Search by phone")
    choice = input("Choose: ").strip()

    if choice == "1":
        field = "name"
        value = input("Enter name to search: ").strip().lower()
    elif choice == "2":
        field = "phone"
        value = input("Enter phone to search: ").strip()
    else:
        print("Invalid choice.")
        return

    if not value:
        print("Search value cannot be empty.")
        return

    found = False

    for index, contact in enumerate(contacts, start=1):
        if value in contact[field].lower():
            print("-" * 35)
            print("ID    :", index)
            print("Name  :", contact["name"])
            print("Phone :", contact["phone"])
            print("Email :", contact["email"])
            found = True

    if not found:
        print("Contact not found.")


def edit_contact(contacts):
    view_contacts(contacts)

    if not contacts:
        return

    try:
        contact_id = int(input("Enter contact ID to edit: "))
        if contact_id < 1 or contact_id > len(contacts):
            print("Invalid contact ID.")
            return
    except ValueError:
        print("Enter a valid numeric ID.")
        return

    contact = contacts[contact_id - 1]

    print("\n1. Edit name")
    print("2. Edit phone")
    print("3. Edit email")
    print("4. Edit all details")
    choice = input("Choose what to edit: ").strip()

    if choice == "1":
        value = input("Enter new name: ").strip()
        if not value or "|" in value:
            print("Invalid name.")
            return
        contact["name"] = value

    elif choice == "2":
        value = input("Enter new phone: ").strip()
        if len(value) != 10 or not value.isdigit():
            print("Phone must contain exactly 10 digits.")
            return
        contact["phone"] = value

    elif choice == "3":
        value = input("Enter new email: ").strip()
        if "@" not in value or "." not in value or "|" in value:
            print("Enter a valid-looking email.")
            return
        contact["email"] = value

    elif choice == "4":
        updated = get_contact_details()
        if updated is None:
            return
        contact.update(updated)

    else:
        print("Invalid choice.")
        return

    for index, other in enumerate(contacts):
        if index != contact_id - 1:
            if (other["name"].lower() == contact["name"].lower()
                    or other["phone"] == contact["phone"]
                    or other["email"].lower() == contact["email"].lower()):
                print("Another contact already uses those details.")
                return

    save_contacts(contacts)
    print("Contact updated successfully!")


def delete_contact(contacts):
    view_contacts(contacts)

    if not contacts:
        return

    try:
        contact_id = int(input("Enter contact ID to delete: "))
        if contact_id < 1 or contact_id > len(contacts):
            print("Invalid contact ID.")
            return
    except ValueError:
        print("Enter a valid numeric ID.")
        return

    contact = contacts[contact_id - 1]
    print("Selected contact:", contact["name"], "-", contact["phone"])

    confirm = input("Confirm deletion? (yes/no): ").strip().lower()

    if confirm == "yes":
        contacts.pop(contact_id - 1)
        save_contacts(contacts)
        print("Contact deleted successfully!")
    else:
        print("Deletion cancelled.")


def main():
    contacts = load_contacts()

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
            print("Contacts saved. Goodbye!")
            break
        else:
            print("Invalid choice. Select 1 to 6.")


if __name__ == "__main__":
    main()
