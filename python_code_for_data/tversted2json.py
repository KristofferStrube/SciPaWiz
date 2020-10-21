dir = "files/IvanDamgaard"
query = "Ivan + Damgård"


with open(f"{dir}/citations_by_author") as f:
    lines = f.readlines()


def make_author_string(author, score):
    auth = f'\"author\": \"{author}\"'
    score = f'\"score\": \"{score}\"'
    return "{" + f"{auth}, {score}" + "}"


key_value_pairs = []

for line in lines:
    values = line.split(':')
    key_value_pairs.append(make_author_string(
        values[0], values[1].strip('\n')))

# Out put everything. Pipe output from program into file
print("[")
for pair in key_value_pairs:
    print(f"{pair},")
print("]")
