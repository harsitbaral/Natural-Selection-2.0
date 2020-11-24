import turtle
import random
import time
import graphs

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

# Screen Setup
wn = turtle.Screen()
wn.tracer(0)
wn.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
wn.bgcolor("white")
wn.title('Natural Selection Simulator')

canvas = wn.getcanvas()
root = canvas.winfo_toplevel()

STARTING_X = 0
ENDING_X = 100
STARTING_Y = 0
ENDING_Y = 100

# Turtle allows us to set our own coordinates for the world
# LOWER LEFT X, LOWER LEFT Y, UPPER RIGHT X, UPPER RIGHT Y
# 0, 100, 100, 0

wn.setworldcoordinates(STARTING_X, ENDING_Y, ENDING_X, STARTING_Y)

# A legend to help understand what each colour of the turtles means


def start_legend():
    legend = turtle.Turtle()
    legend.speed(0)
    legend.shape('square')
    legend.color('black')
    legend.penup()
    legend.hideturtle()
    legend.goto(0, 8.5)
    legend.write("Legend:\nBlue = Reproduces\nBlack = Dies\nGreen = Lives", move=False, align="left",
                 font=("Roboto Bold", 14, "bold"))


start_legend()

# Animal pen, which will be used when creating all instances of animals

animal_pen = turtle.Turtle()
animal_pen.shape("turtle")
animal_pen.color("green")
animal_pen.penup()

action_text = turtle.Turtle()
action_text.speed(0)
action_text.shape('square')
action_text.penup()
action_text.hideturtle()
action_text.goto(62, 3)
action_text.write("No turtles have eaten apples", move=False, font=("Roboto Bold", 18, "bold"))

total_apples_eaten = 0

total_apples_text = turtle.Turtle()
total_apples_text.speed(0)
total_apples_text.shape('square')
total_apples_text.penup()
total_apples_text.hideturtle()
total_apples_text.goto(62, 6)
total_apples_text.write(f"({total_apples_eaten} eaten by all)", move=False, font=("Roboto Bold", 18, "normal"))

animal_population = 30

animal_population_text = turtle.Turtle()
animal_population_text.speed(0)
animal_population_text.shape('square')
animal_population_text.penup()
animal_population_text.hideturtle()
animal_population_text.goto(25, 9)
animal_population_text.write(f"Animal Population: {animal_population}", move=False, font=("Roboto Bold", 24, "normal"))

round_number = 1

apple_positions = []
apple_sprites = []

STARTING_ENERGY = 0
STARTING_SPEED = 0
STARTING_VISION_DISTANCE = 20
AGE_OF_DEATH = 10  # How many rounds the animal can live before dying
MOVEMENT_REQUIREMENT = 10  # How many times the animal has to move in a certain direction


class Animal:
    def __init__(self, x, y, vision_distance, speed):
        self.x_size = 0.75
        self.y_size = self.x_size
        self.x = x
        self.y = y
        self.selected_movement = ""
        self.sees_food = False
        self.movement_counter = 0
        self.MOVEMENT_REQUIREMENT = 10
        self.current_direction = ""
        self.vision_distance = vision_distance
        self.speed = speed
        self.apples_eaten = 0
        self.movement_energy_consumption = 0.25
        self.state = "L"
        self.color = "green"
        self.energy = STARTING_ENERGY
        self.age = 0
        self.moves_without_apples = 0

    # Check for state
    def check_state(self):
        if self.apples_eaten >= 2 and self.age < AGE_OF_DEATH:
            # Reproduces
            self.state = "R"
            self.color = "blue"
        elif self.apples_eaten == 1 or self.energy > 0 and self.age < AGE_OF_DEATH:
            # Lives
            self.state = "L"
            self.color = "green"
        elif self.energy <= 0 or self.age == AGE_OF_DEATH:
            # Dies
            self.state = "D"
            self.color = "black"
    # Movement

    def move(self):
        if self.selected_movement == "UP":
            if self.y - 1 >= 0:
                self.y -= 1
            else:
                self.selected_movement = random.choice(["DOWN", "LEFT", "RIGHT"])
        elif self.selected_movement == "DOWN":
            if self.y + 1 <= 100:
                self.y += 1
            else:
                self.selected_movement = random.choice(["UP", "LEFT", "RIGHT"])
        elif self.selected_movement == "LEFT":
            if self.x - 1 >= 0:
                self.x -= 1
            else:
                self.selected_movement = random.choice(["UP", "DOWN", "RIGHT"])
        else:
            if self.x + 1 <= 100:
                self.x += 1
            else:
                self.selected_movement = random.choice(["UP", "DOWN", "LEFT"])

        if self.speed > 0:
            self.movement_energy_consumption *= (self.speed * 2)
        self.energy -= self.movement_energy_consumption

    def update(self):
        self.check_for_food()  # Make sure that we don't see food

        if not self.sees_food:
            if self.movement_counter == self.MOVEMENT_REQUIREMENT or self.movement_counter == 0:
                # If the turtle has moved enough in one direction, proceed
                self.selected_movement = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
                self.current_direction = self.selected_movement

                if self.movement_counter == self.MOVEMENT_REQUIREMENT:
                    self.movement_counter = 0
                else:
                    self.movement_counter += 1
            else:
                self.movement_counter += 1
        self.check_state()

        if total_apples_eaten < 30:
            if self.moves_without_apples == 15 and self.state == "L":
                pass
            else:
                self.move()

    def render(self, pen):
        pen.color(self.color)
        pen.goto(self.x, self.y)
        pen.shapesize(self.x_size, self.y_size)
        if self.speed < 0:
            self.speed = 0
        elif self.speed > 10:
            self.speed = 10
        pen.speed(self.speed)
        pen.stamp()

    def check_for_food(self):
        """
        Check if the x is in animal_positions then inside that check if the food x is greater or lower
        than the animal x. If so, move right and if not, move left.

        Check if the y is in animal_positions then inside that check if the food y is greater or lower
        than the animal y. If so, move down and if not, move up.
        """
        for position in apple_positions:
            if position[0] == self.x:
                if position[1] in range(int(self.y-self.vision_distance), int(self.y+self.vision_distance)+1):
                    self.sees_food = True
                    if position[1] > self.y:
                        self.selected_movement = "DOWN"
                    else:
                        self.selected_movement = "UP"
            if position[1] == self.y:
                if position.index(self.y) == 1:
                    if position[0] in range(int(self.x-self.vision_distance), int(self.x+self.vision_distance)+1):
                        self.sees_food = True
                        if position[0] > self.x:
                            self.selected_movement = "RIGHT"
                        else:
                            self.selected_movement = "LEFT"
            if self.y not in position and self.x not in position:
                self.sees_food = False
            update_apples(self)


