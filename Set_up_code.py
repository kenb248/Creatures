import random
direction = ["North", "East", "South", "West"]
creatures = ["Anticluster", "Flytrap","Parry","Twister","Crawler","Advrook","Sentry","Nest"]
number_of_creatures = 80 #Number of creatures to spawn
grid_size = 40 #Size of Grid
length = 50 #Length of simulation
to_append = [str(grid_size), str(length)] #Grid size, length of simulation


for i in range(number_of_creatures):
    creature = creatures[(random.randint(0,7))]
    start_dir = str(direction[(random.randint(0,3))])
    start_x = str(random.randint(1, grid_size)) 
    start_y = str(random.randint(1, grid_size))
    string = creature + " " + start_x + " " + start_y + " " + start_dir
    to_append.append(string)


open("world_input.txt", "w").close()

with open("world_input.txt", "a") as f:
    for i in to_append:
        f.write(i + '\n')




