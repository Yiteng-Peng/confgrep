import os
from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from .config import *
from .db import Base, Paper
from .build_db import build_db
from .utils import new_logger, handle_field_str, get_conf_list
import argparse

DB_PATH = "papers.db"

engine = sqlalchemy.create_engine(f'sqlite:///{DB_PATH}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

logger = new_logger("ConfGrep")


def grep(keywords, field, year_low, year_high):
    # TODO: currently we only grep from title, also grep from other fields in the future maybe?
    constraints = []
    for x in keywords:
        constraints.append(Paper.title.contains(x))
    if "ALL" not in field:
        conf_list = get_conf_list(field)
        constraints.append(Paper.conference.in_(conf_list))
    constraints.extend([Paper.year >= year_low, Paper.year <= year_high])
    

    with Session() as session:
        papers = session.query(Paper).filter(*constraints).all()

    # perform customized sorthing
    papers = sorted(papers, key=lambda paper: paper.year + ALL_CONFERENCES_LIST.index(paper.conference)/10, reverse=True)
    return papers


def show_papers(papers):
    for paper in papers:
        print(paper)


def main():
    parser = argparse.ArgumentParser(description='Scripts to query the paper database',
                                     usage="%(prog)s [options] -k <keywords>")
    parser.add_argument('-k', type=str, help="keywords to grep, separated by ','. For example, 'linux,kernel,exploit'", default='')
    parser.add_argument('--build-db', action="store_true", help="Builds the database of conference papers")
    parser.add_argument("-f", "--field", type=str, help='''
                        build database or grep for top conference in specific field, based on CCF-A ;)
                        ATTENTION!NOW SUPPORT:
                        all: all field; sc: security; se: software engineering;
                        pick fields separated by ','. For example, 'sc, se'. String is case insensitive.
                        Add Your Favorite Conference In the "config.py" file!''', default='all')
    parser.add_argument("-yl", "--year_low", type=int, help="low year for grep or database build, default is 2000", default=2000)
    parser.add_argument("-yh", "--year_high", type=int, help="high year for grep or database build, default is current year + 1", default=datetime.now().year+1)
    args = parser.parse_args()
    
    field = handle_field_str(args.field)
    year_low, year_high = args.year_low , args.year_high

    if args.k:
        assert os.path.exists(DB_PATH), f"need to build a paper database first to perform wanted queries"
        keywords = [x.strip() for x in args.k.split(',')]
        if keywords:
            logger.info("Grep based on the following keywords: %s", ', '.join(keywords))
        else:
            logger.warning("No keyword is provided. Return all the papers.")

        papers = grep(keywords, field, year_low, year_high)
        logger.debug(f"Found {len(papers)} papers")

        show_papers(papers)
    elif args.build_db:
        print("Building db...")
        build_db(field, year_low, year_high)


if __name__ == "__main__":
    main()
