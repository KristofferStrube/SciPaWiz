import json
import requests

dir = "files/IvanDamgaard"
query = "Ivan + Damgård"


def download(author=True):
    if author:
        searchstring = f"https://dblp.org/search/publ/api?q=author%3A{query}%3A&format=json&h=1000"

    print(searchstring)
    return json.loads(requests.get(searchstring).text)


def download_papers_by_author(author_object):
    papers_doi = [(hit['info']['title'], hit['info']['doi']) for hit in author_object['result']['hits']['hit'] if 'doi' in hit['info']]
    with open(f"{dir}/papers_by_author", 'w+') as f:
        for tuple in papers_doi:
            f.write(f"{tuple[0]},{tuple[1]}\n")
    return papers_doi


def load_papers_by_author():
    papers_doi = []
    with open(f"{dir}/papers_by_author") as f:
        for line in f.readlines():
            l = line.split(',')
            papers_doi.append((l[0], l[1]))
    return papers_doi


def download_citations_for_paper(author_dois):
    citing_dois = []
    for doi in author_dois:
        doi = doi.strip('\n')
        request_string = f"https://opencitations.net/index/api/v1/citations/{doi}"
        try:
            text = requests.get(request_string).text
            res = json.loads(text)
            if len(res) > 0:
                for citing_doi in res:
                    citing_dois.append(citing_doi['citing'].strip("coci => "))
            else:
                print("No doi for this paper")
        except:
            print(f"Error parsing json for {text}")

    with open(f"{dir}/papers_citing_author", 'w+') as f:
        for doi in citing_dois:
            f.write(f"{doi}\n")


def load_papers_citing_author():
    with open(f"{dir}/papers_citing_author") as f:
        return [x.strip('\n') for x in f.readlines()]


def get_authors_by_doi(doi):
    request_string = f"https://opencitations.net/index/api/v1/metadata/{doi}"
    try:
        text = requests.get(request_string).text
        res = json.loads(text)
        if len(res) > 0:
            for author_information in res:
                return author_information['author']
    except:
        print("Trist panda")
        return None


def download_citing_authors(dois):
    authors = [get_authors_by_doi(doi) for doi in dois]
    authors = [x for x in authors if x is not None]
    with open(f"{dir}/authors_citing_author", "w'") as f:
        for author in authors:
            f.write(f"{author}\n")


download_citing_authors(load_papers_citing_author())