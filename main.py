from standard_bloom_filter import *
from counting_bloom_filter import *
from breadth_bloom_filter import *
from cache_finder import *
from excel_parser import *
import time

#NOTE change level, k, and m to test different types of bloom filters
level = 15
k = 10
m = 8000

def main():
    
    '''
    First, turn TrainingHistory.csv found from the website and create output.csv
    '''
    parseExcel()
    print("----------output.csv created from TrainingHistory.csv----------")

    '''
    Next, create a validCache.csv from output.csv. This is to compare validCache.csv with our result at the end
    '''
    findCache()
    print("----------validCache.csv created from output.csv----------\n")

    '''
    Standard Bloom Filter
    '''
    print("----------Standard Bloom Filter----------")
    start = time.perf_counter()
    findStandardBloomFilter(k, m)
    end = time.perf_counter()
    ms = (end - start) * 10**3
    print(f"Execution time: {ms:.03f} ms\n")

    '''
    Counting Bloom Filter
    '''
    print("----------Counting Bloom Filter----------")
    start = time.perf_counter()
    findCountingBloomFilter(k, m)
    end = time.perf_counter()
    ms = (end - start) * 10**3
    print(f"Execution time: {ms:.03f} ms\n")

    '''
    Breadth Bloom Filter
    '''
    print("----------Breadth Bloom Filter----------")
    start = time.perf_counter()
    findBreadthBloomFilter(level, k, m)
    end = time.perf_counter()
    ms = (end - start) * 10**3
    print(f"Execution time: {ms:.03f} ms\n")


if __name__ == "__main__":
    main()