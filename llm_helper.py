import google.generativeai as genai
import textwrap
import dotenv
import os
import re
import logging

class gemini_bot():
    def __init__(self, model='gemini-pro'):
        dotenv.load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def get_respondse(self, req: str):
        logging.info(f'Request: {req}')
        resp = self.model.generate_content(req)
        resp = resp.text
        logging.info(f'Response: {resp}')
        return resp

def get_selected_papers(bot, papers: list, interest: str):
    prompt = 'Hello, I have a list of research papers, and I need help identifying which of them are relevant to a specific field of interest.'
    prompt += f'My field of interest is {interest}'
    prompt += 'Below is the list of paper titles along with their abstracts:\n\n'
    for i, paper in enumerate(papers):
        paper_info = f'{i}. Title: {paper["title"]}\n'
        prompt += paper_info
    prompt += '\n'
    prompt += f'Could you please review each paper and provide me with the numbers of those papers that are relevant to the field of {interest}? Thank you!'
    resp = bot.get_respondse(prompt)
    indexes = re.findall(r'\d+', resp)
    indexes = [int(i) for i in indexes]
    selected_papers = [papers[i] for i in indexes]
    return selected_papers