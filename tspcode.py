import pandas as pd
import utm
import math
import matplotlib.pyplot as plt
import sys
import random
import warnings

#Load problem 
def setup():
    #This code hides warnings - use it to make it easier to novice users, but comment it out when developeing/debugging as
    # warnings may be useful!!
    warnings.filterwarnings('ignore')
    global problem
    problem = pd.read_csv('./edinburgh.csv')
    problem['Text'] = problem['Name']
    problem = problem.set_index('Name')
    global start
    start = (55.948526, -3.198427)
    global dists
    dists = pd.read_csv('./dists.csv')
    dists = dists.set_index('key')

def conv(lat, lon):
    #Lower left

    ll_lon = -3.211108
    ll_lat = 55.944933
    lx, ly, zone, ut = utm.from_latlon(ll_lat, ll_lon)
   
    #Upper right
    ur_lon =  -3.183407
    ur_lat = 55.958019
    rx, ry, zone, ut = utm.from_latlon(ur_lat, ur_lon)

    dx = rx -lx
    dy = ry -ly 
    nx, ny, zone, ut = utm.from_latlon(lat, lon)
    return (((nx-lx)/dx)*300),(((ny-ly)/dy)*300)

def findroute(start, end):
    xystart = conv(start[0],start[1])
    xyend = conv(end[0],end[1])
    return math.dist(xystart, xyend)

#Get the route represented by solution. Returns a set of OSM node refs. 
#To plot the route get the lat/lon of the OSM refs
def getRoute(solution):
    return ""

def draw_map(solution):
    count=1
    plt.rcParams["figure.figsize"] = [17.00, 13.50]
    plt.rcParams["figure.autolayout"] = True
    im = plt.imread("map.png")
    fig, ax = plt.subplots()
    im = ax.imshow(im, extent=[0, 300, 0, 300])
    # x,y = conv(55.952996,-3.189636)
    # ax.text(x,y, 'H', fontsize = 22)
    for c in solution:
        for index, row in problem.iterrows():
            if row['Text'] == c :
               x,y = conv(row['Lattitude'],row['Longitude'])
               ax.plot(x, y, marker="o", markersize=10, markeredgecolor="red", markerfacecolor="green")
               ax.text(x+2,y-2, (row['Text'] +":"+str(count)), fontsize = 22) 
               count  = count +1 
    plt.show()



#Measure the distance travelled in a solution
def measure(solution):
    if not verify(solution):
        return 9999999
                 
    prev = '*'
    dist =0;
    for city in solution:
        key= prev+":"+city
        d= dists.loc[key]['dist']
        dist = dist + d
        prev = city
        
    key= prev+':*'
    d= dists.loc[key]['dist']
    dist = dist + d
    return dist
# dists.loc['AZ']['dist']

#Verify that <solution> is a valid permutation
def verify(solution):
    if len(problem) < len(solution):
        print("Sorry, your route has too many visits!")
        return False

    if len(problem) > len(solution):
        print("Sorry, your route has a visit missed out!")
    for r in problem['Text']:
        if not (r in solution):
              print("Sorry, your route is missing a visit to "+r+" !")
              return False
    
    for r in solution:
        if not r in problem['Text']:
                print("Sorry, I don't understand "+r)
                return False
    
    return True

def neighbour(city,options):
    if city =='':
        city = '*'
        
##    loc = (problem.loc[city].Lattitude,problem.loc[city].Longitude)
    dist = sys.maxsize   
    best = ''
    for index, row in problem.iterrows():
        ##        p = (row['Lattitude'],row['Longitude'])
        key = city +":"+row['Text']
        d= dists.loc[key]['dist']
        ##        d = findroute(loc,p)
        current = row['Text']
        if (current != city):
            if current in options:
                if (d<dist):
                    dist = d
                    best = row['Text']
    
    options = options.replace(best,'')                
    return best,options

##def swap_random(seq):
##    idx = range(len(seq))
##    i1, i2 = random.sample(idx, 2)
##    seq[i1], seq[i2] = seq[i2], seq[i1]

def random_change_5(seq):
    c= random.randint(1,3)
    if c==1:
        return random_change_1(seq)
    if c==2:
        return random_change_2(seq)
    if c==3:
        return random_change_3(seq)
    
def random_change_1(seq):
    idx = range(len(seq))
    i1, i2 = random.sample(idx, 2)
    c= seq[i1]
    seq = seq[0 : i1 : ] + seq[i1 + 1 : :]
    seq = seq[:i2] + c + seq[i2:]
    return seq

def random_change_4(st):
    seq = list(st)
    random.shuffle(seq)
    return ''.join(seq)

def random_change_2(st):
    seq = list(st)
    idx = range(len(seq))
    i1, i2 = random.sample(idx, 2)
    seq[i1], seq[i2] = seq[i2], seq[i1]
    return ''.join(seq)

def random_change_3(st):
    seq = list(st)
    idx = range(len(seq))
    i1, i2 = random.sample(idx, 2)
    while i1>=i2:
        i1, i2 = random.sample(idx, 2)
        
    t=''
    for x in range(i1,i2):
       t = t + seq[x]

    for x in range(i1,i2):
       seq[x] = t[-1]
       t = t[:-1]
    
    return ''.join(seq)
