import os
import csv

csv_path = os.path.join("Resources", "budget_data.csv")


letters= []
num = []
with open(csv_path, newline = '') as csvfiles:
    csvread = csv.reader(csvfiles, delimiter = ",")

    next(csvread)
    
    total = 0
    for row in csvread:
        total += int(row[1])
        num.append(row[1])
        letters.append(row[0])


    num_a = list(map(int, num))
    
    num1 = num
    num1.pop(0)
    num_b = list(map(int, num1))
    
    
    num_combined = zip(num_b, num_a)
    num_difference = [x - y for x, y in num_combined]
    num_difference.insert(0,0)
    num_average = sum(num_difference)/len(num_difference)
    num_difference = list(map(int, num_difference))
    dictionary = dict(zip(letters, num_difference))

    num_max = max(zip(dictionary.values(), dictionary.keys()))
    num_min = min(zip(dictionary.values(), dictionary.keys()))

print("Financial Analysis")
print("------------------------")
print("Total Months: " + str(len(letters)))
print("Total: " + "$" + str(total))
print("Average Change: " + "$" + str("%.2f" % num_average))
print("Greatest Increase in Profit: " + str(num_max))
print("Greatest Decrease in Profit: " + str(num_min))
