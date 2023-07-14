# AUTOGENERATED! DO NOT EDIT! File to edit: ../create_graph.ipynb.

# %% auto 0
__all__ = ['Author', 'Number']

# %% ../create_graph.ipynb 6
class Author:
    def __init__(self, first, middle, last, email=None, publications=[]):
        self.first = first
        self.middle = middle
        self.last = last
        self.email = email
        self.publications = publications

# %% ../create_graph.ipynb 9
import pprint

# %% ../create_graph.ipynb 15
from fastcore.basics import patch

# %% ../create_graph.ipynb 17
class Number:
    "A number."
    def __init__(self, num): self.num = num

# %% ../create_graph.ipynb 22
# two things need to be added to create a patch for Author
@patch
def __repr__(self:Author):
    return pprint.pformat(vars(self))

# %% ../create_graph.ipynb 44
for index_a in range(len(authors)):
    for index_b in range(index_a + 1, len(authors)):
        author_a = authors[index_a]
        author_b = authors[index_b]
        
        for publication_a in author_a.publications:
            for publication_b in author_b.publications:
                if publication_a == publication_b:
                    G.add_edge(author, publication)
                    print(f"Match found between a{index_a+1} and a{index_b+1} for publication {publication_a}")