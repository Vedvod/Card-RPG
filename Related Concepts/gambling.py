#-------------------------modules-------------------------
import os, random, time, sys, math, winsound

#-----------------------function(s)-----------------------
win_percent=lambda x: (k_value*math.log(x+1)+b_value)/100

#-------------------------classes-------------------------
class timer:
    def __init__(self):
        self.start_time=time.time()
    def time(self):
        return time.time()-self.start_time

#--------------------------setup--------------------------
a=(5, 100)
b=(10001, 900)
k_value = (b[1]-a[1])/(math.log(b[0])-math.log(a[0]))
b_value=a[1]-k_value*math.log(a[0])
roll_times=int(10e5)

#------------------------main line------------------------
bet, roll_times=round(float((_:=(input("bet and rolls? $")).split(", ")+["10"])[0]), 2), int(eval(_[1]))
total, losses=0, 0
print(f"now rolling a set of {int(eval(_[1]))} games...")
game_time=timer()
for x in range(roll_times):
    rolls=[random.randint(1, 10000) for x in range(10)]; gcd=math.gcd(rolls[1], rolls[2]); track=round(win_percent(gcd)*bet, 2)
    if track < bet:
        losses+=1
    #print(f"${track} ({gcd} --> {round(100*win_percent(gcd), 2)}%)")
    total+=track
print("\a", end="")
print(f"\nTotal: ${roll_times*bet} --> ${round(total, 2)}")
print(f"Total returns is {round(total*100/(roll_times*bet), 2)}% of bet, with {round(100*losses/roll_times, 2)}% of games losing money.")
print(f"Whole set of {roll_times} games took {round(game_time.time(), 2)} seconds.")
input("Press Enter to exit the script...")