### COMPSCI 130, Summer School 2019
### Project Two - Creatures
### Read readme file before executing program
import turtle
import hashlib
import random #used for explode intstruction

"""This class represents a Creature and contains all the information specific to the creature and handles things such as
     - Draws Creature
     - Handles Creatures next turn """

class Creature:
    def __init__(self, row, col, dna, direction):
        """All variables declared here relate to the set up of the creature ie starting location and direction"""
        self.convert_to_bearing(direction) #sets bearing 
        self.row = row
        self.col = col
        self.dna = dna
        self.next_instruction = 1
        self.starting_location = (row, col)
        self.set_direction()
        self.been_left = False #Used for the Roomber creature

    ## A creature draws itself using the colour specified as part of its dna
    ## the size of the grid squares, and the position of the top-left pixel are provided as input.
    def draw(self, grid_size, top_left_x, top_left_y):
        ## Compute the position of the top left hand corner of the cell this creature is in
        x = top_left_x + (self.col-1)*grid_size
        y = top_left_y - (self.row-1)*grid_size
        turtle.color(self.dna[0].split(":")[1])

        ## Depending on the direction of the Creature tip of triangle will be in a different part of the square
        if self.direction == 'North':
            turtle.goto(x, y - grid_size)
            turtle.pendown()
            turtle.begin_fill()
            turtle.goto(x + grid_size, y - grid_size)
            turtle.goto(x + (0.5 * grid_size), y)
            turtle.goto(x, y - grid_size)
        elif self.direction == 'East':
            turtle.goto(x,y)
            turtle.pendown()
            turtle.begin_fill()
            turtle.goto(x + grid_size, y - (0.5 * grid_size))
            turtle.goto(x, y - grid_size)
            turtle.goto(x,y)
        elif self.direction == 'South':
            turtle.goto(x,y)
            turtle.pendown()
            turtle.begin_fill()
            turtle.goto(x + (0.5 * grid_size), y - grid_size)
            turtle.goto(x + grid_size, y)
            turtle.goto(x,y)
        elif self.direction == 'West':
            turtle.goto(x + grid_size, y - grid_size)
            turtle.pendown()
            turtle.begin_fill()
            turtle.goto(x, y - (0.5 * grid_size))
            turtle.goto(x + grid_size, y)
            
        turtle.end_fill()
        turtle.penup()
        turtle.color("black")

    ## Returns the name of the species for this creature
    def get_species(self):
        return self.dna[0].split(":")[0]

    ## Gets the current position of the creature
    def get_position(self):
        return (self.row, self.col)

    ## Returns a string representation of the creature
    def __str__(self):
        return str(self.get_species() + ' ' + str(self.row) + ' ' + str(self.col) + ' ' + str(self.direction))

    ## Converts input directions to bearings
    def convert_to_bearing(self, direction):
        if direction == "North":
            self.bearing = 90
        elif direction == "East":
            self.bearing = 180
        elif direction == "South":
            self.bearing = 270
        else:
            self.bearing = 360
        
    ## This function sets the creatures direction based on their bearing. Using a bearing system makes
    ## it easier to implement intructions such as reverse and twist.
    def set_direction(self):
        if self.bearing > 360:
            self.bearing -=360
        elif self.bearing <= 0:
            self.bearing += 360
        if self.bearing == 90:
            self.direction = 'North'
        elif self.bearing == 180:
            self.direction = 'East'
        elif self.bearing == 270:
            self.direction = 'South'
        elif self.bearing == 360:
            self.direction = 'West'
    ### Used by the Roomber to make sure the Creature has been to the top left
    def been_top_left(self, position): 
        if position == (1,1):
            self.been_left = True
        return self.been_left

    def record_location(self):
        return (self.row, self.col)
    
    ## Execute a single move for this creature by following the instructions in its dna
    def make_move(self, world):
        """The first part of this function determines the location of the square in front of the creature"""
        finished = False
        does_have_2 = False 
        ahead_row = self.row
        ahead_col = self.col
        ahead_row2 = self.row #this variable only used by creatures with ifenemy2 in there DNA
        ahead_col2 = self.col #this variable only used by creatures with ifenemy2 in there DNA
        if self.direction == 'North':
            ahead_row = ahead_row - 1
            ahead_row2 = ahead_row - 1 
        elif self.direction == 'South':
            ahead_row = ahead_row + 1
            ahead_row2 = ahead_row + 1 
        elif self.direction == 'East':
            ahead_col = ahead_col + 1
            ahead_col2 = ahead_col + 1 
        elif self.direction == 'West':
            ahead_col = ahead_col - 1
            ahead_col2 = ahead_col - 1 
        ahead_value = world.get_cell(ahead_row, ahead_col)
        ahead_location = (ahead_row, ahead_col)
        ahead_location2 = (ahead_row2, ahead_col2) #only used if creature executes ifenemy2 instruction
        
        """The last part of the function executes the instructions based on the Creatures DNA"""
        while not finished:
            next_op = self.dna[self.next_instruction]
            op = next_op.split()
            ################## GO #########################2
            if op[0] == 'go':
                self.next_instruction = int(op[1])
            ################## HOP #########################3
            if op[0] == 'hop':
                if ahead_value == 'EMPTY':
                    self.row = ahead_row
                    self.col = ahead_col
                self.next_instruction = self.next_instruction + 1
                finished = True
            ################# Reverse ######################
            if op[0] == 'reverse':
                self.bearing += 180
                self.set_direction()
                self.next_instruction = self.next_instruction + 1
                finished = True
            ################ If Not Wall ####################
            if op[0] == 'ifnotwall':
                if world.get_cell(ahead_row, ahead_col) == 'EMPTY':
                    self.next_instruction = int(op[1])
                else:
                    self.next_instruction += 1
            ################### Twist ########################
            if op[0] == 'twist':
                self.bearing += 90
                self.set_direction()
                self.next_instruction += 1
                finished = True
            ################### Reverse Twist ################ Custom Instruction
            if op[0] == 'reversetwist':
                self.bearing -= 90
                self.set_direction()
                self.next_instruction += 1
                finished = True
            ###################    Topleft  ################### Custom Instruction for Roomber
            if op[0] == 'topleft':
                if self.been_top_left((self.row,self.col)) == False:
                    if self.bearing != 360:
                        self.next_instruction = int(op[1]) #Sets Creatures direction to North
                    else:
                        self.next_instruction = 23 #Makes the Creature hop forward until it hits the first column
                else:
                    if self.bearing != 90:
                        self.next_instruction = int(op[1]) #Sets Creatures direction to North
                    else:
                        self.next_instruction += 1 #Makes creature hop until in first row which at (1,1) ie top left
          ##################### ifsame #######################
            if op[0] == 'ifsame':
                if ahead_location in world.all_starting_locations:
                    creature_index = world.all_starting_locations.index(ahead_location)
                    species = world.all_creatures[creature_index]
                    species = species.get_species()
                    if species != self.get_species():
                        self.next_instruction += 1 #creature is an enemy move to next instruction
                    elif species == self.get_species():
                        self.next_instruction = int(op[1]) #Creature is the same species jump to some instruction
                else:
                    self.next_instruction += 1
            ##################### ifenemy #####################
            if op[0] == 'ifenemy':
                if ahead_location in world.all_starting_locations:
                    creature_index = world.all_starting_locations.index(ahead_location)
                    species = world.all_creatures[creature_index]
                    species = species.get_species()
                    if species != self.get_species():
                        self.next_instruction = int(op[1]) #creature is an enemy jump to some instruction
                    else:
                        self.next_instruction += 1 #creature is same species
                else:
                    self.next_instruction += 1 #ahead cell has no creatures move to next instruction
            #################### ifrandom #######################
            if op[0] == 'ifrandom':
                if world.pseudo_random() == 1:
                    self.next_instruction = int(op[1])
                else:
                    self.next_instruction += 1
            ##################### infect ##########################
            if op[0] == 'infect':
                if ahead_location in world.all_starting_locations:
                    creature_index = world.all_starting_locations.index(ahead_location)
                    species = world.all_creatures[creature_index]
                    species = species.get_species()
                    if species != self.get_species():
                        other_creature = world.all_creatures[creature_index]
                        other_creature.dna = self.dna
                        other_creature.next_instruction = 1 #Because if instructions aren't reset could be out of range of new dna instructions
                        self.next_instruction += 1
                        finished = True
                        
                #Below code used for custom creatures only gives ability to infect creatures two squares in front
                elif ahead_location2 in world.all_starting_locations and does_have_2 == True: #Only executes if does_have_2 is true
                    creature_index = world.all_starting_locations.index(ahead_location2)
                    species = world.all_creatures[creature_index]
                    species = species.get_species()
                    if species != self.get_species():
                        other_creature = world.all_creatures[creature_index]
                        other_creature.dna = self.dna
                        other_creature.next_instruction = 1
                        self.next_instruction += 1
                        finished = True
                finsished = True
            """Note that instructions beyond this line are used for custom creatures and aren't part of the required instructions"""
            """------------------------------------------------------------------------------------------------------------------"""
            ######################## ifenemy2 ##################################
            if op[0] == 'ifenemy2':
                does_have_2 = True #Used so that in the infect function only uses 2 locations if there is 2 locations
                if ahead_location in world.all_starting_locations:
                    creature_index = world.all_starting_locations.index(ahead_location)
                    species = world.all_creatures[creature_index]
                    species = species.get_species()
                    if species != self.get_species():
                        self.next_instruction = int(op[1])
                    else:
                        self.next_instruction += 1
                elif ahead_location2 in world.all_starting_locations:
                    creature_index = world.all_starting_locations.index(ahead_location2)
                    species = world.all_creatures[creature_index]
                    species = species.get_species()
                    if species != self.get_species():
                        self.next_instruction = int(op[1])
                    else:
                        self.next_instruction += 1
                else:
                    self.next_instruction += 1
            ########################## Wait #####################################
            if op[0] == 'wait': #purpose of this if for when the square in front is filled with a Creature of same species
                self.next_instruction += 1
                finished = True 
            ############################# Spawn ###################################
            ## Used to spawn a new creature used by Nest creature
            if op[0] == 'spawn':
                if ahead_value == "EMPTY" and ahead_value not in world.all_starting_locations:
                        possible_spawns = ["Anticluster", "Crawler", "Advrook", "Twister", "Advrandy"]
                        new_dna = possible_spawns[(random.randint(0, 4))]
                        new_dna = world.dna_dict[new_dna]
                        spawned_creature = Creature(ahead_row, ahead_col, new_dna, self.bearing)
                        world.add_creature(spawned_creature)
                self.next_instruction += 1
                finished = True
            ############################# Explode #################################
            if op[0] == 'explode':
                ### Area_to_explode will contain a range of locations which are in the infection
                area_to_explode = []
                
                area_to_explode.append((self.row-1, self.col-1))
                area_to_explode.append((self.row-1, self.col))
                area_to_explode.append((self.row-1, self.col+1))
                area_to_explode.append((self.row, self.col-1))
                area_to_explode.append(ahead_location2)
                area_to_explode.append((self.row, self.col+1))
                area_to_explode.append((self.row+1, self.col-1))
                area_to_explode.append((self.row+1, self.col))
                area_to_explode.append((self.row+1, self.col+1))
                
                ## If there is a creature in a square in the radius given some random DNA
                for i in area_to_explode:
                    if i in world.all_starting_locations:
                        new_dna = random.randint(5,(len(world.types_of_creatures)-1)) #this is reason for importing random
                        new_dna = world.types_of_creatures[new_dna]
                        new_dna = world.dna_dict[new_dna]
                        creature_index = world.all_starting_locations.index(i)
                        other_creature = world.all_creatures[creature_index]
                        other_creature.dna = new_dna
                        other_creature.next_instruction = 1
                self.next_instruction = 1
                finished = True
                        
        self.string = str(self.get_species() + ' ' + str(self.row) + ' ' + str(self.col) + ' ' + str(self.direction)) #Gives an up to data location of creature used in world __str__ method
                

