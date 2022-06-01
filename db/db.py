from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


engine = create_engine('postgresql+psycopg2://admin:admin@localhost/telegram_bot')
Base = declarative_base()

pizza_ingredient = Table(
    "pizza_ingredient",
    Base.metadata,
    Column("ingredients_id", ForeignKey("Ingredients.id_ingredient"), primary_key=True),
    Column("pizza_id", ForeignKey("Pizza.id_pizza"), primary_key=True),
)


class Ingredient(Base):
    __tablename__ = 'Ingredients'

    id_ingredient = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    pizza = relationship(
        'Pizza', secondary=pizza_ingredient, back_populates="ingredients"
    )

    def __repr__(self):
        return f'{self.name}'


class Pizza(Base):
    __tablename__ = 'Pizza'

    id_pizza = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    photo = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    ingredients = relationship(
        'Ingredient', secondary=pizza_ingredient, back_populates="pizza"
    )


Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)
s = session()






