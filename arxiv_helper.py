import requests
import re
from bs4 import BeautifulSoup as bs



def get_papers(field: str):
    """
    Get all papers from the arXiv for a given field.

    :param field: The field to get papers for.
    :return: A list of papers.
    """
    url = f'https://arxiv.org/list/{field}/new'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    lists = soup.find_all('dl')

    new_subs = lists[0]
    
    papers = []
    for dt, dd in zip(new_subs.find_all('dt'), new_subs.find_all('dd')):
        paper = {}
        paper['id'] = re.search(r"arXiv:(\d{4}\.\d{5})", dt.text, re.DOTALL).group(1)
        paper['title'] = re.search(r"Title:\s*(.*)", dd.find("div", {"class": "list-title mathjax"}).text).group(1).strip()
        paper['authors'] = dd.find("div", {"class": "list-authors"}).text.replace("Authors:\n", "").replace("\n", "").strip()
        paper['subjects'] = dd.find("div", {"class": "list-subjects"}).text.replace("Subjects: ", "").strip()
        try:
            paper['abstract'] = dd.find("p", {"class": "mathjax"}).text.replace("\n", " ").strip()
        except AttributeError:
            paper['abstract'] = None

        papers.append(paper)

    return papers