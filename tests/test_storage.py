from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from storage import list_saved_sets, load_learning_set


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name).resolve()
        self.folder = self.root / "sets"

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


if __name__ == "__main__":
    unittest.main()
