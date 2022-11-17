import numpy as np
file=open("/Users/yohanpark/git/Decision Tree/ESE589/data/adult.data")


x = np.array([(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)],
             dtype=[('age', np.int32), ('workclass', (np.str_, 10)), ('education', (np.str_, 10)),('educationNum',(np.str_, 10)),('maritialStatus',(np.str_, 10)),('occupation',(np.str_, 10)),('relationship',(np.str_, 10)),('race',(np.str_, 10)),('sex',(np.str_, 10)),('capital_gain',(np.str_, 10)),('capital_loss',np.int32),('hoursPerWeek',np.int32),('nativeCountry',(np.str_, 10)),('more50K',(np.str_, 10))])

data = np.zeros(14, dtype={'names':('age', 'workclass', 'education','educationNum','maritialStatus','occupation','relationship','race','sex','capital_gain','capital_loss','hoursPerWeek','nativeCountry','more50K'),
                          'formats':('i4', 'i4', 'i4','i4','i4','i4','i4','i4','i4','i4','i4','i4','i4','f8')})


print(data['age'])
print(x['age'])

lines = file.readlines()
for line in lines:
    cols = line.split(',')
    if len(cols) == 0:
        continue
    tmtarray = np.array([(cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[7], cols[8], cols[9], cols[10], cols[11], cols[12], cols[13])],
             dtype=[('age', np.int32), ('workclass','U20'), ('education', (np.str_, 10)),('educationNum',(np.str_, 10)),('maritialStatus',(np.str_, 10)),('occupation',(np.str_, 10)),('relationship',(np.str_, 10)),('race',(np.str_, 10)),('sex',(np.str_, 10)),('capital_gain',(np.str_, 10)),('capital_loss',np.int32),('hoursPerWeek',np.int32),('nativeCountry',(np.str_, 10)),('more50K',(np.str_, 10))])
    x = np.append(x,tmtarray,axis=0)

print(x)

    

    



