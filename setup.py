import itertools
import copy
import random

class Building:
    def __init__(self, name: str, floors:int):
        self.name = name
        self.floors = floors
        self.people = []
        self.grid_distance = 2.5
        for _ in range(self.floors):
            self.people.append([])

    def __str__(self):
        return self.name

    def get_floor(self, floor_num):
        return self.people[floor_num - 1]
        

    def check_floor_sick(self, floor_num: int):
        floor = self.get_floor(floor_num)
        for person in floor:
            if person.sick:
                return True
        return False

    def get_grid_distance(self, person1, person2):
        position1 = person1.position
        position2 = person2.position
        floor_difference = abs(position1[0] - position2[0])
        x_difference = abs(position1[1] - position2[1])
        y_difference = abs(position1[2] - position2[2])
        difference = (floor_difference, x_difference, y_difference)
        return difference

    def find_sick_people(self, floor_num: int):
        sick_people = []
        floor = self.get_floor(floor_num)
        for person in floor:
            if person.sick:
                sick_people.append(person)
        return sick_people

    def add_person(self, person):
        floor_num = person.position[0]
        floor = self.get_floor(floor_num)
        floor.append(person)
        person.building = self

    def remove_person(self, person):
        floor_num = person.position[0] 
        floor = self.get_floor(floor_num)
        floor.remove(person)
        person.building = None

    # writing this function so that we can get everyone from
    # that is next to a certain person
    def get_people_next_to(self, person):
        people_next_to = []
        floor_index = person.position[0] - 1
        person_floor = copy.copy(self.people[floor_index])

        try:
            person_floor.remove(person)
        except ValueError:
            raise ValueError("Person not in {}".format(person))
        

        person_x = person.position[1]
        person_y = person.position[2]
        x_range = range(person_x - 2, person_x + 3)
        y_range = range(person_y - 2, person_y + 3)
        for p in person_floor:
            current_x = p.position[1]
            current_y = p.position[2]
            if current_x in x_range and current_y in y_range:
                people_next_to.append(p)
        return people_next_to

    # this method simulates the spread itself not the movement of people
    def spread(self, floor_num: int):
        # if the spread score is above or equal 25 then they are sick and then enter the asymptomatic stage
        sick_people = self.find_sick_people(floor_num)
        new_sick_people = []

        sick_scores = {}

        for person in sick_people:
            spread_score = 5 if not person.mask else 3
            possible_spread = self.get_people_next_to(person)
            # assigning the sick scores for people
            for possible_person in possible_spread:
                distance_between = self.get_grid_distance(possible_person, person)
                distance_x = distance_between[1]
                distance_y = distance_between[2]
                spread_score += 5 if not possible_person.mask else 2
                spread_score += possible_person.vulnerable * 1.9
                spread_score += 3.8 - distance_x
                spread_score += 3.8 - distance_y
                sick_scores[possible_person] = spread_score
            # checking if the person should get sick
            for person in sick_scores.keys():
                score = sick_scores[person]
                if score >= 40:
                    person.get_sick()
                    new_sick_people.append(person)
        return new_sick_people

    def day(self):
        # this is what happens in the day 
        for _ in range(1000):
            for floor_num, floor in enumerate(self.people, start=1):
                self.spread(floor_num)
                for person in floor: 
                    person.simulate_movement()
                    self.spread(floor_num)
    
    def days(self, num_of_days):
        # repeats day function for a certain number of days 
        for _ in range(num_of_days):
            self.day()
  
  
    def get_sick_people(self):
        sick_people = {}
        for floor_num in range(0, self.floors):
            sick_people[floor_num+1] = self.find_sick_people(floor_num)
        return sick_people


class Person:
    base_id = itertools.count()

    def __init__(self, name: str, floor: int, sick: bool, mask: bool,
                 vulnerable: int, x: int, y: int):
        self.id = next(Person.base_id)
        self.name = name
        self.sick = sick
        self.mask = mask
        self.asymptomatic = True
        self.vulnerable = vulnerable
        # the order is floor, x, y
        self.position = (floor, x, y)
        self.isolate = False
        self.days_sick = int(self.sick)
        self.building = None

    def get_sick(self):
        self.sick = True
        self.asymptomatic = True

    def go_home(self):
        if self.sick and not self.asymptomatic:
            self.isolate = True
        self.building.remove_person(self)

    def move_floor(self, up: bool):
        current_building = self.building
        self.building.remove_person(self)
        if up:
                new_floor = self.position[0] + 1 if self.position[0] < len(current_building.people) \
                            else self.position[0]
        else:
            if self.position[0] <= 1:
              new_floor = 1
            else:
              new_floor = self.position[0] - 1
        self.position = (new_floor, self.position[1], self.position[2])
        self.building = current_building
        self.building.add_person(self)

    def day_pass(self):
        if self.days_sick >= 14:
            self.asymptomatic = False
            self.go_home()
        else:
            self.days_sick += 1

    def simulate_movement(self):
        # this is the random number generator that determines wether they should go...
        # up or down a floor
        floor = random.randrange(1, 11)
        if floor in range(1, 7) and self.position[0] >= 1:
            self.move_floor(False)
        elif floor == 10 and self.position[0] <= len(self.building.people):
            self.move_floor(True)
        else:
            x_position = random.randint(0, 10)
            y_position = random.randint(0, 10)
            self.position = (self.position[0], x_position, y_position)

        return self.position

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

