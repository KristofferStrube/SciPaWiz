from scholarly import scholarly
import numpy as np
import time
from fp.fp import FreeProxy


scholar = 'Davide Mottin'
scholar_dir = "files/DavideMottin"
scholarly.use_tor(tor_sock_port=9050, tor_control_port=9051, tor_pw="scholarly_password")


def sleep():
    time.sleep((30-5)*np.random.random()+5)


def set_new_proxy():
    while True:
        proxy = FreeProxy(rand=True, timeout=1).get()
        proxy_works = scholarly.use_proxy(http=proxy, https=proxy)
        if proxy_works:
            break
    print("Working proxy:", proxy)
    return proxy


def extract_author_information(author):
    return f"""
        name: {author.name}
        affiliation: {author.affiliation}
        citedby: {author.citedby}
        citedby5y: {author.citedby5y}
        cites_per_year: {author.cites_per_year}
        hindex: {author.hindex}
        hindex5y: {author.hindex5y}
    """


def extract_paper_information(paper):
    return f"""
        citedby: {paper.citedby}
    """


citingauthors = set()


def bypass_rate_limit_pub(pub, f):
    try:
        for citation in pub.citedby:
            # sleep()
            f.write(f"{citation.bib['title']}")
            citers = citation.bib['author']
            try:
                for citer in citers:
                    citingauthors.add(citer)
            except:
                pass
    except:
        set_new_proxy()
        # sleep()
        bypass_rate_limit_pub(pub, f)


def bypass_rate_limit_citing(citingauthor, f):
    try:
        # sleep()
        search_query = scholarly.search_author(citingauthor)
        cauthor = next(search_query).fill()
        f.write(f"{extract_author_information(cauthor)}\n")
    except:
        # sleep()
        set_new_proxy()
        bypass_rate_limit_citing(citingauthor, f)


# Retrieve the author's data, fill-in, and print
search_query = scholarly.search_author(scholar)
author = next(search_query).fill()
with open(f"{scholar_dir}/{scholar}", 'w+') as f:
    f.write(extract_author_information(author))


with open(f"{scholar_dir}/citingpapers", "w+") as f:
    for pub in author.publications:
        # sleep()
        # citations_titles = [citation.bib['title'] for citation in pub.citedby]
        bypass_rate_limit_pub(pub, f)


with open(f"{scholar_dir}/citingauthors", 'w+') as f:
    for citingauthor in citingauthors:
        bypass_rate_limit_citing(citingauthor, f)
