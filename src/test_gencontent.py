import unittest
from gencontent import extract_title

class test_extract_title(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# My Title\n\nThis is some content."
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")
    
    def test_extract_title_missing_h1(self):
        markdown = "## My Title\n\nThis is some content"
        with self.assertRaises(Exception):
            extract_title(markdown)
            
if __name__ == "__main__":
    unittest.main()


    