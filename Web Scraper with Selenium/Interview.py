import numpy as np

mat1=np.arange(16).reshape(4,4)
mat2=np.arange(8,24).reshape(4,4)


for i in range(mat1.shape[0]):
    for j in range(mat1.shape[1]):
        for x in range(mat2.shape[0]):
            for y in range(mat2.shape[1]):
                if mat1[i,j]==mat2[x,y]:
                    print(mat1[i,j])

for item in mat2:
    for i in range(mat1.shape[0]):
        for j in range(mat1.shape[1]):
            if mat1[i,j] in item:
                print(mat1[i,j])