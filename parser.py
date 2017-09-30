import beans as Beans
from enum import Enum


class Context(Enum):
    NONE = 0,
    ID = 1,
    ASIN = 2,
    TITLE = 3,
    GROUP = 4,
    SALESRANK = 5,
    SIMILAR = 6,
    CATEGORIES = 7,
    REVIEWS = 8,
    NEW = 9
    PURGED = 10


products = {}
similarProducts = {}
productsCategories = {}
groups = {}
categories = {}
reviews = {}


switcher = {
    'Id': Context.ID,
    'ASIN': Context.ASIN,
    'title': Context.TITLE,
    'group': Context.GROUP,
    'salesrank': Context.SALESRANK,
    'similar': Context.SIMILAR,
    'categories': Context.CATEGORIES,
    'reviews': Context.REVIEWS,
    'discontinued product': Context.PURGED,
    '': Context.NEW
}

currentGroupIndex = 0
currentProduct = None


def parseId(text):

    global currentProduct

    currentProduct.id = int(text)


def parseASIN(text):

    global currentProduct

    currentProduct.asin = text


def parseTitle(text):

    global currentProduct

    currentProduct.title = text


def parseGroup(text):

    global currentGroup
    global currentGroupIndex
    currentGroup = groups.get(text, None)
    if currentGroup != None:
        currentProduct.groupId = currentGroup
    else:
        currentGroupIndex += 1
        curGroup = groups[text] = Beans.Group()
        curGroup.id = currentProduct.groupId = currentGroupIndex
        curGroup.description = text


parse = {
    Context.ID: parseId,
    Context.ASIN: parseASIN,
    Context.TITLE: parseTitle,
    Context.GROUP: parseGroup,
    Context.SALESRANK: None,
    Context.SIMILAR: None,
    Context.CATEGORIES: None,
    Context.REVIEWS: None,
    Context.PURGED: None,
    Context.NEW: None,
    Context.NONE: None
}

curContext = Context.NONE
with open('./docs/simpletest.txt') as f:
    for line in f:

        rawString = line.strip().split(':', 1)
        lastContext = curContext
        curContext = switcher.get(rawString[0], Context.NONE)

        if curContext != Context.ID:

            parsingFunction = parse[curContext]

            if parsingFunction != None:

                parsingFunction(rawString[1].strip())
        else:
            currentProduct = Beans.Product()
            currentCategory = Beans.Category()
            parseId(rawString[1].strip())
            products[currentProduct.id] = currentProduct

print "Products : "
for p in products:
    print p, ' - ', products[p].title

print "Groups : "
for g in groups:
    print groups[g].id, ' - ', g
