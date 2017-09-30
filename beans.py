class Product:
    id = None  # pk
    title = None
    asin = None  # df this->id
    groupId = None  # fk_group
    salesrank = None  # df this->id


class SimilarProducts:
    mainProductAsin = None  # pk #fk_product
    similarProductAsin = None  # pk #fk_product


class ProductCategories:
    productId = None  # pk #fk_product
    categoryId = None  # pk #fk_category


class Group:
    id = None  # pk
    description = None  # df this->id


class Category:
    id = None  # pk
    description = None  # df this->id


class Review:
    productId = None  # pk #fk_product
    customerId = None  # pk
    date = None  # df this->id
    rating = None  # df this->id
    votes = None  # df this->id
    helpful = None  # df this->id
