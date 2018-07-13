ass = ['jack','ass']
if 'ass' in ass:
    print('yeaa')
else:
    print('nah')

file =  open('Karnataka_Bangalore_Maize.txt','r')
print(file.readline().split())
header = file.readline().split()
head = ['Market','Commodity','Variety','Date','min_price','max_price','modal_price']
print(header != head)
if header != head:
    file.close()
    file = open('Karnataka_Bangalore_Maize.txt', 'r')
    tempdata = file.readlines()
    print(tempdata)
    file.close()
    file = open('Karnataka_Bangalore_Maize.txt','w')
    file.write('\t'.join(head)+'\n')
    file.writelines(tempdata)
    file.close()

print(4*'=')