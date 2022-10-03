# Most upvoted StackOverflow Python questions

Parse a copy of StackOverflow Python questions which we cached.

Retrieve + parse this URL with requests + BeautifulSoup and extract the question (question-hyperlink class), votes (vote-count-post class) and number of views (views class) into a list.

Next filter the list to only show questions with more than one million views (HTML = "..m views") and sort the remaining questions descending on number of votes. See the tests for the expected return output. Some pretty good questions in that list!
