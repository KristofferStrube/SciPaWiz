from scholarly import scholarly
from time import sleep


scholar = 'Davide Mottin'
scholar_dir = "files/DavideMottin"


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
            f.write(f"{citation.bib['title']}")
            citers = citation.bib['author']
            try:
                for citer in citers:
                    citingauthors.add(citer)
            except:
                pass
    except:
        sleep(5*60)
        bypass_rate_limit_pub(pub, f)


def bypass_rate_limit_citing(citingauthor, f):
    try:
        search_query = scholarly.search_author(citingauthor)
        cauthor = next(search_query).fill()
        f.write(f"{extract_author_information(cauthor)}\n")
    except:
        sleep(10*60)
        bypass_rate_limit_citing(citingauthor, f)


# Retrieve the author's data, fill-in, and print
search_query = scholarly.search_author(scholar)
author = next(search_query).fill()
with open(f"{scholar_dir}/{scholar}", 'w+') as f:
    f.write(extract_author_information(author))


with open(f"{scholar_dir}/citingpapers", "w+") as f:
    for pub in author.publications:
        # citations_titles = [citation.bib['title'] for citation in pub.citedby]
        sleep(15)
        bypass_rate_limit_pub(pub, f)
            

with open(f"{scholar_dir}/citingauthors", 'w+') as f:
    for citingauthor in citingauthors:
        bypass_rate_limit_citing(citingauthor, f)
