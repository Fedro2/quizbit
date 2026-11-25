import csv
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from storage import (
    import_learning_set,
    list_saved_sets,
    load_learning_set,
    save_learning_set,
)


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name).resolve()
        self.folder = self.root / "sets"

    def new_set(self, name="Python"):
        return {
            "name": name,
            "questions": [
                {"question": "Display text?", "answer": "print"},
                {"question": "Read input?", "answer": "input"},
            ],
            "file_path": None,
            "has_unsaved_changes": True,
        }

    def write_csv(self, name, text, encoding="utf-8"):
        path = self.root / name
        path.write_text(text, encoding=encoding)
        return path

    def test_missing_and_empty_folders_have_no_sets(self):
        self.assertEqual(list_saved_sets(self.folder), [])
        self.assertFalse(self.folder.exists())
        self.folder.mkdir()
        self.assertEqual(list_saved_sets(self.folder), [])

    def test_listing_contains_only_csv_files(self):
        self.folder.mkdir()
        lower = self.folder / "python.csv"
        upper = self.folder / "maths.CSV"
        lower.write_text("question,answer\nQ,A\n")
        upper.write_text("question,answer\nQ,A\n")
        (self.folder / "notes.txt").write_text("notes")
        (self.folder / ".quizbit-pending.tmp").write_text("temporary")
        (self.folder / "nested.csv").mkdir()
        self.assertCountEqual(list_saved_sets(self.folder), [lower, upper])

    def test_listing_a_file_instead_of_folder_reports_oserror(self):
        path = self.write_csv("file.csv", "question,answer\nQ,A\n")
        with self.assertRaises(OSError):
            list_saved_sets(path)

    def test_save_and_load_preserve_csv_content(self):
        learning_set = self.new_set()
        learning_set["questions"] = [
            {"question": '  A comma, a "quote" and ä?  ', "answer": "  Ö  "},
            {"question": "First line\nsecond line?", "answer": "yes"},
        ]
        path = save_learning_set(learning_set, self.folder)
        expected = [
            {"question": 'A comma, a "quote" and ä?', "answer": "Ö"},
            {"question": "First line\nsecond line?", "answer": "yes"},
        ]
        self.assertEqual(path, self.folder / "Python.csv")
        self.assertEqual(learning_set["questions"], expected)
        self.assertEqual(learning_set["file_path"], path)
        self.assertFalse(learning_set["has_unsaved_changes"])
        self.assertEqual(load_learning_set(path), learning_set)
        with path.open(encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            self.assertEqual(reader.fieldnames, ["question", "answer"])

    def test_loaded_set_can_update_its_existing_file(self):
        path = save_learning_set(self.new_set(), self.folder)
        loaded = load_learning_set(path)
        loaded["questions"][0] = {"question": "Changed?", "answer": "yes"}
        loaded["has_unsaved_changes"] = True
        self.assertEqual(save_learning_set(loaded, self.folder), path)
        self.assertEqual(load_learning_set(path)["questions"][0], {
            "question": "Changed?", "answer": "yes"
        })
        self.assertFalse(loaded["has_unsaved_changes"])

    def test_case_insensitive_name_conflict_preserves_existing_file(self):
        path = save_learning_set(self.new_set(), self.folder)
        old_content = path.read_bytes()
        for name in ["Python", "pYtHoN", "  PYTHON  "]:
            with self.subTest(name=name):
                new_set = self.new_set(name)
                before = deepcopy(new_set)
                with self.assertRaises(ValueError):
                    save_learning_set(new_set, self.folder)
                self.assertEqual(path.read_bytes(), old_content)
                self.assertEqual(new_set, before)

    def test_invalid_names_are_rejected_before_creating_storage(self):
        for name in ["", "   ", "a/b", "a\\b", None]:
            with self.subTest(name=name):
                learning_set = self.new_set(name)
                before = deepcopy(learning_set)
                with self.assertRaises(ValueError):
                    save_learning_set(learning_set, self.folder)
                self.assertEqual(learning_set, before)
                self.assertFalse(self.folder.exists())

    def test_empty_or_invalid_questions_cannot_overwrite_a_saved_set(self):
        path = save_learning_set(self.new_set(), self.folder)
        old_content = path.read_bytes()
        invalid_questions = [
            [],
            None,
            ["not a pair"],
            [{"question": "Q"}],
            [{"question": "Q", "answer": "  "}],
            [{"question": " ", "answer": "A"}],
            [{"question": "Q", "answer": " /QUIT "}],
            [{"question": "Q", "answer": "/restart"}],
        ]
        for questions in invalid_questions:
            with self.subTest(questions=questions):
                loaded = load_learning_set(path)
                loaded["questions"] = questions
                loaded["has_unsaved_changes"] = True
                before = deepcopy(loaded)
                with self.assertRaises(ValueError):
                    save_learning_set(loaded, self.folder)
                self.assertEqual(path.read_bytes(), old_content)
                self.assertEqual(loaded, before)

    def test_io_failures_preserve_old_file_and_unsaved_changes(self):
        path = save_learning_set(self.new_set(), self.folder)
        old_content = path.read_bytes()
        failures = ["storage.os.replace", "storage.csv.DictWriter.writerows"]
        for failure in failures:
            with self.subTest(failure=failure):
                loaded = load_learning_set(path)
                loaded["questions"].append({
                    "question": "New question?", "answer": "yes"
                })
                loaded["has_unsaved_changes"] = True
                before = deepcopy(loaded)
                with patch(failure, side_effect=OSError("Cannot write")):
                    with self.assertRaises(OSError):
                        save_learning_set(loaded, self.folder)
                self.assertEqual(path.read_bytes(), old_content)
                self.assertEqual(loaded, before)
                self.assertEqual(list(self.folder.glob(".quizbit-*.tmp")), [])

    def test_invalid_csv_files_are_rejected(self):
        invalid_files = [
            "",
            "question,answer\n",
            "Question,Answer\nQ,A\n",
            "question;answer\nQ;A\n",
            "question,answer,extra\nQ,A,X\n",
            "question,answer\nQ\n",
            "question,answer\nQ,A,X\n",
            "question,answer\nQ, \n",
            "question,answer\n ,A\n",
            "question,answer\nQ,/RESTART\n",
            'question,answer\n"unclosed quote,A\n',
            "question,answer\nValid,yes\nIncomplete\n",
        ]
        for index, text in enumerate(invalid_files):
            with self.subTest(index=index):
                path = self.write_csv(f"invalid-{index}.csv", text)
                before = path.read_bytes()
                with self.assertRaises(ValueError):
                    load_learning_set(path)
                self.assertEqual(path.read_bytes(), before)

    def test_bom_and_uppercase_extension_are_supported(self):
        path = self.write_csv(
            "German.CSV", "question,answer\nÄ,Ö\n", encoding="utf-8-sig"
        )
        loaded = load_learning_set(path)
        self.assertEqual(
            loaded["questions"], [{"question": "Ä", "answer": "Ö"}]
        )
        self.assertEqual(loaded["file_path"], path)
        self.assertFalse(loaded["has_unsaved_changes"])

    def test_invalid_encoding_is_reported_as_invalid_data(self):
        path = self.root / "invalid.csv"
        path.write_bytes(b"question,answer\nQ,\xff\n")
        with self.assertRaises(ValueError):
            load_learning_set(path)

    def test_missing_or_unreadable_file_reports_oserror(self):
        with self.assertRaises(OSError):
            load_learning_set(self.root / "missing.csv")
        path = self.write_csv("unreadable.csv", "question,answer\nQ,A\n")
        with patch.object(Path, "open", side_effect=PermissionError("Denied")):
            with self.assertRaises(OSError):
                load_learning_set(path)

    def test_non_csv_file_is_rejected(self):
        path = self.write_csv("notes.txt", "question,answer\nQ,A\n")
        with self.assertRaises(ValueError):
            load_learning_set(path)

    def test_import_stays_in_memory_and_leaves_source_unchanged(self):
        source = self.write_csv("External.csv", "question,answer\nQ,A\n")
        old_content = source.read_bytes()
        imported = import_learning_set(source)
        self.assertIsNone(imported["file_path"])
        self.assertTrue(imported["has_unsaved_changes"])
        self.assertFalse(self.folder.exists())
        target = save_learning_set(imported, self.folder)
        self.assertEqual(target, self.folder / "External.csv")
        self.assertEqual(source.read_bytes(), old_content)
        self.assertEqual(load_learning_set(target)["questions"], [
            {"question": "Q", "answer": "A"}
        ])

    def test_import_name_conflict_can_be_resolved_without_data_loss(self):
        existing_path = save_learning_set(self.new_set(), self.folder)
        old_content = existing_path.read_bytes()
        source = self.write_csv("Python.csv", "question,answer\nOther?,yes\n")
        source_content = source.read_bytes()
        imported = import_learning_set(source)
        before = deepcopy(imported)
        with self.assertRaises(ValueError):
            save_learning_set(imported, self.folder)
        self.assertEqual(imported, before)
        self.assertEqual(existing_path.read_bytes(), old_content)
        imported["name"] = "Imported Python"
        saved = save_learning_set(imported, self.folder)
        self.assertEqual(saved, self.folder / "Imported Python.csv")
        self.assertEqual(source.read_bytes(), source_content)

    def test_external_loaded_path_is_not_used_as_save_destination(self):
        source = self.write_csv("External.csv", "question,answer\nQ,A\n")
        before = source.read_bytes()
        loaded = load_learning_set(source)
        with self.assertRaises(ValueError):
            save_learning_set(loaded, self.folder)
        self.assertEqual(source.read_bytes(), before)
        self.assertFalse(self.folder.exists())

    def test_saved_file_cannot_be_renamed_through_its_name_field(self):
        path = save_learning_set(self.new_set(), self.folder)
        old_content = path.read_bytes()
        loaded = load_learning_set(path)
        loaded["name"] = "Another name"
        loaded["has_unsaved_changes"] = True
        before = deepcopy(loaded)
        with self.assertRaises(ValueError):
            save_learning_set(loaded, self.folder)
        self.assertEqual(path.read_bytes(), old_content)
        self.assertEqual(loaded, before)

    def test_an_existing_destination_directory_is_not_overwritten(self):
        self.folder.mkdir()
        occupied = self.folder / "Python.csv"
        occupied.mkdir()
        with self.assertRaises(ValueError):
            save_learning_set(self.new_set(), self.folder)
        self.assertTrue(occupied.is_dir())

    def test_identical_question_rows_are_preserved(self):
        learning_set = self.new_set()
        pair = {"question": "Same question?", "answer": "yes"}
        learning_set["questions"] = [dict(pair), dict(pair)]
        path = save_learning_set(learning_set, self.folder)
        self.assertEqual(load_learning_set(path)["questions"], [pair, pair])


if __name__ == "__main__":
    unittest.main()
