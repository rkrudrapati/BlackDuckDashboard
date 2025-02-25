import numpy as np

# Q1
# c = np.arange(start= 1, stop=7).reshape(2, 3)
# # print(c)
# d = np.array([[1, 2, 3], [4, 5, 6]])
# print(np.add(c, d))

## Q2
# t1 = (1, 2, "tuple", 4)
# t2 = (5, 6, 7)
# x = t2[t1[1]]
# t3 = t1 + t2
# t3 = (t1, t2)
# t3 = (list(t1), list(t2))
# print(t3)


## Q3
# d1 = {1: "Pyhton", 2: [1, 2, 3]}
# d1[2].append(4)     # no error
# # x = d1[0]           # error
# d1["one"] = 1       # no error
# d1.update({'one': 2})   # no error

## Q4
# s1 = {1, 2, 3}
# s2 = {5, 6, 3}
# s1.add(4)
# s2.add("4")
# print(s1-s2)

## Q5
# s1 = "Hello"
# s2 = "World"
# print(s1 + " " + s2)
# print(s1[0:] + " " + s2[0:])
# print("{} {}".format(s1, s2))
# print(s1[:-1] + " " + s2[:-1])

## Q6
# arr = np.array([[1, 9, 10], [3, 7, 6], [12, 8, 0]])
# # output = [16 24 16]
# print(arr[1:2])
# print(np.sum(arr, axis=0))
# print(np.sum(arr, axis=1))
# print(np.sum([[1, 9, 10], [3, 7, 6], [12, 8, 0]]))

## Q7
# mat = np.matrix("5, 9, 10; 2, 5, 4; 1, 9, 8; 2, 6, 8")
# mat1 = np.matrix("1, 2, 3, 4")
# mat2 = np.insert(mat, 1, mat1, axis=1)
# print(mat2)
# # axis 1 => vertical
# # insert operation at position 1

## Q8
# student = {'name': 'Jane', 'age': 25, 'courses': ['Math', 'Statistics']}
# # Output: {'name': 'Jane', 'age': 26, 'courses': ['Math', 'Statistics'], 'phone': '123-456'}
# # student.update({'age': 26, 'phone': '123-456'})
# # print(student)
# student['phone'] = '123-456'
# student.update({'age': 26})
# print(student)

## Q9
c = np.arange(start=1, stop=20, step=3)
print(c[5])

