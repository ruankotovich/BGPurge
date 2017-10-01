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


class Dataparser:
    products = []
    similarProducts = []
    productsCategories = []
    reviews = []
    groups = {}
    categories = {}

    currentGroupIndex = 0
    currentProduct = None

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

    def parseId(self, text):

        # global currentProduct

        self.currentProduct.id = int(text)

    def parseASIN(self, text):

        # global currentProduct

        self.currentProduct.asin = text

    def parseTitle(self, text):

        # global currentProduct

        self.currentProduct.title = text

    def parseGroup(self, text):

        # global currentGroup
        # global currentGroupIndex

        currentGroup = self.groups.get(text, None)
        if currentGroup != None:
            self.currentProduct.groupId = currentGroup.id
        else:
            self.currentGroupIndex += 1
            curGroup = self.groups[text] = Beans.PGroup()
            curGroup.id = self.currentProduct.groupId = self.currentGroupIndex
            curGroup.description = text

    def parseSalesRank(self, text):

        # global currentProduct

        self.currentProduct.salesrank = int(text)

    def parseSimilar(self, text):

        # global currentProduct
        # global similarProducts

        pieces = text.split('  ')

        for i in range(1, len(pieces)):
            similarObject = Beans.SimilarProducts()
            similarObject.mainProductAsin = self.currentProduct.asin
            similarObject.similarProductAsin = pieces[i]
            self.similarProducts.append(similarObject)

    def parseCategories(self, text):
        if len(text) == 10:
            return

        # global currentProduct
        # global categories

        lastCategoryId = None

        categoriesAphex = text.split('|')

        for cat in range(1, len(categoriesAphex)):
            curCat = categoriesAphex[cat]
            indexLB = curCat.rindex('[')
            indexRB = curCat.rindex(']')

            aphex = (curCat[:indexLB], curCat[indexLB + 1: -1])
            currentCategory = self.categories.get(aphex[1], None)

            if currentCategory == None:
                newCategory = Beans.Category()
                newCategory.superCategory = lastCategoryId
                newCategory.id = aphex[1]
                newCategory.description = aphex[0]
                self.categories[newCategory.id] = newCategory

            lastCategoryId = aphex[1]

        categoryObject = Beans.ProductCategory()
        categoryObject.productId = self.currentProduct.id
        categoryObject.categoryId = lastCategoryId
        self.productsCategories.append(categoryObject)

    def parseReviews(self, text):
        if len(text) == 7:
            return

        reviewSplit = text.split(':')
        newRating = Beans.Review()
        newRating.productId = self.currentProduct.id
        newRating.date = reviewSplit[0][:9]
        newRating.customerId = reviewSplit[1][1:reviewSplit[1].index(
            'r')].strip()
        newRating.rating = int(reviewSplit[2][:reviewSplit[2].index('v')])
        newRating.votes = int(reviewSplit[3][:reviewSplit[3].index('h')])
        newRating.helpful = int(reviewSplit[4])
        self.reviews.append(newRating)

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

    def parseFile(self, filename, factory):
        processed = 0
        lastUpperContext = Context.NONE

        with open(filename) as f:
            for line in f:

                if len(line) < 4:
                    continue

                if line[0: 3] != '   ':
                    rawString = line.strip().split(':', 1)
                else:
                    rawString = line.strip().split("\n")

                curContext = self.switcher.get(rawString[0], Context.NONE)

                if curContext != Context.NONE:
                    lastUpperContext = curContext

                if curContext != Context.ID:
                    if curContext != Context.PURGED:
                        parsingFunction = self.parse[lastUpperContext]

                        if parsingFunction != None:
                            if lastUpperContext != Context.CATEGORIES and lastUpperContext != Context.REVIEWS:
                                parsingFunction(self, rawString[1].strip())
                            else:
                                parsingFunction(self, rawString[0].strip())
                    else:
                        self.currentProduct = None
                else:
                    if self.currentProduct != None:
                        self.products.append(self.currentProduct)
                        processed += 1
                        if processed % 5000 == 0:
                            print "Processed in memory ", processed, " instanzas."
                        if processed % 50000 == 0:
                            print "Dumping..."
                            for p in self.products:
                                factory.insertProduct(p)
                            for sp in self.similarProducts:
                                factory.insertSimilar(sp)
                            for r in self.reviews:
                                factory.insertReview(r)
                            for cat in self.productsCategories:
                                factory.insertProCategory(cat)

                            factory.commit()
                            self.products = []
                            self.similarProducts = []
                            self.reviews = []
                            self.productsCategories = []

                            print "Processed in disk", processed, " instanzas."

                    self.currentProduct = Beans.Product()
                    self.parseId(rawString[1].strip())

            if self.currentProduct != None:
                self.products.append(self.currentProduct)

        print "Dumping the last records..."
        for p in self.products:
            factory.insertProduct(p)
        for sp in self.similarProducts:
            factory.insertSimilar(sp)
        for r in self.reviews:
            factory.insertReview(r)
        for cat in self.productsCategories:
            factory.insertProCategory(cat)
        for key, group in self.groups.iteritems():
            factory.insertGroup(group)
        for key, category in self.categories.iteritems():
            factory.insertCategory(category)

        factory.commit()

        self.products = []
        self.similarProducts = []
        self.reviews = []
        self.productsCategories = []
        print "Processed in disk", processed, " instanzas finally."

        if self.currentProduct != None:
            self.products.append(self.currentProduct)
        self.currentGroupIndex = 0
        self.currentProduct = None

    def printAll(self):
        print "\nProducts : "
        for p in self.products:
            print p.id, ' - ', p.title

        print "\nGroups : "
        for g in self.groups:
            print self.groups[g].id, ' - ', g

        print "\nSimilar Products : "
        for sim in self.similarProducts:
            print sim.mainProductAsin, ' - ', sim.similarProductAsin

        print "\nCategories : "
        for cat in self.categories:
            print cat, ' - ', self.categories[cat].description

        print "\nSubCategories : "
        for subc in self.productsCategories:
            print subc.productId, ' - ', subc.categoryId

        print "\nReviews : "
        for rev in self.reviews:
            print rev.date, ' - ', rev.customerId, ' - ', rev.rating, ' - ', rev.votes, ' - ', rev.helpful
