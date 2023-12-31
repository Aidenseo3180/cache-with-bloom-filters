'''
Program used to re-organize the data to have count number of the link and create a new excel with it
'''
import csv

def parseExcel():
    filename = 'data/TrainingHistory.csv'
    with open(filename) as f_in, open("data/output.csv", "w") as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        #read each row, write the link by click count number of times to output file
        for row in reader:
            for i in range(int(row[3])):
                writer.writerow([row[0]])

if __name__ == "__main__":
    parseExcel()