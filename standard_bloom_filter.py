import numpy as np
import mmh3
import csv
import sys

total_number_of_unique_url = 6383

class BloomFilter:
    def __init__(self, k:int = 10, m:int=100000):
        """
        :param k: The number of hash functions (rows).
        :param m: The number of buckets (cols).

        Initializes the bloom filter to all zeros, as a
        boolean array where True = 1 and False = 0.
        
        """
        self.k = k
        self.m = m
        self.t = np.zeros((k, m), dtype=bool)

    def hashing(self, x, i:int) -> int:

        return mmh3.hash(str(x), i) % self.m

    def insert(self, x):
        for i in range(self.k):
            idx = self.hashing(x, i)
            self.t[i][idx] = 1

    def check(self, url) -> bool:

        for i in range(self.k):
            idx = self.hashing(url,i)
            if (self.t[i][idx] != 1):
                return False

        return True
    
def findStandardBloomFilter(k, m):
    filename = 'data/output.csv'

    # Create a new bloom filter structure.
    bf = BloomFilter(k, m)

    cache_list = []

    # Create our bloom filter of URL
    with open(filename) as f_in:
        reader = csv.reader(f_in)
        for row in reader:

            #if already in cache list, then skip
            if row[0] in cache_list:
                continue

            #if not in cache list but we're visiting the same URL again(now we know that it should be cached), then insert to cache list
            if bf.check(row[0]):
                cache_list.append(row[0])   #append the whole URL, not current_row that doesnt have https in front
                continue
            
            #otherwise, add to bloom filter
            bf.insert(row[0])

    #valid cache list that I will use to compare our program's false positive rate
    cache_filename = 'data/validCache.csv'
    valid_cache_set = set()
    with open(cache_filename) as f_in:
        reader = csv.reader(f_in)
        for row in reader:
            if (row[0] not in valid_cache_set):
                valid_cache_set.add(row[0])
    
    count = 0

    for element in cache_list:
        if element not in valid_cache_set:
            count += 1

    expected_fpr = pow(1 - pow(1 - 1/m, total_number_of_unique_url), k)
    print("Expected FPR: {0:.5f}".format(expected_fpr))
    fpr = count / len(valid_cache_set) if count / len(valid_cache_set) < 1 else 1
    print("Valid number of cached URLs: {0}, Total number of incorrectly cached URLs: {1}, Actual FPR: {2}".format(len(valid_cache_set), count, fpr))
    print("Memory usage: {0} Bytes".format(sys.getsizeof(bf.t)))

if __name__ == '__main__':

    for i in range (1, 11):
        print("----------------")
        for j in range(1000, 8001, 1000):
            print(i, j)
            findStandardBloomFilter(i, j) # 10 * 8,000 = 80,000 bits = 10 KB

