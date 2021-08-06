# *Explanation*

## *Driver function*

The program asks the user to input number of topics to search. Based on number of topics entered for each iteration, the code generates search string(generally a google.com url), calls the *_get_content* function to generate articles and format the results according to groups and topics.

----------

## *Output*

`{"GRP_1_TOP_1": ['Text from article 1', 'Text from article 2', 'Text from article 3'], "GRP_2_TOP_1": ['Text from article 1', 'Text from article 2', 'Text from article 3'], "GRP_1_TOP_2": ['Text from article 1', 'Text from article 2', 'Text from article 3'], "GRP_2_TOP_2": ['Text from article 1', 'Text from article 2', 'Text from article 3']}`
