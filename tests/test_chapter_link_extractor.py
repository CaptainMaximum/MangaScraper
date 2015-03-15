import bs4, unittest
from chapter_link_extractor import *

class TestExtractorFunctions(unittest.TestCase):
    def setUp(self):
        self.test_page = "tests/test_files/TestPage.htm"
        self.page_contents = open(self.test_page).read()

    def test_get_chapters(self):
        expected = ["1", "2", "3", "4"]
        observed = get_chapters(["script_name.py", "1 2 3 4"])
        self.assertEqual(expected, observed)

    def test_extract_chapters(self):
        soup = bs4.BeautifulSoup(self.page_contents)
        expected = [ "/manga/?series=ComicName&chapter=1&index=1", 
            "/manga/?series=ComicName&chapter=2&index=1", 
            "/manga/?series=ComicName&chapter=3&index=1" ]
        observed = extract_chapters(soup, ["1", "2", "3"])
        self.assertEqual(expected, observed)

    def test_get_chapter_links(self):
        expected = ["mangasee.co/chap1", "mangasee.co/chap2"]
        observed = get_chapter_links(["/chap1", "/chap2"])
        self.assertEqual(expected, observed)

if __name__ == "__main__":
    unittest.main()