animals = []


def move_sprites():
    animal_pen.clear()
    time.sleep(0.1)
    # check_for_pause()
    for sprite in animals:
        sprite.render(animal_pen)
        update_apples(sprite)
        sprite.update()

    wn.update()


APPLE_POPULATION = 0


def render_apples(apples):
    global APPLE_POPULATION
    for apple in apples:
        apple_sprite = turtle.Turtle("circle")
        apple_sprite.shapesize(0.75, 0.75)
        apple_sprite.color(apple.color)
        apple_sprite.penup()
        apple_sprite.setpos(apple.x, apple.y)
        apple_positions.append([apple.x, apple.y])
        apple_sprites.append(apple_sprite)

        APPLE_POPULATION = len(apple_sprites)


def update_apples(animal):
    x = int(animal.x)
    y = int(animal.y)
    global total_apples_eaten, animal_population

    if [x, y] in apple_positions:
        animal.apples_eaten += 1
        total_apples_eaten += 1
        animal.moves_without_apples = 0
        animal.energy += 25

        apple_remaining_percent = round(((APPLE_POPULATION-total_apples_eaten)/APPLE_POPULATION)*100, 1)
        total_apples_text.clear()
        total_apples_text.write(f"({APPLE_POPULATION - total_apples_eaten}/{APPLE_POPULATION} = "
                                f"{apple_remaining_percent}% of apples remain)", move=False,
                                font=("Roboto Bold", 18, "bold"))
        action_text.clear()
        action_text.write(f"Turtle #{animals.index(animal) + 1} ate an apple ({animal.apples_eaten})", move=False,
                          font=("Roboto Bold", 18, "bold"))

        apple = apple_sprites[apple_positions.index([x, y])]
        apple.hideturtle()
        apple_position = apple_positions[apple_positions.index([x, y])]
        apple_positions.remove(apple_position)
        apple_sprites.remove(apple)
        del apple
    else:
        animal.moves_without_apples += 1


animal_ages = []
average_age = 0
animal_speeds = []
average_speed = 0

total_animal_speeds = []


def clear_objects():
    global total_apples_eaten, animal_population, average_speed, average_age, round_number

    round_number += 1
    action_text.clear()
    total_apples_eaten = 0
    total_apples_text.clear()
    action_text.write("No turtles have eaten apples", move=False, font=("Roboto Bold", 18, "bold"))

    animal_population_text.clear()
    if len(animals) > 0:
        animal_population = len(animals)
    animal_population_text.write(f"Animal Population: {animal_population}", move=False,
                                 font=("Roboto Bold", 24, "normal"))

    for animal in animals:
        animal_pen.clear()
        animal_pen.hideturtle()

        animal.x = ENDING_X / 2
        animal.y = animal.x
        animal.apples_eaten = 0
        animal.energy = STARTING_ENERGY
        animal.age += 1

        animal_ages.append(animal.age)
        animal_speeds.append(animal.speed)

    for apple_sprite in apple_sprites:
        apple_sprite.clear()
        apple_sprite.hideturtle()
        del apple_sprite

    try:
        average_age = sum(animal_ages) / len(animal_ages)
        average_speed = sum(animal_speeds) / len(animal_speeds)
        total_animal_speeds.append(average_speed)
        print(f"Average age: {average_age} rounds")
        print(f"Average speed: {average_speed}")
    except ZeroDivisionError:
        print("Average age: 1 round")
        print("Average speed: 0")


def create_speed_graph_button():
    speed_graph_button = turtle.Turtle()
    speed_graph_button.speed(0)
    speed_graph_button.hideturtle()
    speed_graph_button.penup()
    speed_graph_button.goto(0, 10)
    speed_graph_button.pendown()
    speed_graph_button.goto(5, 10)
    speed_graph_button.goto(5, 12.5)
    speed_graph_button.goto(0, 12.5)
    speed_graph_button.goto(0, 10)
    speed_graph_button.penup()
    speed_graph_button.goto(0.25, 12)
    speed_graph_button.write("Speed", move=False, font=("Roboto Bold", 12, "normal"))


create_speed_graph_button()

# root.protocol("WM_DELETE_WINDOW", csvfile.close())

# def show_speed_graph(x, y):
#     if 0 < x < 5 and 10 < y < 12.5:
#         print(round_number)
#         print(total_animal_speeds)
#
#         graphs.speed_graph(round_number=round_number, animal_speeds=total_animal_speeds)
#         graphs.plt.close()
#         print("closed")
#     else:
#         print(x, y)


# turtle.onscreenclick(show_speed_graph, 1)
# turtle.listen()
