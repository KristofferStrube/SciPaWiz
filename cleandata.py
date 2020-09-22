dir = "files/IvanDamgaard"
query = "Ivan + Damgård"


citations_by_author = dict()


lines = []
with open(f"{dir}/authors_citing_author") as f:
    lines = f.readlines()


for line in lines:
    authors = line.split("; ")
    authors = [x.strip("\n") for x in authors]
    print(authors)
    for author in authors:
        if author in citations_by_author:
            citations_by_author[author] = citations_by_author[author] + 1
        else:
            citations_by_author[author] = 1

with open(f"{dir}/citations_by_author", 'w+') as f:
    for k, v in citations_by_author.items():
        f.write(f"{k}:{v}\n")
