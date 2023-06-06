import unittest
import unittest.mock
from pathlib import Path
from tempfile import TemporaryDirectory

from pyautoreloadserver import FileObserver


class FileObserverTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name)
        self.observer = FileObserver(self.root_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_scan_existing_files(self):
        # Create some files
        file1 = self.root_path / "file1.txt"
        file1.touch()
        file2 = self.root_path / "dir1" / "file2.txt"
        file2.parent.mkdir(parents=True, exist_ok=True)
        file2.touch()

        # Scan for files
        files = list(self.observer.scan())

        # Verify scanned files
        expected_files = [file1, file2]
        self.assertEqual(sorted(files), sorted(expected_files))

    def test_observe_new_file(self):
        # Create a new file
        new_file = self.root_path / "new_file.txt"
        new_file.touch()

        # Observe for changes
        changed_files = self.observer.observe()

        # Verify changed files
        expected_files = [new_file]
        self.assertEqual(changed_files, expected_files)

    def test_observe_added_file(self):
        # Observe for changes
        changed_files = self.observer.observe()
        self.assertEqual(changed_files, [])

        # Create an existing file
        existing_file = self.root_path / "existing_file.txt"
        existing_file.touch()

        # Modify the file
        existing_file.write_text("Modified content")

        # Observe for changes
        changed_files = self.observer.observe()

        # Verify changed files
        expected_files = [existing_file]
        self.assertEqual(changed_files, expected_files)

    def test_observe_modified_file(self):
        # Create an existing file
        existing_file = self.root_path / "existing_file.txt"
        existing_file.touch()

        # Write to the file
        existing_file.write_text("Content")

        # Observe for changes
        changed_files = self.observer.observe()

        # Verify changed files
        expected_files = [existing_file]
        self.assertEqual(changed_files, expected_files)

        existing_file.write_text("More text")

        with unittest.mock.patch("os.path.getmtime") as mock_getmtime:
            mock_getmtime.return_value = 10e10
            # Observe for changes
            changed_files = self.observer.observe()

        # Verify changed files
        expected_files = [existing_file]
        self.assertEqual(changed_files, expected_files)
        mock_getmtime.assert_called()

    def test_observe_no_changes(self):
        # Observe for changes
        changed_files = self.observer.observe()

        # Verify no changes
        self.assertEqual(changed_files, [])

    def test_observe_subdirectories(self):
        # Create some files in subdirectories
        file1 = self.root_path / "dir1" / "file1.txt"
        file1.parent.mkdir(parents=True, exist_ok=True)
        file1.touch()
        file2 = self.root_path / "dir2" / "file2.txt"
        file2.parent.mkdir(parents=True, exist_ok=True)
        file2.touch()

        # Observe for changes
        changed_files = self.observer.observe()

        # Verify changed files
        expected_files = [file1, file2]
        self.assertEqual(sorted(changed_files), sorted(expected_files))


if __name__ == "__main__":
    unittest.main()
