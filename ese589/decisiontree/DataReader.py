import numpy as np
file=open("data/adult.data")


x = np.array([(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)],
             dtype=[('age', np.int32), ('workclass', np.int32), ('education', np.int32),('educationNum',np.int32),('maritialStatus',np.int32),('occupation',np.int32),('relationship',np.int32),('race',np.int32),('sex',np.int32),('capital_gain',np.int32),('capital_loss',np.int32),('hoursPerWeek',np.int32),('nativeCountry',np.int32),('more50K',np.float64)])

print(x.workclass)


lines = file.readlines()
for line in lines:
    cols = line.split()
    