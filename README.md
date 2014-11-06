Samuraizer
=========

Samuraizer is a keyword extractor for Python 3.
It uses stopwords and simple suffix stemming.
Currently it only supports suffix stemming and stopwords in english language but go ahead and try something else.

Installation
--------------
Currently the only way is to clone the repo and do:
```sh
python setup.py install
```

Usage
--------------
To extract keywords from data just:

```sh
import samuraizer
samuraizer.extract_keywords(data)
```
Optional parameters:
- p - Start value for percentage of text a word needs to own to be a keyword. (default=0.1)
- step - Step to decrease p for every call failing to return desired number of keywords. (default= 0.0005)
- desired_words - Desired minimum number of keywords. (default=floor(log(len(data))+1))


License
----

BSD
