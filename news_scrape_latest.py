import requests
import bs4


# Specify topics and optional keyword to check in url
TOPICS = (
    ("fishing dispute in south china sea", "fish"),
    ("presidential elections in usa", ""),
    ("extinction of animals in africa", "")
)

# Specify parent urls and location based source id
GROUPS = (
    ("https://google.com.hk", "hl=zh-CN&sourceid=cnhp%2F"),
    ("https://google.com", "")
)

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


def _get_search_string(topic, parent_url="https://google.com",
        location_source_id="", result_per_page=RESULT_PER_PAGE):
    """Returns search url.

    Args:
        topic (str): topic to search
        parent_url (str): search engine and domain to use
        location_source_id (str): unique identifier to specify location if
            default parent_url is not used
        result_per_page (int): number of results per page 
    Returns:
        url (str): url search string
    """
    url = f"{parent_url}/search?q={topic}&num={result_per_page}&"\
            f"{location_source_id}"

    return url


def _get_soup_object(url):
    """Parse the given url.

    Args:
        url (str): takes url to parse and build the soup object
    Returns:
        soup (bs4.BeautifulSoup): bs4 object contiaing parsed html
    """
    request_result=requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    return soup


def _get_urls(soup, keyword):
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


def _get_content(soup, keyword):
    """Get content from each news url if article is valid.

    Args:
        soup (bs4.BeautifulSoup): soup object to iterate over
        keyword (str): word to search inside url string, if keyword found
            in the url, it is a valid url

    Returns:
        articles_list (list): list containing content of different articles
    """
    articles_list = []
    urls = _get_urls(soup, keyword)
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
                    articles_list.append(final_article)
        except Exception as err:
            pass
    return articles_list


if __name__ == "__main__":
    # Driver function
    topic_prefix = "TOP_"
    group_prefix = "GRP_"
    for topic_count, topic_info in enumerate(TOPICS):
        topic, keyword = topic_info
        for grp_count, group_info in enumerate(GROUPS):
            search_engine_url, location_source_id = group_info
            url = _get_search_string(topic, search_engine_url,
                location_source_id)
            soup_obj = _get_soup_object(url)
            RESULT[group_prefix + str(grp_count+1) + "_" + topic_prefix +
                str(topic_count+1)] = _get_content(soup_obj, keyword)
