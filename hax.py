import sys
import time
import urllib.request
import urllib.parse

import requests

#


def listtostring(s):
    return (''.join([str(elem) for elem in s]))


charlist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


guessedtag = [0] * 32
url = 'http://dart.cse.kau.se:12345/auth/200/alice/'
bestchar = '0'
for i in range(len(guessedtag)):
    current_longest = -100
    print(f"index {i}, guessedtag: {listtostring(guessedtag)}")

    for char in charlist:
        print(f"index {i} char: {char}")
        guessedtag[i] = char
        newtag = listtostring(guessedtag)
        t0 = time.time()
        # make request
        requests.get(url + newtag)
        t1 = time.time()
        rq_time = t1 - t0

        if(rq_time > current_longest):
            current_longest = rq_time
            bestchar = char

    guessedtag[i] = bestchar


print(listtostring(guessedtag))
