import requests
import json
import sys
import os.path


def getstate():
    state = input('Enter the state you live in : ').split()
    for i in range(len(state)):
        state[i] = state[i].capitalize()
    state = ' '.join(state)
    if (checkstate(state)):
        print('Accepted')
        return state
    elif state=='':
        print('Hack')
        return 'Karnataka'
    else:
        print('The state entered is not valid, please try again')
        return getstate()


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





#Get the name of the state as well as the commodity they want to track.

state = getstate()
print(state)


commodities = ['rice','wheat','maize','tomato','paddy']
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

userdistrict = input('Enter the district to which you belong or want to track : ')
userdistrict = userdistrict.capitalize()

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

print('Data entered into files.')

