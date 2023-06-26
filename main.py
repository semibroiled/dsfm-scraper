import filter_text
import scraper
import compare


def main():
    # Load and parse Comparison tags
    with open("tags.txt", "r") as tags:
        tag = tags.read()
        print(tag)

    tags = filter_text.filter_pipeline(tag)
    print(tags)

    # Scrape URLs for texts
    url_lst = scraper.read_urls_from_file()

    # Iterate over urls to get text to compare against
    all_text = []
    for url in url_lst:
        if "html" or "pdf" in url.lower():
            read_from_url = scraper.scrape_stat_url(url)
        else:
            try:
                read_from_url = scraper.scrape_dyn_url(url)
            except:
                print("Error")

        filter_read_from_url = filter_text.filter_pipeline(read_from_url)
        all_text += filter_read_from_url

    print(all_text)

    # Compare the two lists and check the dict
    # Plot in plt/pandas
    comparison = compare.compare_lists(all_text, tags)

    compare.plot_keyword_mentions(comparison)

    # TODO_add cli and caching
    None


if __name__ == "__main__":
    main()
