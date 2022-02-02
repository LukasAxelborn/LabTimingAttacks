import sys, re, requests

def listtostring(s):
    return (''.join([str(elem) for elem in s]))

url = "http://dart.cse.kau.se:12345/auth/100/axelalvi/3b1a9f8934eccb4470c9c1b7850d8e"

charlist = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
#url = 'http://dart.cse.kau.se:12345/auth/100/axelalvi/'


hexfinnishlist = []

for i in charlist:
    for j in charlist:
        hexfinnishlist.append(f"{i}{j}")

for i in range(len(hexfinnishlist)):
    re = requests.get(url + listtostring(hexfinnishlist[i]))
    print("Testing: " + url + listtostring(hexfinnishlist[i]))
    if str(re) == "<Response [200]>":
        print("OK! Correct: " + listtostring(hexfinnishlist[i]))
        break