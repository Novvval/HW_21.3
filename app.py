from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def __init__(self, items, capacity):
        self._items = items
        self._capacity = capacity

    @abstractmethod
    def add(self, name, quantity):
        pass

    @abstractmethod
    def remove(self, name, quantity):
        pass

    @property
    @abstractmethod
    def get_free_space(self):
        pass

    @property
    @abstractmethod
    def get_items(self):
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 100

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, data):
        self._items = data
        self._capacity -= sum(self._items.values())

    def add(self, name, quantity):
        if name in self._items:
            self._items[name] += quantity
        else:
            self._items[name] = quantity
        self._capacity -= quantity

    def remove(self, name, quantity):
        self._items[name] -= quantity
        if self._items[name] < 0:
            del self._items[name]
        self._capacity += quantity

    @property
    def get_free_space(self):
        return self._capacity

    @property
    def get_items(self):
        return self._items

    @property
    def get_unique_items_count(self):
        return len(self._items.keys())


class Shop(Store):
    def __init__(self):
        super().__init__()
        self._capacity = 20


class Request:
    def __init__(self, info):
        self.info = self._split_info(info)
        self.from_ = self.info[4]
        self.to = self.info[6]
        self.amount = int(self.info[1])
        self.product = self.info[2]

    @staticmethod
    def _split_info(info):
        return info.split(" ")

    def __repr__(self):
        return f"Доставить {self.amount} {self.product} из {self.from_} в {self.to}"


def main():
    while True:
        user_input = input("Введите запрос")
        # user_input = "Доставить 3 печеньки из склад в магазин"
        request = Request(user_input)
        if user_input == "stop":
            break

        to = request.to
        from_ = request.from_

        if request.from_ == request.to:
            print("Пункты назначения должны быть разными")
            continue
        request.to, request.from_ = determine_places(request)

        if valid_quantity(request):
            print(f"Нужное количество есть в {from_}" + items_delivered(request, from_, to))
            print(display_contents(request.from_, from_))
            print(display_contents(request.to, to))
            continue
        else:
            print(error_inputs(request, to, from_))
            continue


def valid_quantity(request):
    # проверка на правильное количество товара
    if request.product not in request.from_.items:
        return False
    if request.from_.items[request.product] <= request.amount:
        return False
    if request.to.get_free_space <= request.amount:
        return False
    if request.to == shop and request.to.get_unique_items_count == 5 and request.product not in request.to.items:
        return False
    return True


def error_inputs(request, to, from_):
    # сообщения об ошибках
    if request.product not in request.from_.items:
        return f"Нет товара {request.product}"
    elif request.from_.items[request.product] <= request.amount:
        return f"Не хватает товара в {from_}, попробуйте заказать меньше"
    elif request.to.get_free_space <= request.amount:
        return f"Недостаточно места в {to}"
    elif request.to == shop and request.to.get_unique_items_count == 5 and request.product not in request.to.items:
        return f"Магазин переполнен"


def display_contents(place, name):
    # отображение содержания магазина и склада
    contents = []
    for item, value in place.items.items():
        contents.append(f"{value} {item}")
    return f"в {name} хранится:\n" + "\n".join(contents)


def items_delivered(request, from_, to):
    # логика перемещения товаров
    request.from_.remove(request.product, request.amount)
    request.to.add(request.product, request.amount)
    return f"\nКурьер забрал {request.amount} {request.product} из {from_}\n" \
           f"Курьер везет {request.amount} {request.product} из {from_} в {to}\n" \
           f"Курьер доставил {request.amount} {request.product} в {to}\n"


def determine_places(request):
    # переопределение названий в запросе на объекты
    if request.from_ == "склад":
        request.from_ = store
        request.to = shop
    elif request.from_ == "магазин":
        request.from_ = shop
        request.to = store
    return request.to, request.from_


if __name__ == "__main__":
    store = Store()
    shop = Shop()
    store.items = {"сок": 10,
                   "кофе": 10,
                   "молоко": 10,
                   "печеньки": 10}
    main()
