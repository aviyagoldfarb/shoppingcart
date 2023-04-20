
class ShoppingCart:

    def __init__(self, shopping_dict=None):
        self._shopping_dict = shopping_dict if shopping_dict else {}

    @property
    def shopping_dict(self):
        return self._shopping_dict

    @shopping_dict.setter
    def shopping_dict(self, shopping_dict):
        self._shopping_dict = shopping_dict

    def add_product(self, product_name, quantity=1):
        if product_name in self._shopping_dict:
            added = 0
        else:
            self._shopping_dict[product_name] = quantity
            added = quantity
        return added

    def update_product(self, product, quantity=1):
        if product in self._shopping_dict:
            self._shopping_dict[product] += quantity
            total = self._shopping_dict[product]
        else:
            total = 0
        return total

    def remove_product(self, product, quantity=1):
        if product in self._shopping_dict:
            current_quantity = self._shopping_dict[product]
            if current_quantity - quantity <= 0:
                del self._shopping_dict[product]
                removed = current_quantity
            else:
                self._shopping_dict[product] -= quantity
                removed = quantity
            return removed
        else:
            return 0

    def get_products_num(self):
        return len(self._shopping_dict.keys())

    def reset_shopping_cart(self):
        self._shopping_dict = {}
