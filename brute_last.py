import sys, re, requests

def listtostring(s):
    return (''.join([str(elem) for elem in s]))

url = "http://dart.cse.kau.se:12345/auth/99/axelalvi/798fc0f1716e8ab23cba9273350555"

#charlist = ['a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
charlist = ['5', '9']
#url = 'http://dart.cse.kau.se:12345/auth/100/axelalvi/'


hexfinnishlist = []

def appentofile(url):
    # Open a file with access mode 'a'
    with open("okurls.txt", "a") as file_object:
        # Append 'hello' at the end of file
        file_object.write(url)

for i in charlist:
    for j in charlist:
        hexfinnishlist.append(f"{i}{j}")

for i in range(len(hexfinnishlist)):
    re = requests.get(url + listtostring(hexfinnishlist[i]))
    print("Testing: " + url + listtostring(hexfinnishlist[i]))
    if str(re) == "<Response [200]>":
        print("OK! Correct: " + listtostring(hexfinnishlist[i]))
        appentofile(url + listtostring(hexfinnishlist[i]))
        break