#!/usr/bin/env python
from os.path import join, dirname
try:
    from robot.libdoc import libdoc
except:
    def main():
        print """Robot Framework 2.7 or later required for generating documentation"""
else:
    def main():
        libdoc('robotpageobjects', 'out.xml')
        #libdoc('../robotframework-selenium2library/src/Selenium2Library', 'out.xml')
        #libdoc('../entrez/entrezpageobjects', 'out.xml')

if __name__ == '__main__':
    main()
