import requests
import json
import sys


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

def linsearch(state,commodities,low,high,results):
    sf = False
    for i in range(low,high+1,10):
        print('Iteration :',i//10)
        r = requests.get('https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&offset=' + str(i)+'&limit=10')
        data = json.loads(r.text)
        #print(data['records'])
        records = data['records']

        for entry in records:
            if sf and entry['state']!=state:
                return results
            elif entry['state']==state and commcheck(entry,commodities):
                sf  = True
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
    print('Number of records found :',high)
    low  = 0
    #for commodity in commodities :
    #    binsearch(state,commodity,low,high)
    results = []
    print('Searching the records')
    results = linsearch(state,commodities,low,high,results)
    return results


def filehead(state,userdistrict,commodity):
    file = open(state + '_' + userdistrict + '_' + commodity + '.txt', "r")
    header = file.readline()
    print(header)
    title = ['Market','Commodity','Variety','Date','min_price','max_price','modal_price']
    file.close()
    if header!=title:
        file = open(state + '_' + userdistrict + '_' + commodity + '.txt', "r")
        prevdata = file.readlines()
        print('prevdata :',prevdata)
        file.close()
        file = open(state + '_' + userdistrict + '_' + commodity + '.txt', "w")
        file.write('\t'.join(title)+'\n')
        file.writelines(prevdata)
        file.close()
        return
    else:
        return




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
print('Districts found :')
for entry in results:
    if entry['district'] not in districts:
        districts.append(entry['district'])
        print(entry['district'])

userdistrict = input('Enter the district to which you belong or want to track : ')
userdistrict = userdistrict.capitalize()

for commodity in commodities:
    filehead(state,userdistrict,commodity)
    file = open(state+'_'+userdistrict+'_'+commodity+'.txt',"a")
    for entry in results:
        if ((entry['district'] == userdistrict) and (commodity in entry['commodity'])):
            file.write(entry['market']+'\t'+entry['commodity']+'\t'+entry['variety']+'\t'+entry['arrival_date']+'\t'+str(entry['min_price'])+'\t'+str(entry['max_price'])+'\t'+str(entry['modal_price']))

