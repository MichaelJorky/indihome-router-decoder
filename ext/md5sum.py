#!/usr/bin/env python3

import os
import sys
import hashlib

def md5sum(filename):
    try:
        fh = open(filename, 'rb')
    except IOError as e:
        print('Failed to open {} : {}'.format(filename, str(e)))
        return None

    md5 = hashlib.md5()
    try:
        while True:
            data = fh.read(4096)
            if not data:
                break
            md5.update(data)
    except IOError as e:
        fh.close()
        print('Failed to read {} : {}'.format(filename, str(e)))
        return None
    
    fh.close()
    return md5.hexdigest()

def main():
    if(len(sys.argv) != 2):
        print('Usage: {} <file>'.format(sys.argv[0]))
        sys.exit(-1)

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print('"{}" is not a file'.format(filename))
        sys.exit(-1)

    fh = md5sum(filename)
    if(fh == None):
        print('Failed')
        sys.exit(-1)
        
    print(fh)
    sys.exit(0)

if __name__ == "__main__":
    main()
