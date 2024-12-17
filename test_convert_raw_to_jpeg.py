import os
import unittest
from unittest.mock import patch, MagicMock, mock_open
import shutil
import tempfile
import rawpy
import imageio
from convert_raw_to_jpeg import is_raw_file, process_raw_file, scan_and_process_directory

class TestRawToJpegConverter(unittest.TestCase):
    def setUp(self):
        """
        Setup temporary directories for testing.
        """
        self.source_dir = tempfile.mkdtemp()
        self.target_dir = tempfile.mkdtemp()
        
        # Replace global directories for tests
        global source_dir, target_dir
        source_dir = self.source_dir
        target_dir = self.target_dir

    def tearDown(self):
        """
        Cleanup temporary directories after tests.
        """
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.target_dir)

    def test_is_raw_file(self):
        """
        Test the is_raw_file function to check supported RAW file extensions.
        """
        self.assertTrue(is_raw_file("image1.arw"))
        self.assertTrue(is_raw_file("image2.dng"))
        self.assertTrue(is_raw_file("image3.gpr"))
        self.assertFalse(is_raw_file("image4.jpg"))
        self.assertFalse(is_raw_file("image5.txt"))

    @patch('rawpy.imread')
    @patch('imageio.imsave')
    def test_process_raw_file(self, mock_imsave, mock_rawpy):
        """
        Test the process_raw_file function for RAW to JPEG conversion.
        """
        # Create a mock RAW file in the source directory
        raw_file = os.path.join(self.source_dir, "test_image.arw")
        with open(raw_file, "w") as f:
            f.write("fake RAW data")

        # Mock rawpy and imageio behavior
        mock_raw_instance = MagicMock()
        mock_rawpy.return_value.__enter__.return_value = mock_raw_instance
        mock_raw_instance.postprocess.return_value = "mock RGB data"

        # Run the function
        process_raw_file(raw_file)

        # Verify that imageio.imsave was called with the correct output path
        expected_output_path = os.path.join(self.target_dir, "test_image.jpeg")
        mock_imsave.assert_called_once_with(expected_output_path, "mock RGB data")
        print("✅ process_raw_file test passed.")

    def test_scan_and_process_directory_no_files(self):
        """
        Test scan_and_process_directory when no RAW files exist.
        """
        with patch('builtins.print') as mock_print:
            scan_and_process_directory()
            mock_print.assert_any_call("✨ No new files to convert. All files are up-to-date.")
        print("✅ scan_and_process_directory with no files test passed.")

    @patch('convert_raw_to_jpeg.process_raw_file')
    def test_scan_and_process_directory_with_files(self, mock_process_raw_file):
        """
        Test scan_and_process_directory when RAW files are present.
        """
        # Create RAW files in the source directory
        raw_files = ["image1.arw", "image2.dng"]
        for file in raw_files:
            with open(os.path.join(self.source_dir, file), "w") as f:
                f.write("fake RAW data")

        # Run the function
        scan_and_process_directory()

        # Verify process_raw_file is called for each RAW file
        self.assertEqual(mock_process_raw_file.call_count, len(raw_files))
        print("✅ scan_and_process_directory with files test passed.")

    def test_target_directory_creation(self):
        """
        Test that the target directory is created if it doesn't exist.
        """
        shutil.rmtree(self.target_dir)  # Remove target directory
        self.assertFalse(os.path.exists(self.target_dir))

        # Run scan_and_process_directory
        scan_and_process_directory()

        # Check if target directory is created
        self.assertTrue(os.path.exists(self.target_dir))
        print("✅ Target directory creation test passed.")

if __name__ == "__main__":
    unittest.main()
