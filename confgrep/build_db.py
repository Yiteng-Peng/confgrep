import requests
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup

from .config import *
from .utils import new_logger, get_conf_list
from .db import Base, Paper

logger = new_logger("DB")

KEYWORD = "kernel"

engine = sqlalchemy.create_engine(f'sqlite:///papers.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def save_paper(conf, year, title, authors, abstract):
    session = Session()
    paper = Paper(conference=conf, year=year, title=title, authors=", ".join(authors), abstract=abstract)
    session.add(paper)
    session.commit()
    session.close()

def paper_exist(conf, year, title, authors, abstract):
    session = Session()
    paper = session.query(Paper).filter(Paper.conference==conf, Paper.year==year, Paper.title==title).first()
    session.close()
    return paper is not None

def get_papers(name, year):
    conf_value = NAME_MAP[name]
    if isinstance(conf_value, tuple):
        assoc, conf = conf_value[0], conf_value[1]
    else:
        assoc, conf = conf_value, conf_value

    cnt = 0
    try:
        r = requests.get(f"https://dblp.org/db/conf/{assoc}/{conf}{year}.html")
        assert r.status_code == 200

        html = BeautifulSoup(r.text, 'html.parser')
        paper_htmls = html.find_all("li", {'class': "inproceedings"})
        for paper_html in paper_htmls:
            title = paper_html.find('span', {'class': 'title'}).text
            authors = [x.text for x in paper_html.find_all('span', {'itemprop': 'author'})]
            abstract = ''
            # insert the entry only if the paper does not exist
            if not paper_exist(name, year, title, authors, abstract):
                save_paper(name, year, title, authors, abstract)
            cnt += 1
    except Exception as e:
        logger.warning(f"Failed to obtain papers at {name}-{year}")

    logger.debug(f"Found {cnt} papers at {name}-{year}...")


def build_db(field, year_low, year_high):
    conf_list = get_conf_list(field)
    
    for conf in conf_list:
        for year in range(year_low, year_high):
            get_papers(conf, year)
