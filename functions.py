import json

with open("_internal/importantfiles/crossbreeding.json",
          "r",
          encoding = "utf-8") as cfpr:
    crossbreeds = json.load(cfpr)

with open("_internal/importantfiles/othersources.json",
          "r",
          encoding = "utf-8") as ofpr:
    other = json.load(ofpr)

with open("_internal/importantfiles/onlycross.json",
          "r",
          encoding = "utf-8") as ocfpr:
    onlycross = json.load(ocfpr)

with open("_internal/importantfiles/gatherlist.json",
          "r",
          encoding = "utf-8") as gfpr:
    gatherlist = json.load(gfpr)

# Function 1: Given Input and Output, return Path from Input and Output

def make_pairs(seedlist):

    seedlist.sort()

    if len(seedlist) == 2:
        return [seedlist]

    templist = []

    for x in seedlist:
        temp = seedlist.copy()
        temp.remove(x)
        for y in temp:
            templist.append([x,y])

    for item in templist:
        item.sort()

    output = []

    for item in templist:
        if item not in output:
            output.append(item)

    return output

    

def check_crosses(inputlist, result):

    global crossbreeds

    output = {} # create empty output

    for seed in result:
        output[seed] = []

        potentialseeds = {} # for target seed, create list in output and
                            # empty map

        pairs = make_pairs(inputlist) # make pairs from inventory seeds

        for key in crossbreeds: # for every seed
            temp = crossbreeds[key].copy()
            for pair in pairs:
                # if that seed can be made by seeds in inventory
                if pair in temp or list(reversed(pair)) in temp:
                    try:
                        # add it to seeds that can be made,
                        # and append the pair to the option list
                        potentialseeds[key].append(pair)
                    except KeyError:
                        potentialseeds[key] = []
                        potentialseeds[key].append(pair)

    allseeds = True

    for seed in result:
        if seed not in list(potentialseeds.keys()):
            allseeds = False # if not every target seed was made

    if allseeds:
        for seed in output:
            # if every target was made, set output of seed to the option list
            # for that seed
            output[seed] = potentialseeds[seed]
    else:
        # if not, make a new "inventory" out of seeds that can be made
        newlist = inputlist + list(potentialseeds.keys())
        newlist = list(dict.fromkeys(newlist)) # and eliminate any duplicates
        if newlist == inputlist:
            return output # if no new seeds can be made, return the output
        # check the new list for potential crosses
        newtry = check_crosses(newlist, result)
        # list of all the seeds that can be made using the new inventory
        newkeys = list(newtry.keys())
        for key in newkeys: # for each of those seeds
            # look at every pair that can produce that seed
            for pair in newtry[key]:
                # for every seed in every such pair
                for seed in pair:
                    # if the seed is not in the original inventory
                    if seed not in inputlist and seed not in newkeys:
                        # update the potential crosses with a dict on how to
                        # get to the seed in question
                        newtry.update(check_crosses(inputlist, [seed]))
        output.update(newtry)

    for key in output:
        templist = []
        for pair in output[key]:
            pair.sort()
            if pair not in templist:
                templist.append(pair)
        output[key] = templist

    return output

