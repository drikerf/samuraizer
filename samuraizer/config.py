import os
# Read stopwords.
src = os.path.join(os.path.dirname(__file__), 'resources/stopwords.txt')
# We use a dict for O(1) Lookup.
STOPWORDS = dict([item, None] for item in open(src,"r").read().split("\n"))
