#!/usr/bin/env python3

import concurrent.futures
import hashlib
import os
import string
import sys
import argparse

# Constants

ALPHABET = string.ascii_lowercase + string.digits

# Functions

def usage(exit_code=0):
    progname = os.path.basename(sys.argv[0])
    print(f'''Usage: {progname} [-a ALPHABET -c CORES -l LENGTH -p PATH -s HASHES]
    -a ALPHABET Alphabet to use in permutations
    -c CORES    CPU Cores to use
    -l LENGTH   Length of permutations
    -p PREFIX   Prefix for all permutations
    -s HASHES   Path of hashes file''')
    sys.exit(exit_code)

def md5sum(s):
    ''' Compute md5 digest for given string. '''
    # TODO: Use the hashlib library to produce the md5 hex digest of the given
    # string.
    return hashlib.md5(s.encode('utf-8')).hexdigest() 

def permutations(length, alphabet=ALPHABET):
    ''' Recursively yield all permutations of the given length using the
    provided alphabet. '''
    # TODO: Use yield to create a generator function that recursively produces
    # all the permutations of the given length using the provided alphabet.
    for letter in alphabet:
        index = alphabet.index(letter)
        if length == 0:
            yield ''
            return
        for i in permutations(length -1, alphabet[:index] + alphabet[index:]):
            yield letter + i
        

def flatten(sequence):
    ''' Flatten sequence of iterators. '''
    # TODO: Iterate through sequence and yield from each iterator in sequence.
    for item in sequence:
        yield from item

def crack(hashes, length, alphabet=ALPHABET, prefix=''):
    ''' Return all password permutations of specified length that are in hashes
    by sequentially trying all permutations. '''
    # TODO: Return list comprehension that iterates over a sequence of
    # candidate permutations and checks if the md5sum of each candidate is in
    # hashes.
    
    return [prefix+x for x in permutations(length, alphabet) if md5sum(prefix+x) in hashes]


def cracker(arguments):
    ''' Call the crack function with the specified arguments '''
    return crack(*arguments)

def smash(hashes, length, alphabet=ALPHABET, prefix='', cores=1):
    ''' Return all password permutations of specified length that are in hashes
    by concurrently subsets of permutations concurrently.
    '''
    # TODO: Create generator expression with arguments to pass to cracker and
    # then use ProcessPoolExecutor to apply cracker to all items in expression.

    arguments = ((hashes, length-1, alphabet, prefix+letter) for letter in alphabet)
    
    with concurrent.futures.ProcessPoolExecutor(cores) as executor:
        results = executor.map(cracker, arguments)
        results = flatten(results)

    return results

def main():
    arguments = sys.argv[1:]
    # TODO: Parse command line arguments
    #using argparse
    parser = argparse.ArgumentParser(description='hulk.py')

    parser.add_argument('-a', type=str, dest='alphabet', default=ALPHABET, help='Alphabet to use in permutations')

    parser.add_argument('-c', type=int, dest='cores', default=1, help='CPU Cores to use')

    parser.add_argument('-l', type=int, dest='length', default=1, help='Length of permutations')

    parser.add_argument('-p', type=str, dest='prefix', default='', help='Prefix for all permutations')

    parser.add_argument('-s', type=str, dest='hashes_path', default='hashes.txt', help='Path of hashes file')
    
    args = parser.parse_args()

    # TODO: Load hashes set
    #hashes_set is the set of all hashes
    hashes_set = set()
    for line in open(args.hashes_path):
        line = line.strip()
        hashes_set.add(line)

    # TODO: Execute crack or smash function
    if args.cores > 1:
        perms = smash(hashes_set, args.length, args.alphabet, args.prefix, args.cores)
    else:
        perms = crack(hashes_set, args.length, args.alphabet, args.prefix)

    # TODO: Print all found passwords
    for i in perms:
        print(i)

# Main Execution
if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