def bettercrosses(inputlist, result):

    global crossbreeds

    global other

    global onlycross

    output = {}

    potentialseeds = {}
    
    pairs = make_pairs(inputlist)

    for seed in result:
        output[seed] = []

        for key in crossbreeds:
            if key in onlycross:
                temp = onlycross[key].copy()
                for pair in pairs:
                    if pair in temp or list(reversed(pair)) in temp:
                        try:
                            potentialseeds[key].append(pair)
                        except KeyError:
                            potentialseeds[key] = []
                            potentialseeds[key].append(pair)
            elif key not in inputlist:
                potentialseeds[key] = [other[key]]
    
    allseeds = True

    for seed in result:
        if seed not in list(potentialseeds.keys()):
            allseeds = False

    if allseeds:
        for seed in output:
            output[seed] = potentialseeds[seed]
    else:
        newlist = inputlist + list(potentialseeds.keys())
        newlist = list(dict.fromkeys(newlist))
        if newlist == inputlist:
            return output
        newtry = bettercrosses(newlist, result)
        newkeys = list(newtry.keys())
        for key in newkeys:
            for pair in newtry[key]:
                for seed in pair:
                    if seed in other and seed not in inputlist:
                        tempmap = {seed: [other[seed]]}
                        newtry.update(tempmap)
                    elif seed not in inputlist and seed not in newkeys:
                        newtry.update(bettercrosses(inputlist, [seed]))
        output.update(newtry)
    
    for key in output:
        templist = []
        for pair in output[key]:
            pair.sort()
            if pair not in templist:
                templist.append(pair)
        output[key] = templist

    return output


def splitmap(inputmap):

    output = []

    for key in inputmap:
        options = inputmap[key]
        for pair in options:
            output.append({key: [pair]})
    return output

def betterclean(inputmap):
    output = {}

    for key in inputmap:
        options = inputmap[key]
        output[key] = []
        newoptions = []
        for pair in options:
            if len(pair) == 2:
                zeroseed = isinstance(pair[0], str)
                oneseed = isinstance(pair[1], str)
                zerodict = isinstance(pair[0], dict)
                onedict = isinstance(pair[1], dict)
                if zeroseed and oneseed:
                    newoptions.append(pair)
                elif zeroseed and onedict:
                    dictone = pair[1].copy()
                    # if len(dictone[tempkey][0]) != 1:
                    dictone = betterclean(dictone)
                    templist = splitmap(dictone)
                    for item in templist:
                        newoptions.append([pair[0], item])
                elif zerodict and oneseed:
                    dictzero = pair[0].copy()
                    dictzero = betterclean(dictzero)
                    templist = splitmap(dictzero)
                    for item in templist:
                        newoptions.append([item, pair[1]])
                elif zerodict and onedict:
                    dictzero = pair[0].copy()
                    dictone = pair[1].copy()
                    dictzero = betterclean(dictzero)
                    dictone = betterclean(dictone)
                    templistone = splitmap(dictzero)
                    templisttwo = splitmap(dictone)
                    for x in templistone:
                        for y in templisttwo:
                            newoptions.append([x,y])
            else:
                newoptions.append(pair)
        output[key] = newoptions
    return output
      
def betterremove(inputmap):

    output = inputmap.copy()

    for key in output:
        for pair in output[key]:
            if len(pair) == 2:
                seedzero = pair[0]
                seedone = pair[1]
                zerodict = isinstance(seedzero, dict)
                onedict = isinstance(seedone, dict)
                if str(seedzero) in str(seedone) and zerodict:
                    for seed in seedzero.keys():
                        pair[0] = seed
                    if onedict:
                        pair[1] = betterremove(seedone)
                elif str(seedone) in str(seedzero) and onedict:
                    for seed in seedone.keys():
                        pair[1] = seed
                    if zerodict:
                        pair[0] = betterremove(seedzero)
                elif onedict and zerodict:
                    pair[0] = betterremove(seedzero)
                    pair[1] = betterremove(seedone)
                else:
                    for item in pair:
                        if isinstance(item, dict):
                            item = betterremove(item)
    
    for key in output:
        templist = []
        for item in output[key]:
            if item not in templist:
                templist.append(item)
        output[key] = templist

    return output

    
