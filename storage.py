"""Read, import and save Quizbit learning sets as CSV files."""

import csv
import os
import tempfile
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
    """Load a saved set, retaining its path for a later Save action."""
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


def import_learning_set(source_path):
    """Import a CSV without keeping its source path as a save target."""
    learning_set = load_learning_set(source_path)
    learning_set["file_path"] = None
    learning_set["has_unsaved_changes"] = True
    return learning_set


def _prepare_questions(questions):
    if not isinstance(questions, list) or not questions:
        raise ValueError("An empty learning set cannot be saved.")

    clean_pairs = []
    for pair in questions:
        if not isinstance(pair, dict):
            raise ValueError("Each question-answer pair must be a dictionary.")
        clean_pairs.append(
            _validate_pair(pair.get("question"), pair.get("answer"))
        )
    return clean_pairs


def _get_save_path(learning_set, sets_folder):
    folder = Path(sets_folder).resolve()
    name = _validate_name(learning_set.get("name"))
    current_path = learning_set.get("file_path")

    if current_path is None:
        target = folder / f"{name}.csv"
    else:
        target = Path(current_path).resolve()
        if target.parent != folder:
            raise ValueError("Import external sets before saving them.")
        if (
            target.suffix.casefold() != ".csv"
            or target.stem.casefold() != name.casefold()
        ):
            raise ValueError("The set name must match its saved file.")

    for existing in list_saved_sets(folder):
        if existing.stem.casefold() == name.casefold():
            if current_path is None or existing.resolve() != target:
                raise ValueError("A saved set already uses this name.")

    if current_path is None and target.exists():
        raise ValueError("The destination is already in use.")
    return target


def _write_questions(target, questions):
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=target.parent,
            prefix=".quizbit-",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_path = Path(file.name)
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(questions)

        # Keep the old file until the complete replacement has been written.
        os.replace(temporary_path, target)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def save_learning_set(learning_set, sets_folder):
    """Save a valid set and update its metadata only after success."""
    questions = _prepare_questions(learning_set.get("questions"))
    target = _get_save_path(learning_set, sets_folder)
    _write_questions(target, questions)

    learning_set["name"] = target.stem
    learning_set["questions"] = questions
    learning_set["file_path"] = target
    learning_set["has_unsaved_changes"] = False
    return target
