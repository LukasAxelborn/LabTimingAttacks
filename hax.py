import sys
import urllib.request
import urllib.parse


url = 'https://dart.cse.kau.se:12345/auth/10/alice/c2d07d3c5ed87430f67f20ce9e711307'
f = urllib.request.urlopen(url)
print(f.read().decode('utf-8'))
