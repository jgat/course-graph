import networkx as nx
import requests
import matplotlib.pyplot as plt

def get_prereqs(course):
    r = requests.get('http://rota.eait.uq.edu.au/course/{0}.json'.format(course))
    if r.ok:
        data = r.json()
        return [p['code'] for p in data['prereqs'] if 'code' in p['_keys']]
    else:
        raise IOError("Couldn't retrieve " + r.url)

def get_all_prereqs(course, g=None):
    if g is None:
        g = nx.DiGraph()
    for p in get_prereqs(course):
        g.add_edge(course, p)
        get_all_prereqs(p, g)
    return g

import sys, pprint

g = nx.DiGraph()

for course in sys.argv[1:]:
    get_all_prereqs(course, g)

pprint.pprint(sorted(g.edges()))
pprint.pprint(sorted(g.nodes()))
nx.draw(g)
plt.show()
