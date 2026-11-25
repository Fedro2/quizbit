from storage import _validate_pair


def choose_question_index(questions):
    if not questions:
        print("No questions available.")
        return None

    for number, pair in enumerate(questions, start=1):
        print(f"{number}. {pair['question']} - {pair['answer']}")

    while True:
        choice = input("Select a question (0 to cancel): ")

        if choice == "0":
            return None

        if choice.isdigit():
            index = int(choice) - 1

            if 0 <= index < len(questions):
                return index

        print("Invalid selection. Try again.")


def edit_question(current_set):
    questions = current_set["questions"]
    index = choose_question_index(questions)

    if index is None:
        return

    while True:
        question = input("Enter new question: ")
        answer = input("Enter new answer: ")

        try:
            pair = _validate_pair(question, answer)
        except ValueError as error:
            print(error)
            continue

        questions[index] = pair
        current_set["has_unsaved_changes"] = True

        print("Question and answer updated successfully.")
        return