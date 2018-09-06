import os
import csv


csvpath = os.path.join("Resources", "election_data.csv")


testing = []
with open(csvpath, newline ='') as csvfile:
    csvread = csv.reader(csvfile, delimiter = ",")
    next(csvread)

    for row in csvread:
        testing.append(row[2])
        my_dict = {i:testing.count(i) for i in testing}
        def percentage(x, y):
            percentage = (x/y)*100
            return percentage

    percentage_khan = percentage(my_dict["Khan"], len(testing))
    percentage_correy = percentage(my_dict["Correy"], len(testing))
    percentage_li = percentage(my_dict["Li"], len(testing))
    percentage_tooley = percentage(my_dict["O'Tooley"], len(testing))

    vote_khan = my_dict["Khan"]
    vote_correy = my_dict["Correy"]
    vote_li = my_dict["Li"]
    vote_tooley = my_dict["O'Tooley"]

    highest_vote = max(my_dict, key = my_dict.get)

print("Election Results")
print("------------------------------")
print("Total Votes: " + str(len(testing)))
print("------------------------------")
print("Khan: " + str("%.2f" % percentage_khan) + "% " + "(" + str(vote_khan) + ")")
print("Correy: " + str("%.2f" % percentage_correy) + "% "+ "(" + str(vote_correy) + ")")
print("Li: " + str("%.2f" % percentage_li) + "% "+ "(" + str(vote_li) + ")")
print("O'Tooley: " + str("%.2f" % percentage_tooley) + "% "+ "(" + str(vote_tooley) + ")")
print("------------------------------")
print("Winner: " + str(highest_vote))