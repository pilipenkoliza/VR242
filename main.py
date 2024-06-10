import json

import xml.etree.ElementTree as ET

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.class_name = 'item'
    
    def to_dict(self):
        return {'name': self.name, 'price': self.price}
    
    @staticmethod
    def from_dict(data):
        name = data['name']
        price = data['price']
        return Item(name, price)

class Dish(Item):
    def __init__(self, name, price, weight):
        super().__init__(name, price)
        self.weight = weight
        self.class_name = 'dish'
    
    def to_dict(self):
        data = super().to_dict()
        data['weight'] = self.weight
        return data
    
    @staticmethod
    def from_dict(data):
        name = data['name']
        price = data['price']
        weight = data['weight']
        return Dish(name, price, weight)

class Drink(Item):
    def __init__(self, name, price, volume):
        super().__init__(name, price)
        self.volume = volume
        self.class_name = 'drink'

    
    def to_dict(self):
        data = super().to_dict()
        data['volume'] = self.volume
        return data
    
    @staticmethod
    def from_dict(data):
        name = data['name']
        price = data['price']
        volume = data['volume']
        return Drink(name, price, volume)

# Сериализация в XML
def to_xml(items, filename):
    root = ET.Element('items')
    for item in items:
        item_element = ET.SubElement(root, item.class_name)
        for key, value in item.to_dict().items():
            sub_element = ET.SubElement(item_element, key)
            sub_element.text = str(value)
    
    tree = ET.ElementTree(root)
    tree.write(filename)

# Десериализация из XML
def from_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    
    items = []
    for item_element in root.findall('item'):
        item_dict = {}
        for sub_element in item_element:
            item_dict[sub_element.tag] = sub_element.text
        item_type = item_dict.get('type')
        if item_type == 'dish':
            item = Dish.from_dict(item_dict)
        elif item_type == 'drink':
            item = Drink.from_dict(item_dict)
        else:
            item = Item.from_dict(item_dict)
        items.append(item)
    
    return items


def JsonToArr(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as in_file:
            json_file = json.load(in_file)
            return json_file
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return False

def toDish(dict):
    return Dish(dict["name"], dict["price"], dict["weight"])

def toDrink(dict):
    return Drink(dict["name"], dict["price"], dict["volume"])

def toDishes(dish_arr):
    dishes = []
    for i in dish_arr:
        dishes.append(toDish(i))
    return dishes

def toDrinks(drink_arr):
    drinks = []
    for i in drink_arr:
        drinks.append(toDrink(i))
    return drinks

def jsonToDishes(filename):
    dish_arr = JsonToArr(filename)
    if not dish_arr:
        return False
    return toDishes(dish_arr)

        

def jsonToDrinks(filename):
    drink_arr = JsonToArr(filename)
    return toDrinks(drink_arr)

def arrToJson(arr, filename):
        arr_out = []
        for i in arr:
            arr_out.append(i.to_dict())
        js = json.dumps(arr_out, indent=4)
        try:
            file = open(filename, "w", encoding='utf-8')
            if file:
                file.write(js)
            else:
                print("read file error")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return False



dishes = jsonToDishes("dish.json")
if not dishes:
    print("Error")
drinks = jsonToDrinks("drink.json")
for i in dishes:
    print(i.name, i.price, i.weight)
print()
for i in drinks:
    print(i.name, i.price, i.volume)

dishes[0].name = 'fish'

arrToJson(dishes, "dishes_out.json")

items = [Dish('cack', 250, 300), Dish('pancack', 150, 400)]

to_xml(items, 'data.xml')

# Десериализация из XML
deserialized_items = from_xml('data.xml')
for item in deserialized_items:
    print(item.name, item.price)
    
