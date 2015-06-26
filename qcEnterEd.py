# simple script to quickly enter academic citations on Edtorial app (IOS)
# saves a file to dropbox in JSON format with as many citations as you want to add.
# this can then be put into bibtex, processed directly, etc.
# rationale: entering stuff into citation managers sucks.  Too much clicking,
# too many agonizing drop-down menus, too much friction. Death to friction.

# DEPENDENCIES:
# 1.  processes file created with editorial workflow "reference-entry" at
# http://www.editorial-workflows.com/workflow/5215161153486848/FHMWei8dy9w
#
# 2.  is meant to be called by an editorial workflow yet to be written, which
# will select all the text created by reference-entry and replace with the
# json string output by this script.
#
# 3.  modules "workflow" and "editor" internal to editorial app

# AS YET UNTESTED.  WORK IN PROGRESS.



import workflow
import editor
import re
import json
thefile = editor.get_text()
isBookMatch = '[[BOOK]]'
isArticleMatch = '[[ARTICLE]]'

if isBookMatch in thefile:
    reftype = 'book'
elif isArticleMatch in thefile:
    reftype = 'article'
else:
    reftype = 'chapter'

# books and general
authorsMatch = r'\[\[AUTHORS= *(.*?) *\]\]'
bookTitleMatch = r'\[\[TITLE= *(.*?) *\]\]'
yearMatch = r'\[\[YEAR= *(.*?) *\]\]'
bookPublisherMatch = r'\[\[PUBLISHER= *(.*?) *\]\]'
bookPublisherCityMatch = r'\[\[PUBLISHER CITY= *(.*?) *\]\]'

# special for articles
articleTitleMatch = r'\[\[ARTICLE TITLE= *(.*?) *\]\]'
journalTitleMatch = r'\[\[JOURNAL TITLE= *(.*?) *\]\]'
volumeMatch = r'\[\[VOLUME= *(.*?) *\]\]'
issueNumberMatch = r'\[\[NUMBER= *(.*?) *\]\]'
pagesMatch = r'\[\[PAGES= *(.*) *\]\]'  #  also used in chapters

# special for chapters
chapterTitleMatch = r'\[\[CHAPTER TITLE= *(.*?) *\]\]'
editedBookEditorMatch = r'\[\[BOOKEDITOR= *(.*?) *\]\]'
editedBookTitleMatch = r'\[\[BOOKTITLE= *(.*?) *\]\]'

authorline = re.search(authorsMatch, thefile)
authors = authorline.group(1)
yearline = re.search(yearMatch, thefile)
year = yearline.group(1)

if reftype == 'book':
    titleline = re.search(bookTitleMatch, thefile)
    title = titleline.group(1)
    publisherline = re.search(bookPublisherMatch, thefile)
    publisher = publisherline.group(1)
    cityline = re.search(bookPublisherCityMatch, thefile)
    city = cityline.group(1)
    reference = {'Type': reftype, 'Authors': authors, 'Title': title, 'Year': year, 'Publisher': publisher, 'City': city}

if reftype == 'article':
    titleline = re.search(articleTitleMatch, thefile)
    title = titleline.group(1)
    journalline = re.search(journalTitleMatch, thefile)
    journal = journalline.group(1)
    volumeline = re.search(volumeMatch, thefile)
    volume = volumeline.group(1)
    numberline = re.search(issueNumberMatch, thefile)
    number = numberline.group(1)
    pagesline = re.search(pagesMatch, thefile)
    pages = pagesline.group(1)
    reference = {'Type': reftype, 'Authors': authors, 'Title': title, 'Year': year, 'Journal': journal, 'Volume': volume, 'Number': number, 'Pages': pages}

if reftype == 'chapter':
    titleline = re.search(chapterTitleMatch, thefile)
    title = titleline.group(1)
    publisherline = re.search(bookPublisherMatch, thefile)
    publisher = publisherline.group(1)
    cityline = re.search(bookPublisherCityMatch, thefile)
    city = cityline.group(1)
    pagesline = re.search(pagesMatch, thefile)
    pages = pagesline.group(1)
    bookeditorline = re.search(editedBookEditorMatch, thefile)
    editor = bookeditorline.group(1)
    booktitleline = re.search(editedBookTitleMatch, thefile)
    booktitle = booktitleline.group(1)
    reference = {'Type': reftype, 'Authors': authors, 'Title': title, 'Year': year, 'Editors': editor, 'Book-title': booktitle, 'Pages': pages, 'Publisher': publisher, 'City': city}


# SEND TO JSON:

refline = json.dumps(reference)
workflow.set_output(refline)
