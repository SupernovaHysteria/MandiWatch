import requests
import json
import sys
import os.path
import matplotlib.pyplot as plt
import datetime


def getstate():
    state = input('Enter the state you live in : ').split()
    for i in range(len(state)):
        state[i] = state[i].capitalize()
    state = ' '.join(state)
    if (checkstate(state)):
        print('Accepted')
        return state
    elif state=='':
        print('Defaulting to')
        return 'Karnataka'
    else:
        print('The state entered is not valid, please try again')
        return getstate()


def geddit(things):
    tmp = input()
    tmp = tmp.capitalize()
    if tmp in things:
        print('Accepted')
        return tmp
    else:
        print('Invalid option entered, please try again')
        return geddit(things)



def checkstate(state):
    validstates = ['Andhra Pradesh','Telangana','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu and Kashmir','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Orissa','Punjab','Rajasthan','Sikkim','Tamil Nadu','Tripura','Uttarakhand','Uttar Pradesh','West Bengal','Andaman and Nicobar Islands','Chandigarh','Dadar and Nagar Haveli','Daman and Diu','Delhi','Lakshadeep','Pondicherry']
    if state in validstates:
        return True
    else:
        return False

#optimization to use binary search to be done later.
def binsearch(state,commodity,low,high):
    mid  = (high+low)//2
    r = requests.get('https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&offset='+str(mid)+'&limit=10')
    data = json.loads(r.text)
    #for key in data:
    #   print(key,':',data[key])
    midrecords = data['records']
    print(midrecords)
    found = False

    #for entry in midrecords:
        #if entry['state']==state and entry['commodity'] == commodity:


def commcheck(entry,commodities):
    for commodity in commodities:
        if commodity in entry['commodity']:
            return True
    return False