"""This calss contains all information and instructions relating to the world the Creatures are in"""
class World:
    ## The world stores its grid-size, and the number of generations to be executed.
    def __init__(self, size, max_generations, types_creatures, world_data, all_dna):
        self.size = size
        self.generation = 0
        self.max_generations = max_generations
        self.creature = None  #5
        self.all_creatures = [] #Will contain all the creatures in the world
        self.all_starting_locations = [] # used to hold all postitions of creatures
        self.number_of_creatures = [] #used in __str__
        self.types_of_creatures = types_creatures 
        self.world_data = world_data 
        self.dna_dict = all_dna #used in spawn instruction in creatures class
        
    ## Adds a creature to the world
    def add_creature(self, c):
        self.creature = c
        if self.creature.starting_location not in self.all_starting_locations: #Checks square doesn't already contain a creature
            self.all_creatures.append(self.creature)
            self.all_starting_locations.append(self.creature.starting_location)


    ## Gets the contents of the specified cell.  This could be 'WALL' if the cell is off the grid
    ## or 'EMPTY' if the cell is unoccupied
    def get_cell(self, row, col):
        if row <= 0 or col <= 0 or row >= self.size + 1 or col >= self.size + 1:
            return 'WALL'            
        return 'EMPTY'

    ## Used to generate a semi random number
    def pseudo_random(self):
        total = 0
        for i in self.all_starting_locations:
            total += i[0]
            total += i[1]
        total = total * self.generation
        string_total = str(total)
        return int(hashlib.sha256(string_total.encode()).hexdigest(), 16) % 2
           


    ## Executes one generation for the world - the creature moves once.  If there are no more
    ## generations to simulate, the world is printed
    def simulate(self):
        self.count = 0
        if self.generation < self.max_generations:
            for i in self.all_creatures:
                i.make_move(self)
                location = i.record_location()
                self.all_starting_locations[self.count] = location
                self.count += 1
            self.generation += 1
            return False
        else:
            print(self)
            return True

    ## Returns a string representation of the world
    def __str__(self):
        summary = []
        string = str(self.size)
        for creatures in self.types_of_creatures:
            count = 0
            for i in self.all_creatures:
                if creatures in i.dna[0]:
                    count+= 1
            if count > 0:
                summary.append((creatures, count))
        summary = sorted(summary, key = lambda x: (1/x[1], x[0]))
        string = string + "\n" + str(summary) + "\n"
        for i in self.all_creatures:
            string = string + i.string + "\n"
        return string

    ## Display the world by drawing the creature, and placing a grid around it
    def draw(self):

        # Basic coordinates of grid within 800x800 window - total width and position of top left corner
        grid_width = 700
        self.top_left_x = -350
        self.top_left_y = 350
        self.grid_size = grid_width / self.size

        # Draw the creature
        for i in self.all_creatures:
            i.draw(self.grid_size, self.top_left_x, self.top_left_y)

        # Draw the bounding box
        turtle.goto(self.top_left_x, self.top_left_y)
        turtle.setheading(0)
        turtle.pendown()
        for i in range(0, 4):
            turtle.rt(90)
            turtle.forward(grid_width)
        turtle.penup()

        # Draw rows
        for i in range(self.size):
            turtle.setheading(90)
            turtle.goto(self.top_left_x, self.top_left_y - self.grid_size*i)
            turtle.pendown()
            turtle.forward(grid_width)
            turtle.penup()

        # Draw columns
        for i in range(self.size):
            turtle.setheading(180)
            turtle.goto(self.top_left_x + self.grid_size*i, self.top_left_y)
            turtle.pendown()
            turtle.forward(grid_width)
            turtle.penup()

