from arxiv_helper import get_papers
from llm_helper import get_selected_papers, ChatLLM
from utils import *
from push_helper import email_pusher

import os
import logging
import random

from datetime import datetime
from dotenv import load_dotenv


# Common Subjects
# cs.LG - Machine Learning
# cs.AI - Artificial Intelligence
# cs.CV - Computer Vision and Pattern Recognition
# cs.SI - Social and Information Networks

if __name__ == '__main__':
    logger_init()
    load_dotenv(override=True)
    interests = os.getenv('INTERESTS')
    logger = logging.getLogger('arxivdigest')
    fields = ['cs.lg', 'cs.ai', 'cs.cv', 'cs.si']
    papers = []
    for field in fields:
        papers_fieeld = get_papers(field)
        papers += papers_fieeld
        logger.info(f'Number of papers in {field}: {len(papers_fieeld)}')
    papers = deduplicate_dicts(papers, 'id')
    bot = ChatLLM(model=os.getenv('LLM_MODEL'))
    papers = random.sample(papers, len(papers))
    selected_papers = get_selected_papers(bot, papers, interests)
    selected_papers = deduplicate_dicts(selected_papers, 'id')
    selected_paper_ids = [paper['id'] for paper in selected_papers]
    logger.info(f'Selected papers ids: {selected_paper_ids}')

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