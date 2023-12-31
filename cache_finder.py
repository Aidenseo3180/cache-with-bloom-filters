import csv

def findCache():
    filename = 'data/output.csv'
    empty_set = set()
    cache_set = set()
    total_number_of_unique_URL = 0
    with open(filename) as f_in, open("data/validCache.csv", "w") as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        #reach each line of output.csv
        for row in reader:
            #if not in empty set, then add it
            if row[0] not in empty_set:
                total_number_of_unique_URL += 1
                empty_set.add(row[0])
            #if it is in empty set, that means we have visited it before so cache it
            else:
                #make sure that it's not already in cache set
                if row[0] not in cache_set:
                    cache_set.add(row[0])

        for element in cache_set:
            writer.writerow([element])         

    print("Total number of unique URL: {0}".format(total_number_of_unique_URL))                    #6383
    print("Total number of URLs that appeared more than once: {0}\n".format(len(cache_set)))         #1261

if __name__ == "__main__":
    findCache()