import unittest, string
from samuraizer.samuraizer import make_word_list, clean_word_list, \
    make_frequency_map, most_frequent, extract_keywords
from samuraizer.config import STOPWORDS


# TESTDATA.
STR = {}
STR['PUNCTUATION'] = string.punctuation 
STR['INVALID'] = STR['PUNCTUATION'] + '  -  -  \'s '
STR['INVALID_INPUT'] = None
STR['VALID'] = [('Valid words sometimes come in handy. Handy is sometime valid.',
                ['valid', 'words', 'sometimes', 'come', 'in', 'handy', 'handy', 
                 'is', 'sometime', 'valid'])]
LIST = {}
LIST['STOP'] = STOPWORDS
LIST['INVALID_INPUT'] = None
LIST['VALID'] = [(['valid', 'words', 'sometimes', 'come', 'in', 'handy','handy',
                   'is', 'sometime', 'valid'], ['valid', 'words', 'handy', 
                    'handy', 'valid'])]
MAP = {}
MAP['VALID'] = [(['hello'],{'hello':1}), (['hello','hello'],{'hello': 2}),
                (['green','colors','sometime','greener','than','grass','color'],
                 {'green': 2, 'color': 2, 'sometime': 1, 'than': 1, 'grass': 1})]

class TestMakeWordlist(unittest.TestCase):

    def test_empty_data(self):
        """make_word_list should return [] on input ''."""
        self.assertEqual([], make_word_list(''))

    def test_invalid_data(self):
        """make_word_list should return [] on invalid data."""
        self.assertEqual([], make_word_list(STR['PUNCTUATION']))
        self.assertEqual([], make_word_list(STR['INVALID']))

    def test_invalid_data_input(self):
        """make_word_list should throw TypeError on invalid input."""
        self.assertRaises(TypeError, make_word_list, STR['INVALID_INPUT'])

    def test_valid_data(self):
        """make_word_list should return list with all lowercase 
        and stripped whitespace."""
        for inp, out in STR['VALID']:
            self.assertEqual(out, make_word_list(inp))
        

class TestCleanWordList(unittest.TestCase):

    def test_empty_word_list(self):
        """clean_word_list should return [] on input []."""
        self.assertEqual([], clean_word_list([]))

    def test_only_stopword_word_list(self):
        """clean_word_list should return [] on stopword list."""
        self.assertEqual([], clean_word_list(LIST['STOP']))

    def test_invalid_input(self):
        """clean_word_list should throw TypeError on invalid input."""
        self.assertRaises(TypeError, clean_word_list, None)

    def test_valid_word_list(self):
        """clean_word_list should return list without stopwords."""
        for inp, out in LIST['VALID']:
            self.assertEqual(out, clean_word_list(inp))


class TestMakeFrequencyMap(unittest.TestCase):
    
    def test_empty_word_list(self):
        """make_frequency_map should return empty dict on empty input."""
        self.assertEqual({}, make_frequency_map([]))

    def test_invalid_input(self):
        """make_frequency_map should throw AttributeError on invalid input."""
        self.assertRaises(AttributeError, make_frequency_map, None)
        self.assertRaises(AttributeError, make_frequency_map, 'hello')

    def test_valid_word_list(self):
        """make_frequency_map should return word:frequency pairs on valid input."""
        for inp, out in MAP['VALID']:
            self.assertEqual(out, make_frequency_map(inp))


class TestMostFrequent(unittest.TestCase):

    def setUp(self):
        self.p = 0.1
        self.step = 0.0005
        self.dw = 3
        self.DATA = [({'hi': 3, 'bye': 4, 'howdy': 1, 'blue': 2},
                      ['hi', 'hi', 'hi', 'bye', 'bye', 'bye', 'bye', 'howdy',
                       'blue', 'blue'])]
    
    def test_empty_word_list(self):
        """most_frequent should return empty dict on empty input word list."""
        self.assertEqual({}, most_frequent({'a': 1}, [], self.p, self.step, self.dw))

    def test_empty_freq_dict(self):
        """most_frequent should return empty dict on empty input freq dict."""
        self.assertEqual({}, most_frequent({}, ['a'], self.p, self.step, self.dw))

    def test_zero_step(self):
        """most_frequent will not terminate and should therefore return {}."""
        step = 0
        p = 0.5
        DATA = ({'hi':1,'hello':1,'hej':1,'hellooow':1},['hi','hello','hej','hellooow'])
        self.assertEqual({}, most_frequent(DATA[0], DATA[1], p, step, self.dw))

    def test_invalid_input(self):
        """most_frequent should throw AttributeError on empty dict input."""
        self.assertRaises(AttributeError, most_frequent, None, [], self.p, self.step, self.dw)

    def test_valid_vary_dw(self):
        """most_frequent should return dw most frequent words."""
        dw = [0,1,2,3,4]
        for inp1, inp2 in self.DATA:
            for d in dw:
                self.assertEqual(True, d <= len(most_frequent(inp1, inp2, self.p, self.step, d)))

    def test_valid_vary_p(self):
        """most_frequent should return dw most frequent words."""
        for inp1, inp2 in self.DATA:
            prev = []
            for p in range(0,10):
                p = p/10
                cur = most_frequent(inp1,inp2,p,self.step,self.dw)
                self.assertEqual(True, len(cur) >= len(prev))
                

class TestExtractKeyWord(unittest.TestCase):

    def setUp(self):
        self.p = 0.4
        self.step = 0.0001
        self.dw = 2
        self.DATA = (('Hello there, I have green apples here. Do you know green apples?', 
                      ['apples', 'green']),
                     ('Green and Yellow are colors, so are Green, yes color, wait what? again!',
                      ['color', 'green']))

    def test_empty_input(self):
        """extract_keywords should return empty list on empty input."""
        self.assertEqual([], extract_keywords(''))
    
    def test_invalid_string(self):
        """extract_keywords should return empty list on invalid string."""
        self.assertEqual([], extract_keywords(STR['PUNCTUATION']))
        self.assertEqual([], extract_keywords(STR['INVALID']))
    
    def test_invalid_input(self):
        """extract_keywords should throw TypeError on invalid input."""
        self.assertRaises(TypeError, extract_keywords, STR['INVALID_INPUT'])

    def test_valid_input(self):
        """extract_keywords should return keywords from string."""
        for inp, out in self.DATA:
            res = extract_keywords(inp, p=self.p, step=self.step, desired_words=self.dw)
            self.assertEqual(2, len(res))
            for x in out:
                self.assertEqual(True, x in res)
            
if __name__ == '__main__':
    unittest.main()
