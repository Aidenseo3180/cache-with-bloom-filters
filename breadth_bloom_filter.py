import numpy as np
import mmh3
import csv
import sys

class BloomFilter:
    def __init__(self, level:int = 15, k:int = 10, m:int=100000):
        """
        :param k: The number of hash functions (rows).
        :param m: The number of buckets (cols).

        Initializes the bloom filter to all zeros, as a
        boolean array where True = 1 and False = 0.
        
        """
        self.k = k
        self.m = m
        self.level = level
        self.t = np.zeros((level, k, m), dtype=bool)

    def hashing(self, x, i:int) -> int:

        return mmh3.hash(str(x), i) % self.m

    def insert(self, x, level_cnt):

        for i in range(self.k):
            idx = self.hashing(x, i)
            self.t[level_cnt][i][idx] = 1

            #also put into BBF0 bc it ORs all the BBFs
            self.t[0][i][idx] = 1

    def check(self, url) -> bool:

        temp_list = url.split('/')
        for item in temp_list:
            if item == "":
                continue
            for i in range(self.k):
                idx = self.hashing(item,i)
                #check BBF0, see if it' 1
                if (self.t[0][i][idx] != 1):
                    return False

        #if all elements are in BBF0 -> check each level now
        cnt = 1
        for item in temp_list:
            if item == "":
                continue

            for i in range(self.k):
                idx = self.hashing(item,i)
                #check BBF0, see if it' 1
                if (self.t[cnt][i][idx] != 1):
                    return False

            cnt += 1
        
        return True
    
def findBreadthBloomFilter(level, k, m):
    filename = 'data/output.csv'

    # Create a new bloom filter structure.
    bf = BloomFilter(level, k, m)

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
            #split the URL by slash
            temp_list = row[0].split('/')
            #level cnt to indicate which level it's in. Starts from 1 bc 0 is used for overall BBFs
            level_cnt = 1
            for item in temp_list:
                if item=="":
                    continue
                bf.insert(item, level_cnt)
                level_cnt += 1

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

    fpr = count / len(valid_cache_set) if count / len(valid_cache_set) < 1 else 1
    print("Valid number of cached URLs: {0}, Total number of incorrectly cached URLs: {1}, FPR: {2}".format(len(valid_cache_set), count, fpr))
    print("Memory usage: {0} Bytes".format(sys.getsizeof(bf.t)))


if __name__ == '__main__':

    for i in range (1, 11):
        print("----------------")
        for j in range(1000, 8001, 1000):
            print(i, j)
            findBreadthBloomFilter(15, i, j) # 5 * 10 * 8,000 = 400,000 bits = 400 KB


'''
Ex.
If there are 3 URL:
https://web.facebook.com/?_rdc=1&_rdr
https://www.udebug.com/URI
https://www.udebug.com/Home

Then BBF does:
              https:                        level 1
           /         \
   web.facebook.com   www.udebug.com        level 2
        /               /       \
   ?_rdc=1&_rdr        Home     URI         level 3

Later on, level 0 = level1 OR level2 OR level3   

'''