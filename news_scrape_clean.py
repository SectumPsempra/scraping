import requests
import bs4
  
text= "fishing dispute in south china sea"
result_per_page = 10

# The area specific url uses google china(asian)/us domain, this is based on
# the fact that if you are based out of a certain location, google will show
# results specific to that location first
asian_url = f"https://google.com.hk/search?q={text}&num={result_per_page}&"\
                "hl=zh-CN&sourceid=cnhp%2F/"

us_url = f"https://google.com/search?q={text}&num={result_per_page}"

groups_dict = {}

def parse_url(url):
    """Parse the given url.

    Args:
        url: takes url to parse and build the soup object
    Returns:
        soup: bs4 object contiaing parsed html
    """
    request_result=requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    return soup

def get_news_urls(soup):
    """Get news links from the google search.

    Args:
        soup: soup object to iterate over
    Returns:
        valid_urls: list of valid urls from the google result
    """
    valid_urls = []
    tag = soup.find_all('a')
    for text in tag:
        href_text = text.get('href')
        url = href_text[href_text.find('http'):]
        if 'fish' in url:
            valid_urls.append(url)
    return valid_urls

def get_content_from_news_urls(soup):
    """Get content from each news url if article is valid.

    Args:
        soup: soup object to iterate over
    Returns:
        None
    """
    articles_list = []
    urls = get_news_urls(soup)
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Comment/Uncomment below line to hide/print url of each article
                # print(url)
                url_soup = parse_url(url)
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

# Comment/Uncomment below code to hide/show data based on US source:
soup_obj_us_news = parse_url(us_url)
group_1_articles_list = get_content_from_news_urls(soup_obj_us_news)

# Comment/Uncomment below code to hide/show data based on Asian source:
soup_obj_asian_news = parse_url(asian_url)
group_2_articles_list = get_content_from_news_urls(soup_obj_asian_news)

# Pass this list to gpt2, or you can further break each string down using full
# stop as a separator.
# 'Group A' denotes US group, 'Group B' denotes Asian group.
groups_dict["Group A"] = group_1_articles_list
groups_dict["Group B"] = group_2_articles_list
