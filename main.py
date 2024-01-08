from arxiv_helper import get_papers
from llm_helper import get_selected_papers, gemini_bot
from utils import *
from push_helper import email_pusher

import os
import logging

from datetime import datetime
from dotenv import load_dotenv


# Common Subjects
# cs.LG - Machine Learning
# cs.AI - Artificial Intelligence
# cs.CV - Computer Vision and Pattern Recognition
# cs.SI - Social and Information Networks

if __name__ == '__main__':
    load_dotenv()
    interests = os.getenv('INTERESTS')
    logging.basicConfig(filename='arxivdigest.log', level=logging.INFO)
    fields = ['cs.lg', 'cs.ai', 'cs.cv', 'cs.si']
    papers = []
    for field in fields:
        papers += get_papers(field)
        logging.info(f'Number of papers in {field}: {len(papers)}')
    papers = deduplicate_dicts(papers, 'id')
    bot = gemini_bot()
    selected_papers = get_selected_papers(bot, papers, interests)
    selected_paper_ids = [paper['id'] for paper in selected_papers]
    logging.info(f'Selected papers ids: {selected_paper_ids}')

    content = str()
    for paper in selected_papers:
        paper_info = str()
        paper_info += f'ID: arxiv:{paper["id"]}\n'
        paper_info += f'Link: https://arxiv.org/abs/{paper["id"]}\n'
        paper_info += f'Title: {paper["title"]}\n'
        paper_info += f'Abstract: {paper["abstract"]}\n'
        paper_info += '\n'
        content += paper_info
    # get current date in format like January 05, 2024
    date = datetime.now().strftime('%B %d, %Y')
    subject = f'arXiv Daily Digest: {date}'
    body = f'Here are the papers that focus on {interests} for {date}:\n\n'
    body += content
    body += '\n'

    pusher = email_pusher()
    pusher.send_email(subject, body)