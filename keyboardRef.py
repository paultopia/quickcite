# speedy entry of reference entries and conversion to bibtex or json suitable
# for import into reference managers.  Designed for desktop use to be
# hotkeyed (e.g. via osx automator) and to operate with zero mouse-clicks.
# handles books, articles, chapters.

# work in progress.  UNTESTED

# ISSUES: bibtex is awful (damn near impossible to efficiently enter author
# names, for example).  Maybe use CSL JSON?  For now, just dumping into
# a bibtex file seems like the least terrible choice, and just including
# nonstandard author name components in a miscellaneous tagged field for later
# human correction -- which is horrible, but better than forcing humans to hit
# enter enter enter on a bunch of specific input requests that apply in maybe
# 1% of cases ('enter any von, van, or de' 'enter any Jr, III, etc' 'enter
# any middle names' blah blah blah---not acceptable).  Maybe just parse the
# damn thing with regular expressions after the fact.

import json

def enterCites():
    numEntries = int(raw_input('How many references would you like to add? ').strip())
    refslist = []
    for x in range(numEntries):
        print '-----------------------------------------------------------'
        print 'BEGINNING REFERENCE %s' % x
        print 'How many authors in reference %s? ' % x
        numAuthors = int(raw_input().strip())
        authorlist = []
        for y in range(numAuthors):
            authorlist.append(authorNames(y))
        author1L = authorlist[0][1]
        authors1 = authorlist[0][0]
        xtraAuthors = []
        for y in range(1, numAuthors):
            xtraAuthors.append(authorlist[y][0])
        nthAuthors = ', '.join(xtraAuthors)
        moreNameBits = []
        for y in range(numAuthors):
            moreNameBits.append(authorlist[y][3])
        bonusNameBits = '; '.join(moreNameBits)
        year = int(raw_input('Enter the publication year: ').strip())
        refid = author1L + year + '-' + str(x)

        # THAT COVERS STUFF THAT IS UNIVERSAL, EXCEPT MISC FIELD WHICH SHOULD
        # BE APPENDED TO EACH INDIVIDUAL TYPE AND SHOULD COVER TRANSLATORS AND SUCH
        refType = ''
        while refType != ('a' or 'A' or 'b' or 'B' or 'c' or 'C'):
            print 'What type of reference is ref# %s' % x
            refType = raw_input('Enter A for article, B for book, or C for chapter: ').strip()
        if refType == 'A' or refType == 'a':
            thereftype = 'article'
            title = raw_input('What is the ARTICLE title? ').strip()
            journal = raw_input('What is the JOURNAL title? ').strip()
            volume = raw_input('What is the journal volume number? ').strip()
            number = raw_input('What is the journal issue number (if any)? ').strip()
            page1 = raw_input('What is the first page of the article? ').strip()
            pageN = raw_input('What is the last page of the article? ').strip()
            print 'Please enter any other information (translators, etc.) about reference %s' % x
            miscinfo = raw_input().strip()
            refitem = {'id': refid, 'Type': thereftype, 'Author': authors1, 'Other Authors': nthAuthors,
            'Title': title, 'Year': year, 'Journal': journal, 'Volume': volume, 'Number': number,
            'FirstPage': page1, 'LastPage': pageN, 'MiscNameBits': bonusNameBits, 'MiscInfo': miscinfo}

        if refType == 'B' or refType == 'b':
            thereftype = 'book'
            title = raw_input('What is the book title? ').strip()
            publisher = raw_input('Who is the book publisher? ').strip()
            city = raw_input('What is the city for the publisher? ').strip()
            print 'Please enter any other information (translators, etc.) about reference %s' % x
            miscinfo = raw_input().strip()
            {'Type': thereftype, 'Author': authors1, 'Other Authors': nthAuthors,
            'Title': title, 'Year': year, 'Publisher': publisher, 'City': city,
            'MiscNameBits': bonusNameBits, 'MiscInfo': miscinfo}
        if refType == 'C' or refType == 'c':
            thereftype = 'chapter'
            title = raw_input('What is the CHAPTER title? ').strip()
            booktitle = raw_input('What is the BOOK title? ').strip()
            editors = getEdList()
            publisher = raw_input('Who is the book publisher? ').strip()
            city = raw_input('What is the city for the publisher? ').strip()
            page1 = raw_input('What is the first page of the chapter? ').strip()
            pageN = raw_input('What is the last page of the chapter? ').strip()
            print 'Please enter any other information (translators, etc.) about reference %s' % x
            miscinfo = raw_input().strip()
            {'Type': thereftype, 'Author': authors1, 'Other Authors': nthAuthors,
            'Title': title, 'BookTitle': booktitle, 'Editors': editors, 'FirstPage': page1,
            'LastPage': pageN, 'Year': year, 'Publisher': publisher, 'City': city,
            'MiscNameBits': bonusNameBits, 'MiscInfo': miscinfo}
        refslist.append(refitem)
        # then output here, either by options or just dump to bibtexparser?
        dasjson = json.dumps(refslist)

def authorNames(authNum):
    print 'Enter the first name of author %s: ' % authNum
    authorFirst = raw_input().strip()
    print 'Enter the last name of author %s: ' % authNum
    authorLast = raw_input().strip()
    print 'Enter suffixes, middle names, von van de, etc. of author %s, separated by commas: ' % authNum
    authorMisc = raw_input().strip()
    simpleName = authorFirst + ' ' + authorLast
    return [simpleName, authorLast, authorFirst, authorMisc]
    # maybe a better way to implement this is to ask user if there are special
    # elements in author name, and if so, prompt for all the special crap.

def getEdList():
    numEds = int(raw_input('How many editors for this volume? ').strip())
    edlist = []
    for z in range(numEds):
        editor = raw_input('Enter the full name of the editor in First, Middle, Last, Suffix form')
        edlist.append(editor)
    return '; '.join(edlist)
