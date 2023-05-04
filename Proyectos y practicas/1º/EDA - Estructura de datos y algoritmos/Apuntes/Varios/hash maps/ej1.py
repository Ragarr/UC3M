"""un  algoritmo que dado una lista y un valor enco"""
numbers = [2, 4, 6, 10]
target_number = 16

for i, number in enumerate(numbers):
    complementary = target_number - number
    if complementary in numbers[i:]:
        print("Solution Found: {} and {}".format(number, complementary))
        break
else:
    print("No solutions exist")

