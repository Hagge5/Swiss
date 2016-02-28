import random
import time

class Player:
    wins = 0
    name = ""
    faced = []

    def __init__(self, name):
        self.faced = []
        self.name = name

    def hasFaced(self, other):
        for name in self.faced:
            if name == other.name:
                return True
        return False

    def toString(self):
        return "| wins=" + str(self.wins) + " name=" + self.name + " faced=" + str(self.faced) + " |"

#A very specific player used to match up players in odd-participant rounds
#Can't gain wins, is called "Nobody"
#Don't create another player with this name
nonp = Player("Nobody")
#Returns the nonplayer
def nonePlayer():
    return nonp

#Increments wins/losses and updates faced-list, and/or creates new players if given
#  winners/losers don't exist in lst
def addWin(lst, winner, loser):
    if winner == loser:
        lst.append(Player(winner))
    else:
        winnerExists = False
        loserExists = False
        for player in lst:
            if winnerExists and loserExists:
                break
            if player.name == winner:
                if not player is nonePlayer():
                    player.wins += 1
                player.faced.append(loser)
                winnerExists = True
            elif player.name == loser:
                player.faced.append(winner)
                loserExists = True
        if not winnerExists:
            lst.append(Player(winner))
            lst[-1].wins = 1
            lst[-1].faced.append(loser)
        if not loserExists:
            lst.append(Player(loser))
            lst[-1].faced.append(winner)
        

#Reads player elements into a list
def readPlayers():
    result = [nonePlayer()]
    while True:
        inp = input()
        if inp == "end":
            break
        elif inp != "" and inp[0] != "#":
            inp_s = inp.split()
            name = inp_s[0]
            if len(inp_s) == 1:
                addWin(result, name, name) #Add new player
            else:
                opponent = inp_s[1]
                addWin(result, name, opponent)
    #Remove non-player if even number of players
    if len(result) % 2 != 0:
        for i,e in enumerate(result):
            if e is nonePlayer():
                del result[i]
                break
    return result

#Sorts a list of player elements properly, by wins
def sortedByWins(lst):
    return sorted(lst, key=lambda e: e.wins, reverse=True)

#Sorts a list of player elements properly, by names
def sortedByNames(lst):
    return sorted(lst, key=lambda e: e.name)

#Converts a pos int to str, ending with a st. nd, rd, or th
def posToString(pos):
    if pos == 1:
        return "1st"
    elif pos == 2:
        return "2nd"
    elif pos == 3:
        return "3rd"
    else:
        return str(pos) + "th"

#Adds a suffix s if count != 1
def suffix(count, word):
    if count == 1:
        return word
    else:
        return word + "s"

#Assumes lst have player elements and is sorted
#Prints a leaderboard
def leaderboard(lst):
    pos = 1
    lastE = None
    for e in lst:
        if lastE is not None and e.wins != lastE.wins: 
            pos += 1
        if not nonePlayer() is e:
            print(posToString(pos), ". ", e.name, "\t\t(", e.wins, suffix(e.wins, " win"), ")" )
        lastE = e

#Generates all non-empty possible matchups. 
#Assumes seq is of even length and partResult is []
def matchups(seq, partResult):
    if len(seq) == 0:
        yield partResult
    else:
        first = seq[0]
        remaining = seq[1:]
        for i,e in enumerate(remaining):
            if not first.hasFaced(e):
                nseq = remaining[:]
                del nseq[i]
                yield from matchups(nseq, partResult + [(first, e)])

#Generates all possible matchups based on players in lst
def getAllPossibleMatchups(lst):
    if len(lst) % 2 == 0:
        return [[]] + list(matchups(lst, []))
    else:
        return [[]] + list(matchups(lst + [nonePlayer()], []))

def xor(a,b):
    return (a and not b) or (not a and b)

#Calculate an integer indicating how undesirable this matchup is. The higher the worse.
def badnessOfMatchup(matchup):
    if len(matchup) < 1:
        return float("inf")
    result = 0
    for pair in matchup:
        value = pair[0].wins - pair[1].wins
        result += value*value
    return result

#Calculates the optimal matchup out of the given ones
def getOptimalMatchup(allMatchups):
    withBadness = [[e, badnessOfMatchup(e)] for e in allMatchups]
    muSorted = sorted(withBadness, key=lambda e: e[1])
    lowest = [e for e in muSorted if e[1] == muSorted[0][1]]
    lowestElement = random.choice(lowest)
    return lowestElement[0], lowestElement[1]

#Sorts matchups based on wins/names
def prettierMatchup(matchup):
    def cmpr(a,b):
        if a.wins != b.wins:
            return a.wins > b.wins
        else:
            return min(a.name.lower(),b.name.lower()) == a.name.lower()
    result = []
    for pair in matchup:
        first = pair[0]
        second = pair[1]
        if cmpr(first, second):
            result.append((first, second))
        else:
            result.append((second, first))
    return sorted(result, key=lambda e: e[0].wins, reverse=True)

#Given matchup is an ordered list of players.
#If the list has an odd len, the last element will not play anyone
def printMatchup(matchup):
    if len(matchup) < 1:
        print("No matchups are possible.")
    else:
        for pair in matchup:
            print(pair[0].name, "VS.", pair[1].name)
        
def main():
    players = sortedByWins(sortedByNames(readPlayers()))
    startTime = time.time()
    print("")
    print("------------LEADERBOARD------------------")
    leaderboard(players)
    print("")
    print("------------UPCOMING GAMES---------------")
    random.shuffle(players)
    players = sortedByWins(players)
    possible = getAllPossibleMatchups(players)
    matchup, badness = getOptimalMatchup(possible) 
    printMatchup(prettierMatchup(matchup))
    print("")
    print("------------STATISTICS-------------------")
    print(len(players), "players.")
    print(len(possible), "legal matchups.")
    print("Optimal solution has badness of", badness, ".")
    print("Execution took", round((time.time()-startTime), 3),"seconds.")
    print("")
    
                        

if __name__ == "__main__":
    main()
            