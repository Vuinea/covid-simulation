from setup import Building, Person


giant = Building("Giant", 3)

person1 = Person("Jeff", floor=1, sick=False, mask=True, vulnerable=7, x=7, y=4)
person2 = Person("Tom", floor=1, sick=True, mask=True, vulnerable=5, x=5, y=2)
person3 = Person("Sarah", floor=1, sick=False, mask=True, vulnerable=10, x=9, y=6)
person4 = Person("Mike", floor=2, sick=True, mask=False, vulnerable=3, x=6, y=7)
person5 = Person("Bob", floor=2, sick=False, mask=True, vulnerable=8, x=7, y=5)
person6 = Person("Nate", floor=1, sick=False, mask=True, vulnerable=8, x=7, y=4)
person7 = Person("Lucy", floor=2, sick=False, mask=True, vulnerable=4, x=3, y=7)

giant.add_person(person1)
giant.add_person(person2)
giant.add_person(person3)
giant.add_person(person4)
giant.add_person(person5)
giant.add_person(person6)
giant.add_person(person7)

print(f"Original Sick People: {giant.get_sick_people()}")
giant.days(3)
print(f"New Sick People: {giant.get_sick_people()}")


