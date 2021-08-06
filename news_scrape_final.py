import requests
import bs4


# Specify topics and optional keyword to check in url
TOPICS = []

TOPIC_PREFIX = ""
SEARCH_TAB = "nws"
SEARCH_ENGINE_URL = "https://google.com"
SEARCH_ENGINE_SOURCE_ID = ""

# Specify groups based on news urls
GROUPS = {
    "washingtonpost.com": "USA", "edition.cnn.com": "USA",
    "nytimes.com": "USA", "bbc.com": "USA", "scmp.com": "ASIA",
    "globaltimes.cn": "ASIA", "chinadaily.com.cn": "ASIA",
    "thediplomat.com": "ASIA"
}
OTHER_GROUP = "OTHERS"

# Increase this number to get more results
RESULT_PER_PAGE = 3

# Final results, pass this dict as input to ml model 
RESULT = {}

# Invalid urls to filter out 
FILTER_URLS = (
    "maps.google",
    "policies.google",
    "accounts.google",
    "/preferences?",
    "support.google"
)


def _get_search_string(topic, tab="nws", topic_prefix="",
        parent_url="https://google.com", location_source_id="",
        result_per_page=RESULT_PER_PAGE) -> str:
    """Returns search url.

    Args:
        topic (str): topic to search
        tab (str): search tab to scrape from
        topic prefix (str): prefix for search string
        parent_url (str): search engine and domain to use
        location_source_id (str): unique identifier to specify location if
            default parent_url is not used
        result_per_page (int): number of results per page

    Returns:
        url (str): url search string
    """
    url = f"{parent_url}/search?q={topic_prefix+topic}&{location_source_id}"\
        f"&tbm={tab}&num={result_per_page}"

    return url


def _get_soup_object(url) -> bs4.BeautifulSoup:
    """Parse the given url.

    Args:
        url (str): takes url to parse and build the soup object

    Returns:
        soup (bs4.BeautifulSoup): bs4 object contiaing parsed html
    """
    request_result=requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    return soup


def _get_urls(soup, keyword=None) -> list:
    """Get news links from the google search.

    Args:
        soup (bs4.BeautifulSoup): soup object to iterate over
        keyword (str): word to search inside url string, if keyword found
            in the url, it is a valid url

    Returns:
        valid_urls (list): list of valid urls from the google result
    """
    valid_urls = []
    tag = soup.find_all('a')
    for text in tag:
        href_text = text.get('href')
        url = href_text[href_text.find('http'):]
        if keyword and keyword not in url:
            pass
        else:
            if "http" in url and not any(
                invalid_url in url for invalid_url in FILTER_URLS
            ):
                valid_urls.append(url)
    return valid_urls


def _filter_duplicate_urls(urls) -> set:
    """Filter duplicate urls from the valid urls

    Args:
        urls (list): list of valid urls

    Returns:
        unique_urls (list): list of valid unique urls
    """
    clean_urls = set()
    for url in urls:
        cleaned_url = url.split("&sa=U")[0]
        clean_urls.add(cleaned_url)
    return clean_urls


def _get_content(soup, keyword=None):
    """Get content from each news url if article is valid.

    Args:
        soup (bs4.BeautifulSoup): soup object to iterate over
        keyword (str): word to search inside url string, if keyword found
            in the url, it is a valid url

    Returns:
        articles_list (list): list containing content of different articles
    """
    articles = {}
    urls = _filter_duplicate_urls(_get_urls(soup, keyword))
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Comment/Uncomment below line to
                # hide/print url of each article
                url_soup = _get_soup_object(url)
                article_tags = url_soup.find_all('article')
                p_tags = article_tags[0].find_all('p')
                final_article = ''
                list_paragraphs = []
                for p in range(0, len(p_tags)):
                    paragraph = p_tags[p].get_text()
                    list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs)
                if final_article:
                    articles[url] = final_article
        except Exception as err:
            pass
    return articles


def _format_result(articles, topic_count, topic_prefix="TOPIC_",
    group_prefix="GROUP_") -> None:
    """Format the result articles by group and topic
    
    Args:
        articles (dict): articles dictionary where key is url and value is
            article's content
        topic_count (int): index of current topic
        topic_prefix (str): prefix to use for topic
        group_prefix (str): prefix to use for group

    Returns:
        articles_list (list): list containing content of different articles
    """
    for url in articles:
        key = ""
        for valid_url in GROUPS:
            if valid_url in url:
                key = GROUPS[valid_url]
        if not key:
            key = OTHER_GROUP
        result_key = group_prefix + str(key) + "_" + topic_prefix +\
                str(topic_count+1)
        if RESULT.get(result_key):
            RESULT[result_key] = RESULT[result_key] + [articles[url]]
        else:
            RESULT[result_key] = [articles[url]]


if __name__ == "__main__":
    # Driver function
    num_topics = int(input("Please enter number of topics you want to"
                            " search: "))
    for i in range(num_topics):
        TOPICS.append(str(input(f"Enter topic no. {i+1}: ")))

    print(f"Selected Topics: {TOPICS}\n")
    
    RESULT_PER_PAGE = int(input("Enter number of results you want per"
        " page for each topic (default is 3 results/page, 10 results/page is"
        " recommended for better results): "))

    print("\nProcessing inputs.....\n")

    topic_prefix = "TOPIC_"
    group_prefix = "GROUP_"
    for topic_count, topic in enumerate(TOPICS):
        url = _get_search_string(topic, SEARCH_TAB, TOPIC_PREFIX,
            SEARCH_ENGINE_URL, SEARCH_ENGINE_SOURCE_ID, RESULT_PER_PAGE)
        soup_obj = _get_soup_object(url)
        articles = _get_content(soup_obj)
        _format_result(articles, topic_count, topic_prefix, group_prefix)
    print(RESULT)