def shortestpath(inputlist, results, gather = True):

    inputpairs = make_pairs(inputlist) # make all possible pairs from inventory

    if gather:
        inputmap = bettercrosses(inputlist, results) # check for crosses
    else:
        inputmap = check_crosses(inputlist, results)

    output = {} # create empty output

    for item in results: # for each target item
        output[item] = [] # create an empty list in output
        # create a copy of a list of all pairs that produce the target item
        temppairs = inputmap[item].copy()
        if len(inputmap[item][0]) == 1:
            output[item].append(inputmap[item][0])
            return output
        for pair in inputpairs: # for each pair of seeds in the inventory
            if pair in temppairs: # if that pair can produce the result
                output[item].append(pair) # append the pair to outputlist
            else:
                # else, for each pair that can produce the target
                for otherpair in temppairs:
                    temppair = [] # create a temppair
                    for x in otherpair: # for each seed in the otherpair
                        if x not in inputlist: # if seed not in inputlist
                            temp = shortestpath(inputlist, [x], gather)
                            temppair.append(temp)
                        else:
                            temppair.append(x)
                    output[item].append(temppair)
    
    output = betterclean(output)

    output = betterremove(output)

    return output

def recursivedepth(inputlist):

    global crossbreeds

    output = 1 #assume the pair is a simple pair, one step

    for item in inputlist: # for each seed in pair
        if isinstance(item, dict): # if its a complex seed:
            for key in item:
                templist = []
                # then for each pair that can create the seed
                for pair in item[key]:
                    # if the pair is indeed a pair (and not a place to gather
                    # from)
                    if len(pair) == 2:
                        for seed in pair: # then for each seed in that pair
                            # if that seed is not in crossbreeds
                            if not (isinstance(seed, str)
                                    and seed in crossbreeds):
                                # append to templist
                                templist.append(recursivedepth([seed]))
                    else:
                        templist.append(recursivedepth(pair))
                if templist:
                    for step in templist:
                        output = output + step # add up all the steps

    return output
      
def stepamount(inputmap):

    global crossbreeds

    output = {}

    for key in inputmap: # for each seed in inputmap:
        tempmap = {} # create temporary output map for seed
        # create list of each possible source for seed
        optionlist = inputmap[key]
        for item in optionlist: # for each source
            depth = recursivedepth(item) 
            try:
                tempmap[depth].append(item)
            except KeyError:
                tempmap[depth] = []
                tempmap[depth].append(item)
            finallist = []
            templist = tempmap[depth].copy()
            for item in templist:
                if item not in finallist and len(finallist) < 501:
                    finallist.append(item)
            tempmap[depth] = list(reversed(finallist))
        if list(tempmap.keys()) != []:
            leaststeps = min(list(tempmap.keys()))
            tempmap = {key: {leaststeps: tempmap[leaststeps]}}
        else:
            tempmap = {key: {0: []}}
        output.update(tempmap)

    return output


def stepfrommap(inputmap):
    output = []
    for key in inputmap:
        pair = inputmap[key]
        if isinstance(pair, list) and len(pair) == 2:
            zerodict = isinstance(pair[0], dict)
            onedict = isinstance(pair[1], dict)
            if zerodict and onedict:
                output = stepfrommap(pair[0]) + stepfrommap(pair[1])
                for seedzero in pair[0]:
                    for seedone in pair[1]:
                        output.append("Cross " + seedzero +
                                      " with " + seedone +
                                      " to get " + key)
            elif zerodict:
                output = stepfrommap(pair[0])
                for seed in pair[0]:
                    output.append("Cross " + seed +
                                  " with " + pair[1] +
                                  " to get " + key)
            elif onedict:
                output = stepfrommap(pair[1])
                for seed in pair[1]:
                    output.append("Cross " + seed +
                                  " with " + pair[0] +
                                  " to get " + key)
            else:
                output.append("Cross " + pair[0] +
                              " with " + pair[1] +
                              " to get " + key)
        elif isinstance(pair, str):
            output.append("Gather " + key +
                          " from: " + pair)
    return output

def returnsteps(inputlist):

    output = []

    currentstep = []

    for item in inputlist:
        if isinstance(item, dict):
            output = output + stepfrommap(item)
            for key in item.keys():
                currentstep.append(key)
        else:
            currentstep.append(item)

    if len(currentstep) == 2:
        finalstring = ("Cross " + currentstep[0] +
                       " with " + currentstep[1])
    
    output.append(finalstring)

    return output

