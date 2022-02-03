import sys
import time
import urllib.request
import urllib.parse

import requests

#-------------------------------------------------------------------------------------------
#GLOBAL VARIABLES
#-------------------------------------------------------------------------------------------
charlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

delay = 10
name = "axelalvi"

url = "http://dart.cse.kau.se:12345/auth/" + str(delay) + "/" + name + "/"

#-------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------
#HELP FUNCTIONS
#-------------------------------------------------------------------------------------------
def listtostring(s):
    return (''.join([str(elem) for elem in s]))

#make multiple rq & return min rsp time
def min_rsp_time(url, runs):
    min = 1000000000000
    for i in range(runs):
        # make request
        response = requests.get(url)
        rsp_time = response.elapsed.total_seconds() * 1000
        if rsp_time < min:
            min = rsp_time
    return min

#make multiple rq & return avg rsp time
def avg_rsp_time(url, runs):
    total = 0
    for i in range(runs):
        # make request
        response = requests.get(url)
        total += response.elapsed.total_seconds() * 1000

    return total / runs

def appentofile(url):
    # Open a file with access mode 'a'
    with open("okurls.txt", "a") as file_object:
        # Append 'hello' at the end of file
        file_object.write(url)

#-------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------
#create list of all hex numbers (00 - ff)
#-------------------------------------------------------------------------------------------
hexlist = []

for i in charlist:
    for j in charlist:
        hexlist.append(f"{i}{j}")
#-------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------
#get avg rsp to add to intervals since response depends on "timing jitters", multiply by 2 for safety
#-------------------------------------------------------------------------------------------
general_rsp_time = avg_rsp_time(url + ("0" * 32), 100) * 2
#general_rsp_time = avg_rsp_time("https://www.vecka.nu", 100)
print("General rsp time: " + str(general_rsp_time) + " ms")
time.sleep(2)
#-------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------
#test until response is 200 (be patient)
#-------------------------------------------------------------------------------------------
while(True):

    url = "http://dart.cse.kau.se:12345/auth/" + str(delay) + "/" + name + "/"
    #delay += 10
    print("Testing delay: " + str(delay))
    time.sleep(2)
    count_runs = 0
    while(count_runs < 5):
        count_runs += 1
        #-------------------------------------------------------------------------------------------
        #find first hex in tag that by checking which one gives back a response time inside desired interval
        #-------------------------------------------------------------------------------------------
        temp_tag = ['00'] * 16
        longest_rsp = -100
        curr_first = ""
        for hex in hexlist:
            temp_tag[0] = hex
            tag_string = listtostring(temp_tag)
            rsp_time = min_rsp_time(url + tag_string, 1)
            print(f"char: {hex} rsp_time: {rsp_time} besthex: {curr_first} longest_rsp {longest_rsp}")
            if(rsp_time > longest_rsp and rsp_time < (delay + general_rsp_time)):
                longest_rsp = rsp_time
                curr_first = hex
                if rsp_time > (delay + 15):
                    break
        #-------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------
        #make guessed hex first (& all) hex in guessed tag
        #-------------------------------------------------------------------------------------------
        guessedtag = [curr_first] * 16
        besthex = ""
        wrong_guess = False
        #-------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------
        #go through guessed tag hex by hex, until only hex remains
        #-------------------------------------------------------------------------------------------
        i = 1
        while i < len(guessedtag) - 1:

            current_longest = -100
            sweetspot_top = (i + 1) * delay + general_rsp_time
            sweetspot_bottom = (i + 1) * delay
            minimum_rsp_time = i * delay

            #if rq_time is less than i * delay, we know we guessed wrong and want to try previous i again
            if wrong_guess is True:
                if i < 3:
                    wrong_guess = False
                    break
                i -= 2
                wrong_guess = False

            
            print(f"index {i}, guessedtag: {listtostring(guessedtag)}")

            for hex in hexlist:
                print(f"index {i} char: {hex} besthex: {besthex} curr_long: {current_longest}")
                guessedtag[i] = hex
                newtag = listtostring(guessedtag)
                rq_time = min_rsp_time((url + newtag), 1)
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
                        temp_rq_time = min_rsp_time((url + temp_list_string), 10)
                        next_min_rsp_time = (i + 1) * delay
                        next_max_rsp_time = ((i + 1) * delay) + delay
                        print(f"trying: {besthex} next_min: {next_min_rsp_time} temp_rq_time: {temp_rq_time} next_max: {next_max_rsp_time}")
                        if temp_rq_time > next_min_rsp_time and temp_rq_time < next_max_rsp_time:
                            break
                        else:
                            current_longest = -100
                            best_hex = ""

            guessedtag[i] = besthex
            i += 1
            #-------------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------------
        #brute force last hex until response is 200
        #-------------------------------------------------------------------------------------------
        if i > 14:
            for hex in hexlist:
                guessedtag[15] = hex
                re = requests.get(url + listtostring(guessedtag))
                print("Testing: " + url + listtostring(guessedtag))
                if str(re) == "<Response [200]>":
                    print("OK! Correct: " + url + listtostring(guessedtag))
                    appentofile("Delay: " + str(delay) + ", URL: " + url + listtostring(guessedtag))
                    break
        #-------------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------------
        #test and break if response is 200
        #-------------------------------------------------------------------------------------------
        re = requests.get(url + listtostring(guessedtag))
        if str(re) == "<Response [200]>":
            print("OK!")
            break
        #-------------------------------------------------------------------------------------------
    delay += 10
#-------------------------------------------------------------------------------------------

