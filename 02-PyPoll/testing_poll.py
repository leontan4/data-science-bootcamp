import os
import csv


csvpath = os.path.join("Resources", "election_data.csv")

df_election = []
testing = []
with open(csvpath, newline ='') as csvfile:
    csvread = csv.reader(csvfile, delimiter = ",")
    next(csvread)

    for row in csvread:
        testing.append(row[2])
    print(testing)
    
    # for row in csvread:
    #     df_election.append(row)
    # # print(len(df_election))
    # print(df_election)
    # # def amount(election_data):
    