from operator import itemgetter

import requests
from bs4 import BeautifulSoup

cached_so_url = "https://bites-data.s3.us-east-2.amazonaws.com/so_python.html"


def top_python_questions(url=cached_so_url):
    """Use requests to retrieve the url / html,
       parse the questions out of the html with BeautifulSoup,
       filter them by >= 1m views ("..m views").
       Return a list of (question, num_votes) tuples ordered
       by num_votes descending (see tests for expected output).
    """
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    questions = soup.select(".question-summary")
    res = []

    for que in questions:
        question = que.select_one('.question-hyperlink')
        votes = que.select_one('.vote-count-post')
        views =  que.select_one('.views')

        if not (question and votes and views):
            continue

        votes = votes.getText().strip()
        question = question.getText()
        views = views.getText().strip()

        #print(question, votes, views, sep='\n', end='\n\n')

        if 'm views' not in views:
            continue

        res.append((question, int(votes)))

    return sorted(res, key=itemgetter(1), reverse=True)


if __name__ == "__main__":
    print(top_python_questions())