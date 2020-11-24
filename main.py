import random
import draw
import time
import graphs
import csv
"""
PEP8:

module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_CONSTANT_NAME,
global_var_name, instance_var_name, function_parameter_name, local_var_name

"""


class Apple:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


ANIMAL_POPULATION = 30
APPLE_POPULATION = 30

animals = []
apples = []

round_number = 0
ROUND_LENGTH = 30  # Seconds

time_pen = draw.turtle.Turtle()
time_pen.speed(0)
time_pen.shape('square')
time_pen.penup()
time_pen.hideturtle()
time_pen.goto(25, 6)
time_pen.write("")

round_counter_pen = draw.turtle.Turtle()
round_counter_pen.speed(0)
round_counter_pen.shape('square')
round_counter_pen.penup()
round_counter_pen.hideturtle()
round_counter_pen.goto(25, 3)
round_counter_pen.clear()
round_counter_pen.write(f"Round: {round_number}", move=False, font=("Roboto Bold", 24, "normal"))

csv_file = open('animal_speeds_data.csv', 'r')
data_reader = csv.reader(csv_file)
csv_speeds = []

if len(csv_file.readline()) > 0:
    print(csv_file.readline())
    user_sees_graph = input("Would you like to see a graph? Y or N\n")
    if user_sees_graph.casefold() == 'y':
        print(data_reader)
        for line in data_reader:
            print(line)
            if line != ["Round", "Speed"] and line != []:
                csv_round_number = line[0]
                csv_speeds.append(line[1])
        graphs.speed_graph(round_number=int(csv_round_number), animal_speeds=csv_speeds)
else:
    print("length is 0")

csv_file.close()


def mutate(**kwargs):

    value = kwargs["value"]
    chances = kwargs["chances"]
    starting_range = kwargs["starting_range"]
    ending_range = kwargs["ending_range"]
    chance_of_increase = kwargs["chance_of_increase"]
    is_float = kwargs["is_float"]

    mutation_decider = random.randint(0, 100)
    increase_range = range(0, chance_of_increase)
    change_direction_decider = random.randint(0, 100)
    original_value = value

    if mutation_decider <= chances:
        # Mutation occurs
        if is_float:
            change_value = random.uniform(starting_range, ending_range)
        else:
            change_value = random.randint(starting_range, ending_range)

        if change_direction_decider in increase_range:
            value += change_value
        else:
            value -= change_value

        print(f"MUTATION: {original_value} to {value}")
    else:
        print("No mutation :(")

    return value


def reproduce(**kwargs):
    born_animal_x = draw.ENDING_X / 2
    born_animal_y = born_animal_x

    born_vision_distance = kwargs["vision_distance"]
    born_speed = kwargs["speed"]

    born_animal = draw.Animal(born_animal_x, born_animal_y, born_vision_distance, born_speed)
    draw.animals.append(born_animal)


def initialize_animals():
    global animals
    if round_number == 1:
        for animal_index in range(ANIMAL_POPULATION):
            animal_x = draw.ENDING_X / 2
            animal_y = animal_x
            vision_distance = draw.STARTING_VISION_DISTANCE
            speed = 1

            current_animal = draw.Animal(animal_y, animal_y, vision_distance, speed)
            draw.animals.append(current_animal)
    else:
        for _ in animals:
            animal_x = draw.ENDING_X / 2
            animal_y = animal_x
            vision_distance = draw.STARTING_VISION_DISTANCE
            speed = 1

            current_animal = draw.Animal(animal_y, animal_y, vision_distance, speed)
            draw.animals.append(current_animal)

            # Call reproduction function


def initialize_food():
    for foodIndex in range(APPLE_POPULATION):
        apple_x = random.randint(draw.STARTING_X+5, draw.ENDING_X-5)
        apple_y = random.randint(draw.STARTING_Y+5, draw.ENDING_Y-5)

        current_apple = Apple(apple_x, apple_y, "red")

        apples.append(current_apple)
    draw.render_apples(apples)


def move_animals():
    start_time = round(time.time())

    while time.time() - start_time < ROUND_LENGTH:
        if (round(time.time()) - start_time) % 1 == 0:
            time_pen.clear()
            time_pen.write(f"{ROUND_LENGTH - (round(time.time()) - start_time)} S", move=False,
                           font=("Roboto Bold", 24, "normal"))
        draw.move_sprites()


def check_animal_states():
    for animal in draw.animals:
        if animal.state == "L":
            # Animal lives
            pass
        elif animal.state == "D":
            # Animal dies
            draw.animal_pen.clear()
            draw.animal_pen.hideturtle()
            draw.animals.remove(animal)
            del animal
        else:
            # Animal reproduces
            for i in range(animal.apples_eaten-2):
                print("New baby born")

                mutated_speed = mutate(value=animal.speed, chances=100,
                                       starting_range=1, ending_range=2,
                                       chance_of_increase=95, is_float=True)

                mutated_vision_distance = mutate(value=animal.vision_distance, chances=100,
                                                 starting_range=5, ending_range=10,
                                                 chance_of_increase=95, is_float=False)

                reproduce(vision_distance=mutated_vision_distance, speed=mutated_speed)


def new_round():
    global round_number, apples

    if round_number > 0:
        # Call the animal_lives function
        check_animal_states()

    round_number += 1
    round_counter_pen.clear()
    round_counter_pen.write(f"ROUND {round_number}", move=False, font=("Roboto Bold", 24, "normal"))

    if round_number > 1:
        draw.clear_objects()

    apples.clear()
    draw.apple_sprites.clear()
    draw.apple_positions.clear()

    initialize_animals()
    initialize_food()
    time_pen.clear()
    move_animals()


while True:
    new_round()

# draw.finish()