def cleanupmap(inputmap):
    
    output = {}

    tolist = []

    fromlist = []

    for key in inputmap:
        output[key] = []
        fromlist = inputmap[key]
        for poss in fromlist:
            if len(poss) < 2:
                tolist = poss
            else:
                templist = []
                temppair = []
                if isinstance(poss[0], str) and isinstance(poss[1], str):
                    templist.append(poss)
                else:
                    for item in poss:
                        if (isinstance(item, str)
                                and templist == []
                                and temppair == []):
                            temppair.append(item)
                        elif (isinstance(item, str)
                              and templist == []
                              and temppair != []):
                            temppair.append(item)
                            templist.append(temppair)
                            temppair = []
                        elif isinstance(item, str) and templist != []:
                            for pair in templist:
                                pair.append(item)
                        elif (isinstance(item, dict)
                              and temppair == []
                              and templist == []):
                            item = cleanupmap(item)
                            seed = list(item.keys())[0]
                            for pair in item[seed]:
                                templist.append([{seed: pair}])
                        elif (isinstance(item, dict)
                              and temppair != []
                              and templist == []):
                            item = cleanupmap(item)
                            seed = list(item.keys())[0]
                            for pair in item[seed]:
                                templist.append([temppair[0], {seed: pair}])
                            temppair = []
                        else:
                            item = cleanupmap(item)
                            temptemplist = []
                            seed = list(item.keys())[0]
                            for pair in item[seed]:
                                for x in templist:
                                    temptemplist.append([x[0], {seed: pair}])
                            templist = temptemplist.copy()
                for item in templist:
                    tolist.append(item)
        output[key] = tolist

    return output

def cleanstep(inputmap):

    for key in inputmap:
        inputmap[key] = cleanupmap(inputmap[key])

    return inputmap

    
def steplist(inputmap):

    output = {}
    
    for result in inputmap:
        steps = 0
        for stepnumber in inputmap[result]:
            numofpaths = len(inputmap[result][stepnumber])
            if numofpaths == 0:
                keystring = ("There is no way to make " + result +
                             " with the given seeds.")
            elif numofpaths == 1:
                keystring = ("There is one way to make " + result +
                             " in " + str(stepnumber) +
                             " steps:")
            elif numofpaths > 25:
                numstring = str(numofpaths)
                if numofpaths > 500:
                    numstring = "(over) 500"
                keystring = ("There are " + numstring +
                             " ways to make " + result +
                             " in " + str(stepnumber) +
                             " steps, here are 10 of them:")
                inputmap[result][stepnumber] = inputmap[result][stepnumber][:10]
            else:
                keystring = ("There are " + str(numofpaths) +
                             " ways to make " + result +
                             " in " + str(stepnumber) +
                             " steps:")
            steps = stepnumber
        output[keystring] = []
        for item in inputmap[result][steps]:
            currentstep = item.copy()
            listofsteps = returnsteps(currentstep)
            listofsteps[-1] = listofsteps[-1] + " to get " + result
            output[keystring].append(listofsteps)
    
    return output

def calculatesteps(inputlist, resultlist, gather):
    
    output = {}

    for item in resultlist:
        depth = 1
        found = False
        while depth < 11 and not found:
            possibles = allpossibles(inputlist, depth)
            for key in possibles:
                if item in possibles[key]:
                    found = True
            depth = depth + 1
        
        outputtemp = {}
        
        if not found:
            print("Seed too complicated")
            outputtemp.update({item + " takes over 8 steps and is a bit too "
                                      "complicated for this silly little "
                                      "program...":[]})
        else:
            print("Calculating shortest path for " + item + "...")
            outputtemp = shortestpath(inputlist, [item], gather)
            print("Calculating amount of steps needed...")
            outputtemp = stepamount(outputtemp)
            print("Cleaning up the steps...")
            outputtemp = cleanstep(outputtemp)
            print("Creating the steplist...")
            outputtemp = steplist(outputtemp)
        output.update(outputtemp)

    return output