"""This Class is responsible for taking all input data and setting up the simulation"""
class CreatureWorld:

    ## Initialises the window, and registers the begin_simulation function to be called when the space-bar is pressed
    def __init__(self):
        self.framework = SimulationFramework(800, 800, 'COMPSCI 130 Project Two')
        self.framework.add_key_action(self.begin_simulation, ' ')
        self.framework.add_tick_action(self.next_turn, 100) # Delay between animation "ticks" - smaller is faster.

    ## Starts the animation
    def begin_simulation(self):
        self.framework.start_simulation()

    ## Ends the animation
    def end_simulation(self):
        self.framework.stop_simulation()

    ## Reads the data files from disk
    def setup_simulation(self):
        
        ## If new creatures are defined, they should be added to this list: #6
        all_creatures = ['Hopper', 'Parry', 'Rook', 'Roomber', 'Randy', 'Flytrap', 'Advrook', 'Sentry',
                         'Advrandy', 'Crawler', 'Twister', 'Nest', 'Anticluster']        

        # Read the creature location data
        with open('world_input.txt') as f:
            world_data = f.read().splitlines()
        # Read the dna data for each creature type
        dna_dict = {}
        for creature in all_creatures:
            with open('Creatures//' + creature + '.txt') as f:
                dna_dict[creature] = f.read().splitlines()

        # Create a world of the specified size, and set the number of generations to be performed when the simulation runs
        world_size = world_data[0]
        world_generations = world_data[1]
        self.world = World(int(world_size), int(world_generations), all_creatures, world_data, dna_dict)

        # Adds all Creatures from input into World
        for i in range(2, len(world_data)):
            creature = world_data[i]
            data = creature.split()
            self.world.add_creature(Creature(int(data[1]), int(data[2]), dna_dict[data[0]], data[3]))
        
            
        # Draw the initial layout of the world
        self.world.draw()

    ## This function is called each time the animation loop "ticks".  The screen should be redrawn each time.         
    def next_turn(self):
        turtle.clear()
        self.world.draw() 
        if self.world.simulate():
            self.end_simulation()

    ## This function sets up the simulation and starts the animation loop
    def start(self):
        self.setup_simulation() 
        turtle.mainloop() # Must appear last.


## This is the simulation framework - it does not need to be edited
class SimulationFramework:

    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.simulation_running = False
        self.tick = None #function to call for each animation cycle
        self.delay = 100 #default is .1 second.       
        turtle.title(title) #title for the window
        turtle.setup(width, height) #set window display
        turtle.hideturtle() #prevent turtle appearance
        turtle.tracer(False) #prevent turtle animation
        turtle.listen() #set window focus to the turtle window
        turtle.mode('logo') #set 0 direction as straight up
        turtle.penup() #don't draw anything
        self.__animation_loop()
        
    def start_simulation(self):
        self.simulation_running = True
        
    def stop_simulation(self):
        self.simulation_running = False

    def add_key_action(self, func, key):
        turtle.onkeypress(func, key)

    def add_tick_action(self, func, delay):
        self.tick = func
        self.delay = delay

    def __animation_loop(self):
        if self.simulation_running:
            self.tick()
        turtle.ontimer(self.__animation_loop, self.delay)
   
cw = CreatureWorld()
cw.start()