def linsearchfront(state,commodities,low,high,results):
    sf = False
    for i in range(low,high+1,10):
        print('Iteration :',i//10)
        r = requests.get('https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&offset=' + str(i)+'&limit=10')
        data = json.loads(r.text)
        #print(data['records'])
        records = data['records']

        for entry in records:
            if sf and entry['state']!=state:
                print('Search complete\n\n')
                return results
            elif entry['state']==state and commcheck(entry,commodities):
                sf  = True
                results.append(entry)
                print('HIT'.center(100,'-'))
    return results


def linsearchback(state,commodities,low,high,results):
    sf = False
    for i in range(high,low+1,-10):
        print('Iteration :',(high-i)//10)
        r = requests.get('https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&offset=' + str(i)+'&limit=10')
        data = json.loads(r.text)
        #print(data['records'])
        records = data['records']

        for entry in records[::-1]:
            if sf and entry['state']!=state:
                print('Search complete\n\n')
                return results
            elif entry['state']==state and commcheck(entry,commodities):
                sf  = True
                results.append(entry)
                print('HIT'.center(100,'-'))
    return results


def tracker(state,commodities):
    r = requests.get('https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&offset=0&limit=10')
    data = json.loads(r.text)
    #print(data)
    #for key in data:
    #    print(key,':',data[key])
    high = data['total'] - 10
    print('Number of records found :',high)
    low  = 0
    #for commodity in commodities :
    #    binsearch(state,commodity,low,high)
    results = []
    print('Searching the records')
    if abs(ord('A')-ord(state[0]))<=abs(ord('Z')-ord(state[0])):
        results = linsearchfront(state,commodities,low,high,results)
    else:
        results = linsearchback(state,commodities,low,high,results)
    return results



def getoption():
    option = input()

    if option == 'y':
        return True

    elif option == 'n':
        print('END'.center(100,'-'))
        sys.exit(0)
    else:
        print('Invalid option entered, please try again')
        return getoption()


def get_points(market,variety,rows):
    x=[]
    y=[]
    for row in rows:
        date = row[3].split('T')
        if row[0]==market and row[2]==variety and date[0] not in x:
            x.append(date[0])
            y.append(row[-1])
    return x,y


def sort_dates(all_x):
   dates = [datetime.datetime.strptime(date,'%Y-%m-%d') for date in all_x]
   dates.sort()
   dates = [datetime.datetime.strftime(date,'%Y-%m-%d')for date in dates]
   return dates



def plotter(state,commodities,userdistrict):
    print('Enter the commodity you want to plot.')
    for i in range(len(commodities)):
        print(i+1,'.',commodities[i])
    commodity = geddit(commodities)
    file = open(state+'_'+userdistrict+'_'+commodity+'.csv','r')
    raw_data = file.readlines()
    #print(raw_data)
    rows = []
    for line in raw_data:
        data = (line.split('|'))
        #print(data)
        row = []
        for e in data:
            row.append(e.strip())
        rows.append(row)
    #print(rows)
    del(rows[0])
    #print(rows)
    cleanrows = []
    for row in rows:
        if row not in cleanrows:
            cleanrows.append(row)
    rows = cleanrows[:]
    del(cleanrows)
    #print(rows)
    markets = []
    varieties = []
    for row in rows:
        if row[0] not in markets:
            markets.append(row[0])
        if row[2] not in varieties:
            varieties.append(row[2])
    #print(markets)
    #print(varieties)
    graphs = {}
    x = []
    y = []
    all_y = []
    all_x = []
    for market in markets:
        for variety in varieties:
            x,y = get_points(market,variety,rows)
            if x==[] and y==[]:
                continue
            else:
                graphs[market+'_'+variety] = x,y
                print(x,y)
                for p in y:
                    all_y.append(int(p))
                for p in x:
                    all_x.append(p)
                #print(all_y)

    #print(all_x)
    dummy_x = sort_dates(all_x)
    dummy_y = [None for el in all_x]
    #print(dummy_y)
    plt.plot(dummy_x,dummy_y)
    for graph in graphs:
        tmp_x = graphs[graph][0]
        tmp_y = graphs[graph][1]
        tmp_y = [int(ely) for ely in tmp_y]
        plt.plot(tmp_x,tmp_y,label =graph+'_modal_price',marker = 'o', markerfacecolor='blue',markersize=6)
        plt.xlabel('Date')
        plt.ylabel('Price(Rs./100kg)')
        plt.title(commodity + ' Prices in ' + userdistrict)
        plt.legend()





    if (all_x):
        plt.ylim(min(all_y) - 300, max(all_y) + 300)
        plt.show()
    else:
        print('No entries found for that commodity.Please try again.')
    print('Would you like to plot a graph for another commodity?\n'
                   '[y/n]')
    option = getoption()
    if (option):
        plotter(state,commodities,userdistrict)



def filefix(state,commodity,district):
    file  = open(state+'_'+district+'_'+commodity+'.csv','r')
    data = file.readlines()
    head = data[0]
    data = data[1:]
    no_dup_data = []
    for line in data:
        if line not in no_dup_data:
            no_dup_data.append(line)
    file.close()
    file = open(state+'_'+district+'_'+commodity+'.csv','w')
    file.write(head)
    for line in no_dup_data:
        file.write(line)
    file.close()
    return





#Get the name of the state as well as the commodity they want to track.

state = getstate()
print(state)


commodities = ['rice','wheat','maize','tomato','paddy','banana']
#commodities = input('Enter the commodities you wish to track seperated by a comma, press enter to continue : ').split(',')

for i in range(len(commodities)):
    commodities[i] = commodities[i].strip().capitalize()
print(commodities)

#track the commodities entered.
results = tracker(state,commodities)
if results == []:
    print('No records found for the parameters given,try again later')
    sys.exit(0)
districts = []
print('Districts found :\n')
for entry in results:
    if entry['district'] not in districts:
        districts.append(entry['district'])
        print(entry['district'])


#get the district they belong to.

print('Enter the district to which you belong or want to track')
userdistrict = geddit(districts)

for commodity in commodities:
    title = [15 * ' ' + 'Market' + 15 * ' ', 10 * ' ' + 'Commodity' + 10 * ' ', 7 * ' ' + 'Variety' + 7 * ' ',10 * ' ' + 'Date' + 10 * ' ', 3*' '+'min_price'+3*' ',3*' '+'max_price'+3*' ',3*' '+'modal_price']
    if not (os.path.isfile(state+'_'+userdistrict+'_'+commodity+'.csv')):
        title = [15 * ' ' + 'Market' + 15 * ' ', 10 * ' ' + 'Commodity' + 10 * ' ', 7 * ' ' + 'Variety' + 7 * ' ',10 * ' ' + 'Date' + 10 * ' ', 3 * ' ' + 'min_price' + 3 * ' ', 3 * ' ' + 'max_price' + 3 * ' ',3 * ' ' + 'modal_price']
        file = open(state+'_'+userdistrict+'_'+commodity+'.csv','w')
        file.write('|'.join(title)+'\n')
        file.close()
    file = open(state+'_'+userdistrict+'_'+commodity+'.csv','a')
    for entry in results:
        if ((entry['district'] == userdistrict) and (commodity in entry['commodity'])):
            file.write(entry['market']+(len(title[0])-len(str(entry['market'])))*' '+'|'+entry['commodity']+(len(title[1])-len(str(entry['commodity'])))*' '+'|'+entry['variety']+(len(title[2])-len(str(entry['variety'])))*' '+'|'+entry['arrival_date']+(len(title[3])-len(str(entry['arrival_date'])))*' '+'|'+str(entry['min_price'])+(len(title[4])-len(str(entry['min_price'])))*' '+'|'+str(entry['max_price'])+(len(title[5])-len(str(entry['max_price'])))*' '+'|'+str(entry['modal_price'])+'\n')
    file.close()
    filefix(state,commodity,userdistrict)

print('Data entered into files.\n\n')

print('Would you like to plot the graph for a given commodity?\n'
                   '[y/n]')
option = getoption()

if (option):
    plotter(state,commodities,userdistrict)

print('END'.center(100,'-'))




