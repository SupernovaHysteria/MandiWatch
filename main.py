import requests
import json


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
    validstates = ['Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu and Kashmir','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Orissa','Punjab','Rajasthan','Sikkim','Tamil Nadu','Tripura','Uttarakhand','Uttar Pradesh','West Bengal','Andaman and Nicobar Islands','Chandigarh','Dadar and Nagar Haveli','Daman and Diu','Delhi','Lakshadeep','Pondicherry']
    if state in validstates:
        return True
    else:
        return False

#optimization to use binary search to be done later..
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

def linsearch(state,commodities,low,high,results):
    for i in range(low,high+1,10):
        print('iteration :',i//10)
        r = requests.get('https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&offset=' + str(i)+'&limit=10')
        data = json.loads(r.text)
        #print(data['records'])
        records = data['records']
        for entry in records:
            if entry['state']==state and commcheck(entry,commodities):
                results.append(entry)
                print(entry)
    return results




def tracker(state,commodities):
    r = requests.get('https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&offset=0&limit=10')
    data = json.loads(r.text)
    #print(data)
    #for key in data:
    #    print(key,':',data[key])
    high = data['total'] - 10
    print(high)
    low  = 0
    #for commodity in commodities :
    #    binsearch(state,commodity,low,high)
    results = []
    results = linsearch(state,commodities,low,high,results)





#Get the name of the state as well as the commodity they want to track.
state = getstate()
print(state)

commodities = input('Enter the commodities you wish to track seperated by a comma, press enter to continue : ').split(',')
for i in range(len(commodities)):
    commodities[i] = commodities[i].strip().capitalize()
print(commodities)

#track the commodities entered.
tracker(state,commodities)



