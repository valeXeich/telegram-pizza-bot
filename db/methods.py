import os

from .db import Pizza, Ingredient, s

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

async def add_to_base(state):
    async with state.proxy() as data:
        pizza = Pizza(name=data['name'], price=data['price'], photo=data['photo'])
        for ingredient in data['ingredients']:
            ingredient_ = get_or_create(s, Ingredient, name=ingredient)
            pizza.ingredients.append(ingredient_)
            s.add(pizza)
            s.commit()

async def delete_pizza(state):
    async with state.proxy() as data:
        pizza = s.query(Pizza).filter(Pizza.name == data['name']).first()
        if pizza is None:
            return False
        else:
            os.remove(pizza.photo)
            s.delete(pizza)
            s.commit()
            return True

async def update_pizza(state):
    async with state.proxy() as data:
        pizza = s.query(Pizza).filter(Pizza.name == data['old_name']).first()
        data['old_ingredients'] = [old_ingredient for old_ingredient in pizza.ingredients]
        os.remove(pizza.photo)
        pizza.name = data['new_name']
        pizza.photo = data['new_photo']
        pizza.price = data['new_price']
        for ingredient in data['old_ingredients']:
            pizza.ingredients.remove(ingredient)
            s.commit()
        for ingredient in data['new_ingredients']:
            ingredient_ = get_or_create(s, Ingredient, name=ingredient)
            pizza.ingredients.append(ingredient_)
            s.commit()

def get_pizza_list():
    pizza_list = []
    pizza = s.query(Pizza).all()
    for pizza_ in pizza:
        pizza_list.append(pizza_.name)
    return pizza_list

