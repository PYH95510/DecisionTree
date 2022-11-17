import numpy as np
file=open("/Users/yohanpark/git/Decision Tree/ESE589/data/adult.data")


x = np.array([(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)],
             dtype=[('age', np.int32), ('workclass', np.int32), ('education', np.int32),('educationNum',np.int32),('maritialStatus',np.int32),('occupation',np.int32),('relationship',np.int32),('race',np.int32),('sex',np.int32),('capital_gain',np.int32),('capital_loss',np.int32),('hoursPerWeek',np.int32),('nativeCountry',np.int32),('more50K',np.float64)])

data = np.zeros(14, dtype={'names':('age', 'workclass', 'education','educationNum','maritialStatus','occupation','relationship','race','sex','capital_gain','capital_loss','hoursPerWeek','nativeCountry','more50K'),
                          'formats':('i4', 'i4', 'i4','i4','i4','i4','i4','i4','i4','i4','i4','i4','i4','f8')})


print(data['age'])
print(x['age'])

lines = file.readlines()
for line in lines:
    cols = line.split(',')
    if len(cols) == 0:
        continue
    np.append(x,cols[0],cols[1],cols[3],cols[4],cols[5],cols[6],cols[7],cols[8],cols[9],cols[12],cols[13],cols[14],axis=0)



