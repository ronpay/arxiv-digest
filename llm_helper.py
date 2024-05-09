import google.generativeai as genai
from openai import OpenAI

import textwrap
import dotenv
import os
import re
import logging

from utils import find_most_similar_paper_jaccard


logger = logging.getLogger('arxivdigest')

class ChatLLM():
    def __init__(self, model: str | None):
        if model is None:
            model = 'gemini-pro'
        if 'gpt' in model:
            self.api_key = os.getenv('OPENAI_API_KEY')
            self.api_base = os.getenv('OPENAI_API_BASE')
        elif 'gemini' in model:
            self.api_key = os.getenv('GOOGLE_API_KEY')
        else:
            raise ValueError('Un-support model!')
        self.model = model
    
    def _chat_gpt(self, req: str):
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base
        )
        completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {'role': 'user', 'content': req}
            ]
        )
        resp = completion.choices[0].message.content
        return resp

    def _chat_gemini(self, req: str):
        resp = genai.GenerativeModel(self.model).generate_content(req)
        resp = resp.text
        return resp

    def get_respondse(self, req: str):
        logger.info(f'Request: {req}')
        if 'gpt' in self.model:
            resp = self._chat_gpt(req)
        elif 'gemini' in self.model:
            resp = self._chat_gemini(req)
        logger.info(f'Response: {resp}')
        return resp
    
def get_selected_papers(bot, papers: list, interest: str):
    # spilit papers to 50
    selected_papers = []
    for i in range(0, len(papers), 50):
        selected_papers += get_selected_papers_aux(bot, papers[i:i+50], interest)
    return selected_papers

def get_selected_papers_aux(bot, papers: list, interest: str):
    prompt = 'Hello, I have a list of research papers, and I need help identifying which of them are relevant to a specific field of interest.'
    prompt += f'My field of interest is {interest}'
    prompt += 'Below is the list of paper titles:\n\n'
    for i, paper in enumerate(papers):
        paper_info = f'{i}. {paper["title"]}\n'
        prompt += paper_info
    prompt += '\n'
    prompt += f'You shoudl review each paper title one by one carefully. '
    prompt += f'And select the papers that are relevant to the field of {interest}. '
    prompt += f'The selection criteria include keyword matching of the title and in-depth analysis of the title before selection. '
    # prompt += f'You should at least return a paper, even if there is no match, please return the most similar one.'
    prompt += f'Return the list of papers which meet the requirement, in markdown list format.'
    prompt += f'For examle, if you think paper 1, 3, 5 are relevant, you should return:\n\n'
    prompt += f'1. WildGEN: Long-horizon Trajectory Generation for Wildlife\n'
    prompt += f'3. Physics-informed Deep Learning to Solve T hree-dimensional Terzaghi  Consolidation Equation: Forward and Inverse Problems\n'
    prompt += f'5. CoLafier: Collaborative Noisy Label Purifier With Local Intrinsic  Dimensionality Guidance\n'


    resp = bot.get_respondse(prompt)
    pattern = r'^\d+\.\s+(.*)|^-+\s+(.*)'
    titles = re.findall(pattern, resp, re.MULTILINE)
    titles = [title[0] if title[0] else title[1] for title in titles]
    selected_papers = []
    for title in titles:
        selected_papers.append(search_paper(title, papers))
    return selected_papers


def search_paper(title: str, papers: list):
    for paper in papers:
        if paper['title'] == title:
            return paper
    return find_most_similar_paper_jaccard(papers, title)
