from datetime import datetime, timedelta
import json
import os


class Note:
    def __init__(self, note_id, title, body):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at

    def update(self, title, body):
        self.title = title
        self.body = body
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class NoteManager:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def load_notes(self):
        if os.path.exists("notes.json"):
            with open("notes.json", "r") as file:
                notes_data = json.load(file)
                for note_data in notes_data:
                    note = Note(note_data['note_id'],
                                note_data['title'], note_data['body'])
                    note.created_at = note_data['created_at']
                    note.updated_at = note_data['updated_at']
                    self.notes.append(note)

    def save_notes(self):
        notes_data = []
        for note in self.notes:
            notes_data.append({
                'note_id': note.note_id,
                'title': note.title,
                'body': note.body,
                'created_at': note.created_at,
                'updated_at': note.updated_at
            })
        with open("notes.json", "w") as file:
            json.dump(notes_data, file, indent=4)

    def add_note(self, title, body):
        note_id = len(self.notes) + 1
        note = Note(note_id, title, body)
        self.notes.append(note)
        self.save_notes()

    def edit_note(self, note_id, title, body):
        for note in self.notes:
            if note.note_id == note_id:
                note.update(title, body)
                self.save_notes()
                return True
        return False

    def delete_note(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                self.notes.remove(note)
                self.save_notes()
                return True
        return False

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                return note
        return None

    def get_all_notes(self):
        return self.notes

    def get_notes_by_date(self, date_str):
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            notes_on_date = [note for note in self.notes if datetime.strptime(
                note.created_at, "%Y-%m-%d %H:%M:%S").date() == target_date.date()]
            return notes_on_date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return []


def print_notes(notes):
    for note in notes:
        print(
            f"ID: {note.note_id}, Title: {note.title}, Created At: {note.created_at}")


def read_full_note(note_manager):
    note_id = int(input("Enter note ID to read: "))
    note = note_manager.get_note_by_id(note_id)
    if note:
        print(
            f"ID: {note.note_id}, Title: {note.title}, Body: {note.body}, Created At: {note.created_at}")
    else:
        print("Note not found.")


def edit_note(note_manager, note_id, title, body):
    note = note_manager.get_note_by_id(note_id)
    if note:
        note_manager.edit_note(note_id, title, body)
        print("Note edited successfully.")
    else:
        print("Note not found.")


def delete_note_and_reassign_ids(note_manager, note_id):
    if note_manager.delete_note(note_id):
        for index, note in enumerate(note_manager.notes):
            note.note_id = index + 1
        note_manager.save_notes()
        print("Note deleted successfully.")
    else:
        print("Note not found.")


def main():
    note_manager = NoteManager()
    while True:
        print("\n1. Create Note")
        print("2. Edit Note")
        print("3. Delete Note")
        print("4. List All Notes")
        print("5. Filter Notes by Date")
        print("6. Read Full Note")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter note title: ")
            body = input("Enter note body: ")
            note_manager.add_note(title, body)
            print("Note created successfully.")

        elif choice == "2":
            note_id = int(input("Enter note ID to edit: "))
            note = note_manager.get_note_by_id(note_id)
            if note:
                title = input("Enter new title: ")
                body = input("Enter new body: ")
                edit_note(note_manager, note_id, title, body)
            else:
                print("Note not found.")

        elif choice == "3":
            note_id = int(input("Enter note ID to delete: "))
            delete_note_and_reassign_ids(note_manager, note_id)

        elif choice == "4":
            notes = note_manager.get_all_notes()
            print_notes(notes)

        elif choice == "5":
            date_str = input("Enter date to filter notes (YYYY-MM-DD): ")
            notes = note_manager.get_notes_by_date(date_str)
            print_notes(notes)

        elif choice == "6":
            read_full_note(note_manager)

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
