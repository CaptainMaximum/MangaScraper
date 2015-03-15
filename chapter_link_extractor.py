import bs4, re, sys

# Takes a BeautifulSoup object and a list of chapters and gets the chapter urls
# for that list
def extract_chapters(soup, chapters):
    all_chapters = soup.find_all('a', class_ = "chapter_link")
    all_chapters = [re.sub("\.\.|&page=1", "", x['href']) for x in all_chapters]
    chapter_sub = re.sub("&chapter=[^&]+", "&chapter=@@@", all_chapters[0])
    selected_chapters = [re.sub("@@@", str(x), chapter_sub) for x in chapters]
    return selected_chapters

# 
def get_chapters(_input = sys.argv):
    chapter_string = _input[1]
    chapters = chapter_string.split(" ")
    chapters = filter(lambda x: x != "", chapters)
    return chapters

def get_chapter_links(chapters):
    links = ["mangasee.co" + x for x in chapters]
    links_string = " ".join(links)
    links_string = "'%s'" % links_string
    return links_string

def print_for_capture(chap_list):
    print "CHAPTERS=" + chap_list

def main():
    page_contents = sys.stdin.read()
    chapters = get_chapters()
    soup = bs4.BeautifulSoup(page_contents)
    chapters = extract_chapters(soup, chapters)
    chapter_links = get_chapter_links(chapters)
    print_for_capture(chapter_links)

if __name__ == "__main__":
    main()