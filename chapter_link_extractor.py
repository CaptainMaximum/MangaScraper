import bs4, re, sys

def extract_chapters(soup, chapters):
    all_chapters = soup.find_all('a', class_ = "chapter_link")
    all_chapters = [re.sub("\.\.|&page=1", "", x['href']) for x in all_chapters]
    chapter_sub = re.sub("&chapter=[^&]+", "&chapter=@@@", all_chapters[0])
    selected_chapters = [re.sub("@@@", str(x), chapter_sub) for x in chapters]
    return selected_chapters

def main():
    page_contents = sys.stdin.read()
    chapter_string = sys.argv[1]
    chapters = chapter_string.split(" ")
    chapters = [x for x in chapters if x != ""]
    soup = bs4.BeautifulSoup(page_contents)
    chapters = extract_chapters(soup, chapters)
    chapter_links = ["mangasee.co" + x for x in chapters]
    for x in chapter_links:
        print x
    print "\n"

if __name__ == "__main__":
    main()