import google.generativeai as genai
import textwrap
import dotenv
import os
import re
import logging

logger = logging.getLogger('arxivdigest')

class gemini_bot():
    def __init__(self, model='gemini-pro'):
        dotenv.load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def get_respondse(self, req: str):
        logger.info(f'Request: {req}')
        resp = self.model.generate_content(req)
        resp = resp.text
        logger.info(f'Response: {resp}')
        return resp

def get_selected_papers_aux(bot, papers: list, interest: str):
    prompt = 'Hello, I have a list of research papers, and I need help identifying which of them are relevant to a specific field of interest.'
    prompt += f'My field of interest is {interest}'
    prompt += 'Below is the list of paper titles:\n\n'
    for i, paper in enumerate(papers):
        paper_info = f'{i}. Title: {paper["title"]}\n'
        prompt += paper_info
    prompt += '\n'
    prompt += f'You shoudl review each paper title one by one carefully. '
    prompt += f'And select the papers that are relevant to the field of {interest}. '
    prompt += f'The selection criteria include keyword matching of the title and in-depth analysis of the title before selection. '
    # prompt += f'You should at least return a paper, even if there is no match, please return the most similar one.'
    prompt += f'Return the list of papers which meet the requirement, in markdown list format.'
    prompt += f'For examle, if you think paper 1, 3, 5 are relevant, you should return:\n\n'
    prompt += f'1. Title: WildGEN: Long-horizon Trajectory Generation for Wildlife\n'
    prompt += f'3. Title: Physics-informed Deep Learning to Solve Three-dimensional Terzaghi  Consolidation Equation: Forward and Inverse Problems\n'
    prompt += f'5. Title: CoLafier: Collaborative Noisy Label Purifier With Local Intrinsic  Dimensionality Guidance\n'


    resp = bot.get_respondse(prompt)
    indexes = re.findall(r'\d+', resp)
    indexes = [int(i) for i in indexes]
    selected_papers = [papers[i] for i in indexes]
    return selected_papers

def get_selected_papers(bot, papers: list, interest: str):
    # spilit papers to 50
    selected_papers = []
    for i in range(0, len(papers), 50):
        selected_papers += get_selected_papers_aux(bot, papers[i:i+50], interest)
    return selected_papers