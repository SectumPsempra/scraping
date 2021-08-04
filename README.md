# *Explanation of news scrape code*

Flow of the program:

## *Global variables*

1) *TOPICS*: topic tuple contians optional keyword as well to filter.
2) *GROUPS*: Groups of different sources(their url and location based source id)
3) *RESULT_PER_PAGE*: Defines the number of queries returned per page(max 100), this is the number of articles the code will iterate over.
4) *RESULT*: Dictionary of sources, contains news text from different sources.
5) *FILTER_URLS*: Filter invalid urls from the generated urls.

----------

## *Methods*

1) *_get_search_string*: It takes topic to search, search domain url, location based source id, RESULT_PER_PAGE and returns search string.
2) *_get_soup_object*: It takes the query text url as input and returns the soup object.
3) *_get_urls*: It takes the parsed soup object(beautifulsoup's html object) and returns a list of all links which are search result of *_get_soup_object*. This will be equal to the number of *result_per_page* generally.
4) *_get_content*: Once we have the urls for each individual link, we use this function to parse the text of each link and format it in a paragraph after removing un-necessary information. Below is the explanation of how this function works:

    - Create an empty *RESULT* dictionary which will be returned at the end having the cleaned articles grouped by source.
    - Read each news link and check whether the response is valid or not(page not found, etc).
    - If news link is valid parse it and get the soup object for the news link, which will be processed to get cleaned text.
    - Find all the items with 'article' tag which specifies that the text is coming from article body and not header/footer or some other part of the web page.
    - Find all the paragraph tags within an article tag and iterate over them one by one and create a consolidated paragraph per article.
    - If there is no paragraph found in the article or the code throws an error while processing the article, then ignore such exceptions.
    - Return the final *RESULT*, which can be used as an input to a machine learning model, if required.

----------

## *Driver function*

We are declaring topic and group prefixes here, that will be used to name keys of RESULT dictionary. For each topic in TOPICS tuple we iterate over each group in GROUPS and save the articles list in RESULT dictionary.

----------

## *Output*

`{"GRP_1_TOP_1": ['Text from article 1', 'Text from article 2', 'Text from article 3'], "GRP_2_TOP_1": ['Text from article 1', 'Text from article 2', 'Text from article 3'], "GRP_1_TOP_2": ['Text from article 1', 'Text from article 2', 'Text from article 3'], "GRP_2_TOP_2": ['Text from article 1', 'Text from article 2', 'Text from article 3']}`
