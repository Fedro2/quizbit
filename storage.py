"""Find and load Quizbit learning sets from CSV files."""

import csv
from pathlib import Path


CSV_FIELDS = ["question", "answer"]
RESERVED_ANSWERS = {"/quit", "/restart"}


def list_saved_sets(sets_folder):
    """Return the CSV file paths in the saved-sets folder."""
    folder = Path(sets_folder)
    if not folder.exists():
        return []

    paths = []
    for path in folder.iterdir():
        if path.is_file() and path.suffix.casefold() == ".csv":
            paths.append(path)
    return paths


def _validate_name(name):
    if not isinstance(name, str):
        raise ValueError("The learning set needs a name.")

    name = name.strip()
    if not name or "/" in name or "\\" in name:
        raise ValueError(
            "Set names cannot be empty or contain path separators."
        )
    return name


def _validate_pair(question, answer):
    if not isinstance(question, str) or not isinstance(answer, str):
        raise ValueError("Each row needs a question and an answer.")

    question = question.strip()
    answer = answer.strip()
    if not question or not answer:
        raise ValueError("Questions and answers cannot be empty.")
    if answer.casefold() in RESERVED_ANSWERS:
        raise ValueError("/quit and /restart cannot be stored as answers.")

    return {"question": question, "answer": answer}


def _read_questions(file_path):
    questions = []
    try:
        with file_path.open(
            "r", encoding="utf-8-sig", newline=""
        ) as file:
            reader = csv.DictReader(file, strict=True)
            if reader.fieldnames != CSV_FIELDS:
                raise ValueError("The CSV header must be question,answer.")

            for number, row in enumerate(reader, start=1):
                if None in row:
                    raise ValueError(f"Record {number} has extra columns.")
                try:
                    pair = _validate_pair(row["question"], row["answer"])
                except ValueError as error:
                    raise ValueError(f"Record {number}: {error}") from error
                questions.append(pair)
    except (UnicodeError, csv.Error) as error:
        raise ValueError(
            "The file must contain valid UTF-8 CSV data."
        ) from error

    if not questions:
        raise ValueError("The learning set contains no questions.")
    return questions


def load_learning_set(path):
    """Load and validate a saved learning set."""
    file_path = Path(path).resolve()
    if file_path.suffix.casefold() != ".csv":
        raise ValueError("Select a CSV file.")

    name = _validate_name(file_path.stem)
    questions = _read_questions(file_path)
    return {
        "name": name,
        "questions": questions,
        "file_path": file_path,
        "has_unsaved_changes": False,
    }
