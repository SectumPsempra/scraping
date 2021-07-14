# *Explanation of news scrape code*

Flow of the program:

## *Arguments*

1) *text*: Query to search.
2) *result_per_page*: Defines the number of queries returned per page(max 100), this is the number of articles the code will iterate over.
3) *us_url* or *chinese_url*: Url specific to chinese location (this can be changed to any asian/other location, and can be modified to include tabs like google maps, news, images, etc).
4) *groups_dict*: Dictionary of sources, contains news text from different sources.

----------

## *Methods*

1) *parse_url*: It takes the query text url as input and returns the soup object.
2) *get_news_urls*: It takes the parsed soup object(beautifulsoup's html object) and returns a list of all links which are search result of *parse_url*. This will be equal to the number of *result_per_page* generally.
3) *get_content_from_news_urls*: Once we have the urls for each individual link, we use this function to parse the text of each link and format it in a paragraph after removing un-necessary information. Below is the explanation of how this function works:

    - Create an empty *groups_dict* dictionary which will be returned at the end having the cleaned articles grouped by source.
    - Read each news link and check whether the response is valid or not(page not found, etc).
    - If news link is valid parse it and get the soup object for the news link, which will be processed to get cleaned text.
    - Find all the items with 'article' tag which specifies that the text is coming from article body and not header/footer or some other part of the web page.
    - Find all the paragraph tags within an article tag and iterate over them one by one and create a consolidated paragraph per article.
    - If there is no paragraph found in the article or the code throws an error while processing the article, then ignore such exceptions.
    - Return the final *groups_dict*, which can be used as an input to a machine learning model, if required.

----------

## *Output*

`{"Group A": ['Text from article 1', 'Text from article 2', 'Text from article 3'], "Group B": ['Text from article 1', 'Text from article 2', 'Text from article 3']}`
