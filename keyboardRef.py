# speedy entry of reference entries and conversion to bibtex or json suitable
# for import into reference managers.  Designed for desktop use to be
# hotkeyed (e.g. via osx automator) and to operate with zero mouse-clicks.
# handles books, articles, chapters.

# work in progress.

# ISSUES: bibtex is awful (damn near impossible to efficiently enter author
# names, for example).  Maybe use CSL JSON?  For now, just dumping into
# a bibtex file seems like the least terrible choice, and just including
# nonstandard author name components in a miscellaneous tagged field for later
# human correction -- which is horrible, but better than forcing humans to hit
# enter enter enter on a bunch of specific input requests that apply in maybe
# 1% of cases ('enter any von, van, or de' 'enter any Jr, III, etc' 'enter
# any middle names' blah blah blah---not acceptable).  Maybe just parse the
# damn thing with regular expressions after the fact.

def enterCites():
    numEntries = int(raw_input('How many references would you like to add? ').strip())
    refslist = []
    for x in range(numEntries):
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

        # THAT COVERS STUFF THAT IS UNIVERSAL, EXCEPT MISC FIELD WHICH SHOULD
        # BE APPENDED TO EACH INDIVIDUAL TYPE AND SHOULD COVER TRANSLATORS AND SUCH
        refType = ''
        while refType != ('a' or 'A' or 'b' or 'B' or 'c' or 'C'):
            refType = raw_input('Enter A for article, B for book, or C for chapter: ').strip()
        if refType == 'A' or refType == 'a':
            # code here
            thereftype = 'article'
            refid = author1L + year + '-' + str(x)
            refitem = {'id': refid, 'Type': thereftype, 'Author': authors1, 'Other Authors': nthAuthors,
            'Title': title, 'Year': year, 'Journal': journal, 'Volume': volume, 'Number': number,
            'Pages': pages, 'MiscNameBits': bonusNameBits}
        if refType == 'B' or refType == 'b':
            # code here
        if refType == 'C' or refType == 'c':
            # code here

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
