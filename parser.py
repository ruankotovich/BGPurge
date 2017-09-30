import re
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
    PURGED = 10


products = []
similarProducts = []
productsCategories = []
groups = {}
categories = {}
reviews = []


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
    '': Context.NONE
}

currentGroupIndex = 0
currentProduct = None
lastUpperContext = Context.NONE


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
        currentProduct.groupId = currentGroup.id
    else:
        currentGroupIndex += 1
        curGroup = groups[text] = Beans.Group()
        curGroup.id = currentProduct.groupId = currentGroupIndex
        curGroup.description = text


def parseSalesRank(text):

    global currentProduct

    currentProduct.salesrank = int(text)


def parseSimilar(text):

    global currentProduct
    global similarProducts

    pieces = text.split('  ')

    for i in range(1, len(pieces)):
        similarObject = Beans.SimilarProducts()
        similarObject.mainProductAsin = currentProduct.asin
        similarObject.similarProductAsin = pieces[i]
        similarProducts.append(similarObject)


def parseCategories(text):
    if len(text) == 10:
        return

    global currentProduct
    global categories

    categoriesAphex = text.split('|')

    for cat in range(1, len(categoriesAphex)):
        curCat = categoriesAphex[cat]
        indexLB = curCat.index('[')
        indexRB = curCat.index(']')

        aphex = (curCat[0:indexLB] , curCat[indexLB+1:len(curCat)-1])
        currentCategory = categories.get(aphex[1], None)

        if currentCategory != None:
            categoryObject = Beans.ProductCategories()
            categoryObject.productId = currentProduct.id
            categoryObject.categoryId = currentCategory.id
        else:
            newCategory = Beans.Category()
            newCategory.description = aphex[0]
            newCategory.id = aphex[1]
            categories[newCategory.id] = newCategory



parse = {
    Context.ID: parseId,
    Context.ASIN: parseASIN,
    Context.TITLE: parseTitle,
    Context.GROUP: parseGroup,
    Context.SALESRANK: parseSalesRank,
    Context.SIMILAR: parseSimilar,
    Context.CATEGORIES: parseCategories,
    Context.REVIEWS: None,
    Context.PURGED: None,
    Context.NONE: None
}

with open('./docs/simpletest.txt') as f:
    for line in f:

        rawString = line.strip().split(':', 1)
        curContext = switcher.get(rawString[0], Context.NONE)

        if curContext != Context.NONE:
            lastUpperContext = curContext

        if curContext != Context.ID:
            if curContext != Context.PURGED:
                parsingFunction = parse[lastUpperContext]

                if parsingFunction != None:
                    if lastUpperContext != Context.CATEGORIES and lastUpperContext != Context.REVIEWS:
                        parsingFunction(rawString[1].strip())
                    else:
                        parsingFunction(rawString[0].strip())
            else:
                currentProduct = None
        else:
            if currentProduct != None:
                products.append(currentProduct)
            currentProduct = Beans.Product()
            parseId(rawString[1].strip())

if currentProduct != None:
    products.append(currentProduct)

print "\nProducts : "
for p in products:
    print p.id, ' - ', p.title

print "\nGroups : "
for g in groups:
    print groups[g].id, ' - ', g

print "\nSimilar Products : "
for sim in similarProducts:
    print sim.mainProductAsin, ' - ', sim.similarProductAsin

print "\nCategories : "
for cat in categories:
    print cat, ' - ' , categories[cat].description