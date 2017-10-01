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
        curGroup = groups[text] = Beans.PGroup()
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

    lastCategoryId = None

    categoriesAphex = text.split('|')

    for cat in range(1, len(categoriesAphex)):
        curCat = categoriesAphex[cat]
        indexLB = curCat.index('[')
        indexRB = curCat.index(']')

        aphex = (curCat[:indexLB], curCat[indexLB + 1: -1])
        currentCategory = categories.get(aphex[1], None)

        if currentCategory == None:
            newCategory = Beans.Category()
            newCategory.superCategory = lastCategoryId
            newCategory.id = aphex[1]
            newCategory.description = aphex[0]
            categories[newCategory.id] = newCategory

        lastCategoryId = aphex[1]

    categoryObject = Beans.ProductCategory()
    categoryObject.productId = currentProduct.id
    categoryObject.categoryId = lastCategoryId
    productsCategories.append(categoryObject)


def parseReviews(text):
    if len(text) == 7:
        return

    reviewSplit = text.split(':')
    newRating = Beans.Review()

    newRating.date = reviewSplit[0][:9]
    newRating.customerId = reviewSplit[1][1:reviewSplit[1].index('r')]
    newRating.rating = int(reviewSplit[2][:reviewSplit[2].index('v')])
    newRating.votes = int(reviewSplit[3][:reviewSplit[3].index('h')])
    newRating.helpful = int(reviewSplit[4])

    reviews.append(newRating)


parse = {
    Context.ID: parseId,
    Context.ASIN: parseASIN,
    Context.TITLE: parseTitle,
    Context.GROUP: parseGroup,
    Context.SALESRANK: parseSalesRank,
    Context.SIMILAR: parseSimilar,
    Context.CATEGORIES: parseCategories,
    Context.REVIEWS: parseReviews,
    Context.PURGED: None,
    Context.NONE: None
}

processed = 0

with open('./docs/simpletest.txt') as f:
    for line in f:

        if len(line) < 4:
            continue

        if line[0: 3] != '   ':
            rawString = line.strip().split(':', 1)
        else:
            rawString = line.strip().split("\n")

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
            processed += 1
            currentProduct = Beans.Product()
            parseId(rawString[1].strip())
            
            if processed % 1000 == 0:
                print "Processed ", processed, " products."



if currentProduct != None:
    products.append(currentProduct)

# print "\nProducts : "
# for p in products:
#     print p.id, ' - ', p.title

# print "\nGroups : "
# for g in groups:
#     print groups[g].id, ' - ', g

# print "\nSimilar Products : "
# for sim in similarProducts:
#     print sim.mainProductAsin, ' - ', sim.similarProductAsin

# print "\nCategories : "
# for cat in categories:
#     print cat, ' - ', categories[cat].description

# print "\nSubCategories : "
# for subc in productsCategories:
#     print subc.productId, ' - ', subc.categoryId

# print "\nReviews : "
# for rev in reviews:
#     print rev.date, ' - ', rev.customerId, ' - ', rev.rating, ' - ', rev.votes, ' - ', rev.helpful