# Function 2: Given a seed, return all seeds needed to breed seed that can
# also be collected from other sources

def seedsources(inputlist):

    global gatherlist

    global onlycross

    global other

    output = {}

    for item in inputlist:
        outputlist = []
        if item in other:
            keystring = item + " can already be gathered! Here's the source:"
            outputlist = other[item]
        elif item in gatherlist:
            keystring = ("Here are possible combinations of seeds you need "
                         "for ") + item + " and where you get them:"
            for pair in gatherlist[item]:
                temppair = []
                for seed in pair:
                    temppair.append(seed + ": " + other[seed][0])
                outputlist.append(temppair)
        output[keystring] = outputlist
    
    return output

# Function 3: Given a list of Seeds and a depth, return all seeds that can be
# bred in "depth" amount of steps

def allpossibles(inputlist, depth, gatherSeeds = True):

    global onlycross

    global crossbreeds

    global other
    
    checkmap = {}

    templist = []

    checklist = []

    allseeds = []

    templist.append(inputlist)

    if gatherSeeds:
        templist.append(list(other.keys()))
        checkmap = onlycross
    else:
        checkmap = crossbreeds

    allseeds = inputlist.copy()

    done = False

    checkcounter = 0

    while len(templist) <= depth + 1 and not done:
        checkcounter = checkcounter + 1
        checklist = templist.copy()
        allpairs = make_pairs(allseeds)
        for seed in checkmap:
            for pair in allpairs:
                seeddepth = 1
                if (pair in checkmap[seed]
                         or list(reversed(pair))
                         in checkmap[seed]):
                    seeddepthzero = -1
                    seeddepthone = -1
                    for seeds in templist:
                        if pair[0] in seeds and seeddepthzero == -1:
                            seeddepthzero = templist.index(seeds)
                        if pair[1] in seeds and seeddepthone == -1:
                            seeddepthone = templist.index(seeds)
                    seeddepth = seeddepth + seeddepthzero + seeddepthone
                    try:
                        templist[seeddepth].append(seed)
                    except IndexError:
                        while len(templist) <= seeddepth:
                            templist.append([])
                        templist[seeddepth].append(seed)
                    templist[0] = templist[0] + pair
        allseeds = []
        for i in range(len(templist)):
            templist[i].sort()
            templist[i] = list(dict.fromkeys(templist[i]))
        for j in range(len(checklist)):
            checklist[j].sort()
            checklist[j] = list(dict.fromkeys(checklist[j]))
        for thing in templist:
            thing = list(dict.fromkeys(thing))
            allseeds = allseeds + thing
        allseeds = list(dict.fromkeys(allseeds))

        if checklist == templist and checkcounter > depth:
            done = True

    finallist = []

    for i in range(len(templist)):
        thing = templist[i]
        finallist = finallist + thing
    finallist = list(dict.fromkeys(finallist))
    finallist.sort()


    outputdepth = depth if len(templist) - 1 >= depth else len(templist) - 1

    if finallist:
        keystring = ("These are all the seeds that can be made in " +
                     str(depth) + " steps:")
    else:
        keystring = ("No seeds can be made in " + str(depth) +
                     " steps from the seeds given.")

    output = {keystring: finallist}

    return output

if __name__ == "__main__":
    test = ["Krakka Root Seeds",
            "Mirror Apple Seeds",
            "Thavnairian Onion Seeds",
            "Chamomile Seeds",
            "Gysahl Green Seeds"]
    testresult = ["Curiel Root Seeds"] # Blood Pepper Seeds

    output = calculatesteps(test, testresult, False)

    #print(allpossibles(test, 10, True))

    #print(sourceseeds(testresult[0], test))

    with open("temp2.json", "w", encoding = "utf-8") as fpw:
        json.dump(output, fpw)




