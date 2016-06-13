#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

import doctest, os, sys, glob
import click

"""
This will doctest all files ending with .rst in this directory.
"""

@click.command()
@click.option('-f', '--file_paths', help="specific rst files to test")
@click.option('-j', '--just', help='comma separated list of names to be matched to files to be tested')
@click.option('-x', '--exclude', help='comma separated list of names to be matched to files to be excluded')
@click.option('-v', '--verbose', is_flag=True, help='verbose output')
def main(file_paths, just, exclude, verbose):
    """runs doctests for the indicated files"""
    if not file_paths:
        # find all files that end with rest
        file_paths = [fname for fname in os.listdir(os.getcwd()) if fname.endswith('.rst')]
    elif "*" in file_paths:
        file_paths = glob.glob(file_paths)
    
    if verbose:
        print file_paths
    
    if just:
        just = just.split(',')
        new = []
        for fn in file_paths:
            for sub_word in just:
                if sub_word in fn:
                    new.append(fn)
        file_paths = new
    elif exclude:
        exclude = exclude.split(',')
        new = []
        for fn in file_paths:
            keep = True
            for sub_word in exclude:
                if sub_word in fn:
                    keep = False
                    break
            if keep:
                new.append(fn)
        file_paths = new
    
    if verbose:
        print "File paths, after filtering: %s" % str(file_paths)
    
    for test in file_paths:
        print
        print "#" * 40
        print test
        doctest.testfile(test, optionflags=doctest.ELLIPSIS, verbose=True, encoding='utf-8')
    

if __name__ == "__main__":
    main()
