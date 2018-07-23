import numpy as np

ass = ['jack','ass']
if 'ass' in ass:
    print('yeaa')
else:
    print('nah')



print(4*'=')
print(abs(ord('A')-ord('U')))

random = [1,2,3,4,5,6,7,8,9,10]
for item in random[::-1]:
    print(item)

title = [15 * ' ' + 'Market' + 15 * ' ', 10 * ' ' + 'Commodity' + 10 * ' ', 7 * ' ' + 'Variety' + 7 * ' ',10 * ' ' + 'Date' + 10 * ' ', 3 * ' ' + 'min_price' + 3 * ' ', 3 * ' ' + 'max_price' + 3 * ' ',3 * ' ' + 'modal_price']
file = open('Karnataka'+'_'+'Bangalore'+'_'+'Tomato'+'.csv','w')
file.write('|'.join(title)+'\n')
file.close()
title = [15 * ' ' + 'Market1' + 15 * ' ', 10 * ' ' + 'Commodity' + 10 * ' ', 7 * ' ' + 'Variety' + 7 * ' ',10 * ' ' + 'Date' + 10 * ' ', 3 * ' ' + 'min_price' + 3 * ' ', 3 * ' ' + 'max_price' + 3 * ' ',3 * ' ' + 'modal_price']
file = open('Karnataka'+'_'+'Bangalore'+'_'+'Tomato'+'.csv','a')
file.write('|'.join(title)+'\n')
file.close()
title = [15 * ' ' + 'Market2' + 15 * ' ', 10 * ' ' + 'Commodity' + 10 * ' ', 7 * ' ' + 'Variety' + 7 * ' ',10 * ' ' + 'Date' + 10 * ' ', 3 * ' ' + 'min_price' + 3 * ' ', 3 * ' ' + 'max_price' + 3 * ' ',3 * ' ' + 'modal_price']
file = open('Karnataka'+'_'+'Bangalore'+'_'+'Tomato'+'.csv','a')
file.write('|'.join(title)+'\n')
file.close()

file = open('Karnataka'+'_'+'Bangalore'+'_'+'Tomato'+'.csv','r')
raw_data = file.readlines()
print(raw_data)
rows = []
for line in raw_data:
    data = (line.split('|'))
    print(data)
    row = []
    for e in data:

        print(type(e))
        row.append(e.strip())
    rows.append(row)

print(rows)

del(rows[0])
print(rows)

def scrub():
    return [2,3,4,5],[7,9,8,0]

x,y = scrub()

print(x,'nub',y)

wew = {}
wew['one'] = x,y
print(wew['one'][0])
gg = [1,34,6644,None,435,None,345,88,None]

print(np.isfinite(np.array(gg).astype(float)))
gg = [1,3,4,2]
if (gg):
    print("hi")
else:
    print('bye')