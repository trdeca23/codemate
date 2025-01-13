import unittest
from utils import *
from pathlib import Path

class TestUtils(unittest.TestCase):

    def test_get_structure_in_target_dir(self):
        structure = get_structure_in_target_dir(recursive=False)
        self.assertIsInstance(structure, dict)
        # Add more assertions based on expected structure

    def test_read_all_files_in_target_dir(self):
        files = read_all_files_in_target_dir()
        self.assertIsInstance(files, dict)
        # Add more assertions based on expected file contents

    def test_read_file_in_target_dir(self):
        content = read_file_in_target_dir('README.md')
        self.assertIsInstance(content, str)
        self.assertIn('# Gemini Utilities Library', content)  # Check for a specific string in README

    def test_write_file_in_target_dir(self):
        test_content = 'This is a test file.'
        result = write_file_in_target_dir('test.txt', test_content)
        self.assertEqual(result, 'File written successfully.')
        retrieved_content = read_file_in_target_dir('test.txt')
        self.assertEqual(retrieved_content, test_content)
        delete_file_in_target_dir('test.txt') #cleanup


    def test_make_directory_in_target_dir(self):
        result = make_directory_in_target_dir('test_dir')
        self.assertEqual(result, {'status': 'success'})
        self.assertTrue(Path('test_dir').exists())
        delete_file_in_target_dir('test_dir') #cleanup


    def test_delete_file_in_target_dir(self):
        write_file_in_target_dir('to_delete.txt', 'content')
        result = delete_file_in_target_dir('to_delete.txt')
        self.assertEqual(result, {'status': 'success'})
        self.assertFalse(Path('to_delete.txt').exists())

    def test_move_file_in_target_dir(self):
        write_file_in_target_dir('to_move.txt', 'content')
        result = move_file_in_target_dir('to_move.txt', 'moved.txt')
        self.assertEqual(result, {'status': 'success'})
        self.assertTrue(Path('moved.txt').exists())
        self.assertFalse(Path('to_move.txt').exists())
        delete_file_in_target_dir('moved.txt') #cleanup


    def test_copy_file_in_target_dir(self):
        write_file_in_target_dir('to_copy.txt', 'content')
        result = copy_file_in_target_dir('to_copy.txt', 'copied.txt')
        self.assertEqual(result, {'status': 'success'})
        self.assertTrue(Path('copied.txt').exists())
        self.assertTrue(Path('to_copy.txt').exists())
        delete_file_in_target_dir('copied.txt')
        delete_file_in_target_dir('to_copy.txt') #cleanup

    def test_local_code_execution(self):
        result = local_code_execution('print(1+1)')
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['output'], '')


if __name__ == '__main__':
    unittest.main()
