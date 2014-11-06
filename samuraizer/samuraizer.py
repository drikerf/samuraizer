"""
    samuraizer.samuraizer
"""

from .config import STOPWORDS
import string, os, re, math

def extract_keywords(data, **kwargs):
    """Extract keywords from data.
    :param **kwargs: p - Keyword tolerance, defaults to 0.1.
                     step - Step to decrease p between calls, default to 0.005.
                     desired_words - Desired minimum numbers of keywords to try to extract.
    :returns: List of extracted keywords.
    """
    # Setup.
    p = kwargs.get('p', 0.1)
    step = kwargs.get('step', 0.0005)
    # Default minwords is calculated by log(length of data) + 1 floored.
    try:
        desired_words = kwargs.get('min_words', math.floor(math.log(len(data))+1))
    except ValueError:
        return [] # Empty input data.
    # If no data, return empty list.
    if len(data) == 0: return []
    
    # Extract keywords from data.
    # 1. Create a list of words from input data.
    #    If no words, return empty list.
    words = make_word_list(data)
    if len(words) == 0: return []

    # 2. Clean list from english stopwords.
    #    If no words, return empty list.
    words = clean_word_list(words)
    if len(words) == 0: return []
    
    # 3. Make a word:frequency map.
    word_freq = make_frequency_map(words)
    
    # 4. Get most frequent words compared relatively.
    most_frequent_words = most_frequent(word_freq, words, p, step, desired_words)
    return [item for item in most_frequent_words.keys()]

def make_word_list(data):
    """Create a word list of input text.
    :param data: Data to create list from.
    :returns: Word list with all words lowercase and stripped punctuation.
    """
    return [word.strip(string.punctuation).lower() for word 
            in re.split("\s|-|'s|'\s", data) if 
            len(word.strip(string.punctuation).lower()) > 0]

def clean_word_list(words):
    """Create a clean word list without stopwords.
    :param words: Word list to clean.
    :returns: Clean list.
    """
    return [word for word in words if
            len(word) > 0 and word not in STOPWORDS]

def make_frequency_map(words):
    """Maps Word-Frequency pairs.
    :param words: List of words to process.
    :returns: Dict with word-frequency pairs.
    """
    # Map word frequency.
    # 1. Sort word list by length. This helps us match similar words.
    # Sort has O(n logn) 
    # TODO: An equivalent solution with O(n).
    words.sort(key=len)
    
    # 2. For every word in words:
    #   a. If stripping of any suffixes at the end of word makes a word
    #      that is already in dict it is probably realted and we add one
    #      to that word.
    #   b. If there is no similar word in map, add word to dict.
    
    # Modern english suffixes.
    suffixes = ['s', 'ed', 't', 'ing', 'en', 'er', 'est', 'n\'t', 'ize', 'ise',
                'fy', 'ly', 'ful', 'able', 'ible', 'hood', 'ess', 'ness', 'less',
                'ism', 'ment', 'ist', 'al','ish','tion','ology']
    word_freq = {}
    # TODO: If Word ends with a suffix but should not be stripped?
    for word in words:
        match = False
        for suffix in suffixes:
            try:
                word_freq[word.rstrip(suffix)] += 1
                match = True
                break
            except KeyError:
                pass
        if not match:
            word_freq[word] = 1
    return word_freq

def most_frequent(word_freq, words, p, step, desired_words):
    """Get all words with higher relative frequency than p%.
    If we don't get the desired amount of words we try again
    with p=p-step until p <= 0 then we return most_frequent anyway.
    :param word_freq: Dict of word-frequency pairs.
    :param words: List of all words.
    :param p: Tolerance in % for most frequent words.
    :param step: Step to decrease p between calls.
    :param desired_words: Desired minimum number of words.
    :returns: Dict of most frequent words.
    """
    most_frequent_words = {}
    for word, freq in word_freq.items():
        try:
            if freq/len(words) > p:
                most_frequent_words[word] = freq
        except ZeroDivisionError:
            return most_frequent_words
    if len(most_frequent_words) < desired_words and p > 0 and step > 0:
        try:
            return most_frequent(word_freq, words, p-step, step, desired_words)
        except RuntimeError: return most_frequent_words # Maximum recursion depth exceeded.
    return most_frequent_words

def extract_summary(data):
    """Extract summary from data.
    :param data: Text to process.
    :returns: Summary string.
    """
    # TODO.
    return
