class PriceUtils:

    @staticmethod
    def nearest_support(price, supports):

        if not supports:
            return None

        valid = [x for x in supports if x.price < price]

        if not valid:
            return None

        return max(valid, key=lambda x: x.price)

    @staticmethod
    def nearest_resistance(price, resistances):

        if not resistances:
            return None

        valid = [x for x in resistances if x.price > price]

        if not valid:
            return None

        return min(valid, key=lambda x: x.price)