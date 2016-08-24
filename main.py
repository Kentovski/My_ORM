# /usr/bin/python3

#MELNIKOV ILYA


from My_ORM import *


class Person(AbstractModel):

    name = TextField(length=200)
    age = IntegerField()
    is_alive = BooleanField()
    float_parameter = FloatField()


if __name__ == "__main__":
    migrate(Person)

    Petya = Person(name='Petya', age=11, is_alive=True, float_parameter=12.5)
    Vasya = Person(name='Vasya', age=12, is_alive=True, float_parameter=56.5)
    Vova = Person(name='Vova', age=99, is_alive=False, float_parameter=14.2)

    Petya.save()
    Vasya.save()
    Vova.save()

    print(select(Person, age__gt=10))