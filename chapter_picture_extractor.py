import bs4, re, sys

def get_images(soup):
    # This may need to change if mangasee changes the way that pictures are presented in html
    images = soup.select("p img")

    return [x['src'] for x in images]

def main():
    page_contents = sys.stdin.read()
    soup = bs4.BeautifulSoup(page_contents)
    images = get_images(soup)
    for x in images:
        print x

if __name__ == "__main__":
    main()