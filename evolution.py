import random
from matplotlib import pyplot as plt 
import numpy 
blobs = []
oozes = []
plants = [] 
day_count = 0 
x_vals = [] 
blob_y_hp_start = [] 
blob_y_speed = [] 
blob_y_e_max = [] 
blob_y_lifespan = []
blob_y_sence = []
blob_y_efficiency = [] 
blob_offspring = [] 
ooze_y_hp_start = [] 
ooze_y_speed = [] 
ooze_y_e_max = [] 
ooze_y_lifespan = []
ooze_y_sence = []
ooze_y_efficiency = [] 
ooze_offspring = [] 
total_food = 50 
world_light = 10 
blob_population = []
ooze_population = [] 
blob_x = [] 
blob_y = [] 
ooze_x = [] 
ooze_y = [] 
fears_list = []
plant_offspring = [] 
class organism(object): 
    def __init__(self, hp_start, speed, e_max, lifespan, sence, efficiency, x, y): # sets up the internal variables 
        self.hp = hp_start
        self.hp_start = hp_start
        self.speed = speed 
        self.energy = e_max 
        self.e_max = e_max 
        self.life = 0
        self.lifespan = lifespan
        self.sence = sence 
        self.efficiency = efficiency 
        self.x = x 
        self.y = y 
    def find_closest(self,instance,quantity) :
        order = {} 
        output_list = [] 
        if instance.casefold().strip() == 'blob' :
            for i in blobs: 
                order.update({numpy.sqrt((i.x - self.x)**2 + (i.y - self.y)**2): i}) 
        if instance.casefold().strip() == 'ooze' : 
            for i in oozes: 
                order.update({numpy.sqrt((i.x - self.x)**2 + (i.y - self.y)**2): i}) 
        if instance.casefold().strip() == 'plant': 
            for i in plants: 
                order.update({numpy.sqrt((i.x - self.x)**2 + (i.y - self.y)**2): i}) 
        sort_order = list(order.keys())
        sort_order.sort()
        out_final = sort_order[0:quantity] 
        for i in out_final: 
            output_list.append(order.get(i))     
        return output_list
    def move_basic(self): 
        direction = random.random()*360
        dist = random.random()*self.speed 
        self.x = self.x + dist*numpy.cos(direction/(2*numpy.pi))
        self.y = self.y + dist*numpy.sin(direction/(2*numpy.pi))
    def eat(self,foods): 
        total_fo = foods
        if isinstance(self, blob) == True:
            self.foods = foods 
            if self.foods > 0 and self.sence > 0 and self.speed > 0 and self.efficiency > 0: 
                a = random.choices((0,1),(1,(2*self.sence))) 
            else: 
                a = [0]
            food = 0 
            if a[0] == 1:                                  #finding food
                food = random.randint(1,4)
                self.energy = self.energy + (food*self.efficiency) 
                if self.energy > self.e_max:               #turning exess energy into hp
                    rem = self.energy - self.e_max
                    self.energy = self.e_max 
                    self.hp = self.hp + rem 
                total_fo = self.foods - food 
        if isinstance(self, ooze) == True: 
            if self.speed > 0 and self.sence > 0 and self.efficiency > 0:           #sees if a ooze finds a blob
                a = random.choices((0,1),(1, self.sence))   #choices weighted by sence
            else: 
                a = [0]
            if a[0] == 1:                   #if they find a blob... 
                meal_list = []
                for i in blobs: 
                    if numpy.sqrt((i.x - self.x)**2 + (i.y - self.y)**2) < self.speed:
                        meal_list.append(i)
                if len(meal_list) > 0: 
                    meal = meal_list[random.randint(0,len(meal_list)-1)] 
                    if self.speed > meal.speed: 
                        self.energy = self.energy + (meal.hp*self.efficiency) 
                    else: 
                        meal.energy = meal.energy - (meal.speed/10)
                    if self.energy > self.e_max:               #turning exess energy into hp
                        rem = self.energy - self.e_max
                        self.energy = self.e_max 
                        self.hp = self.hp + rem 
                    blobs.remove(meal)
        return(total_fo)
    def reproduce(self): 
        if self.hp > self.hp_start*2 and self.energy == self.e_max:    #reproduction 
            b1 = random.triangular(-1,1)                       #mutations 
            c1 = random.triangular(-1,1)
            d1 = random.triangular(-1,1)
            e1 = random.triangular(-1,1)
            f1 = random.triangular(-.1,.1)
            if self.sence + f1 > 1 : 
                f1 = -1*f1 
            g1 = random.triangular(-.1,.1)
            if self.efficiency + g1 > 1: 
                g1 = -1*g1 
            b2 = random.triangular(-1,1)
            c2 = random.triangular(-1,1)
            d2 = random.triangular(-1,1)
            e2 = random.triangular(-1,1)
            f2 = random.triangular(-.1,.1)
            if self.sence + f2 > 1 : 
                f2 = -1*f2 
            g2 = random.triangular(-.1,.1)
            if self.efficiency + g2 > 1: 
                g2 = -1*g2 
            if isinstance(self,blob): 
                h1 = random.randint(-1,1)
                h2 = random.randint(-1,1)
                blob_offspring.append(blob(self.hp_start+b1, self.speed+c1, self.e_max+d1, self.lifespan+e1, self.sence+f1, self.efficiency+g1, self.x+random.triangular(-1,1), self.y+random.triangular(-1,1), self.fear+h1))
                blob_offspring.append(blob(self.hp_start+b2, self.speed+c2, self.e_max+d2, self.lifespan+e2, self.sence+f2, self.efficiency+g2, self.x+random.triangular(-1,1), self.y+random.triangular(-1,1), self.fear+h2))
            if isinstance(self,ooze) and self.hp > self.hp_start*3: 
                ooze_offspring.append(ooze(self.hp_start+b1, self.speed+c1, self.e_max+d1, self.lifespan+e1, self.sence+f1, self.efficiency+g1, self.x+random.triangular(-1,1), self.y+random.triangular(-1,1)))
                ooze_offspring.append(ooze(self.hp_start+b2, self.speed+c2, self.e_max+d2, self.lifespan+e2, self.sence+f2, self.efficiency+g2, self.x+random.triangular(-1,1), self.y+random.triangular(-1,1)))
    def move(self): 
        if isinstance(self, blob) == True:
            if len(oozes) > 0 and self.fear > 0:  
                fear_list = self.find_closest('ooze',self.fear)
                if numpy.sqrt((fear_list[0].x - self.x)**2 + (fear_list[0].y - self.y)**2) < 100*self.sence :
                    angle_list = [] 
                    for i in fear_list:
                        dy = i.y - self.y 
                        dx = i.x - self.x 
                        angle = numpy.arctan(dy/dx) 
                        if dx > 0 :
                            angle = angle + numpy.pi
                        if angle < 0: 
                            angle = angle + 2*numpy.pi
                        angle_list.append(angle)
                    avg_angle = numpy.average(angle_list) 
                    dist = self.speed 
                    self.x = self.x + dist*numpy.cos(avg_angle)            
                    self.y = self.y + dist*numpy.sin(avg_angle)   
                else: 
                    self.move_basic()
            else:
                self.move_basic() 
        if isinstance(self, ooze) == True:
            if len(blobs) > 0: 
                diff = blobs[0] #sets the variable 
                for i in blobs: #iterates through the blobs to find the closest one
                    i_dist = numpy.sqrt((i.x - self.x)**2 + (i.y - self.y)**2)
                    diff_dist = numpy.sqrt((diff.x - self.x)**2 + (diff.y - self.y)**2)
                    if i_dist  < diff_dist: 
                        diff = i 
                diff_dist = numpy.sqrt((diff.x - self.x)**2 + (diff.y - self.y)**2)
                if diff_dist < self.speed: 
                    self.x = diff.x + random.triangular(-.5,.5)
                    self.y = diff.y + random.triangular(-.5,.5)
                else: 
                    direction = numpy.arctan((diff.y - self.y)/(diff.x - self.x))
                    if diff.x < self.x: 
                        direction = direction + numpy.pi 
                    dist = self.speed 
                    self.x = self.x + dist*numpy.cos(direction)            
                    self.y = self.y + dist*numpy.sin(direction) 
            else: 
                direction = random.random()*360
                dist = random.random()*self.speed 
                self.x = self.x + dist*numpy.cos(direction/(2*numpy.pi))
                self.y = self.y + dist*numpy.sin(direction/(2*numpy.pi)) 
    def use_energy(self): 
        self.energy = self.energy - (self.speed/10) 
    def exaustion(self): 
        if self.energy <= 0:                                #exaustion
            self.hp = self.hp - 1 
        if self.hp_start < 2:                               #weakness
            self.hp = self.hp - 1 
    def age(self): 
        self.life = self.life + 1 
    def death(self): 
        if self.hp <= 0 or self.life >= self.lifespan or self.e_max <= 0 or self.hp_start < 1 or (self.hp > self.hp_start*2 and self.energy == self.e_max):                            #death
            if isinstance(self, blob) == True:     
                blobs.remove(self) 
            if isinstance(self, ooze) == True: 
                oozes.remove(self)
    def day(self, foods):
        self.move() 
        self.use_energy                                     #energy usage
        total_fo = self.eat(foods)                          #eating food 
        self.exaustion() 
        self.reproduce()                                    #reproduction
        self.age() 
        self.death() 
        return total_fo

class blob(organism): 
    def __init__(self, hp_start, speed, e_max, lifespan, sence, efficiency, x, y, fear=2):
        super().__init__(hp_start, speed, e_max, lifespan, sence, efficiency, x, y)
        self.fear = fear
#    def eat(self, foods):
#        pass 
#        total_fo = foods
#        if isinstance(self, blob) == True:
#            self.foods = foods 
#            if self.foods > 0 and self.sence > 0 and self.speed > 0 and self.efficiency > 0: 
#                a = random.choices((0,1),(1,(2*self.sence))) 
#            else: 
#                a = [0]
#            food = 0 
#            if a[0] == 1:                                  #finding food
#                food = random.randint(1,4)
#                self.energy = self.energy + (food*self.efficiency) 
#                if self.energy > self.e_max:               #turning exess energy into hp
#                    rem = self.energy - self.e_max
#                    self.energy = self.e_max 
#                    self.hp = self.hp + rem 
#                total_fo = self.foods - food 
#            return(total_fo) 
        
class ooze(organism): 
    def __init__(self, hp_start, speed, e_max, lifespan, sence, efficiency, x, y):
        super().__init__(hp_start, speed, e_max, lifespan, sence, efficiency, x, y)

class plant(organism): 
    def __init__(self, hp_start, speed, e_max, lifespan, sence, efficiency, x, y, seed_spread, seed_count):   
        super().__init__(hp_start, speed, e_max, lifespan, sence, efficiency, x, y)
        self.seed_spread = seed_spread 
        self.seed_count = seed_count 
        self.e_max = e_max 
        self.hp_start = hp_start 
        self.energy = e_max 
        self.lifespan = lifespan 
        self.efficiency = efficiency 
        self.x = x 
        self.y = y 
        self.hp = hp_start
    def photosynthesize(self,world_light): 
        self.energy = self.energy + self.efficiency*world_light 
        if self.energy > self.e_max:               #turning exess energy into hp
            rem = self.energy - self.e_max
            self.energy = self.e_max 
            self.hp = self.hp + rem 
    def age(self): 
        self.life = self.life + 1 
    def death(self): 
        if self.hp <= 0 or self.life >= self.lifespan or self.e_max <= 0 or self.hp_start < 1:                            #death
            plants.remove(self)
    def reproduce(self): 
        if self.hp > 4*self.hp_start and self.energy >= self.e_max: 
            for i in range(round(self.seed_count)):
                b = random.triangular(-1,1)                       #mutations 
                c = random.triangular(-1,1)
                d = random.triangular(-1,1)
                e = random.triangular(-.1,.1)
                f = random.triangular(-self.seed_spread,self.seed_spread)
                g = random.triangular(-self.seed_spread,self.seed_spread)
                h = random.triangular(-1,1) 
                i = random.triangular(-1,1)
                plant_offspring.append(plant(self.hp_start + b, self.speed, self.e_max + c, self.lifespan + d, self.speed, self.efficiency + e, self.x + f, self.y + g, self.seed_spread + h, self.seed_count + i))
                self.hp = self.hp_start
                self.energy = self.energy/2
    def day(self,world_light): 
        self.photosynthesize(world_light) 
        self.reproduce() 
        self.age() 
        self.death() 

for i in range (300):
    blobs.append(blob(random.randint(5,10),random.randint(2,7),random.randint(2,7),45,.5,.5,random.random()*10, random.random()*10))

for i in range(50): 
    oozes.append(ooze(random.randint(5,10),random.randint(4,8),random.randint(2,7),45,.5,.5,random.random()*10, random.random()*10))

#for i in range(3): 
#    plants.append(plant(random.randint(5,10),random.randint(2,7),random.randint(2,7),45,.5,.5,random.random()*50, random.random()*50, 2, 2))

def time(days,clip): 
    global day_count 
    global x_vals 
    global total_food
    global duration 
    global blob_y_hp_start 
    global blob_y_speed 
    global blob_y_e_max 
    global blob_y_lifespan
    global blob_y_sence
    global blob_y_efficiency 
    global ooze_y_hp_start 
    global ooze_y_speed 
    global ooze_y_e_max 
    global ooze_y_lifespan
    global ooze_y_sence
    global ooze_y_efficiency 
    global blob_offspring 
    global ooze_offspring 
    global blob_x 
    global blob_y
    global ooze_x
    global ooze_y
    global blob_polulation 
    global ooze_population
    global fears_list
    global plant_offspring
    avg_sence = 0
    for j in range(days):
        random.shuffle(blobs)
        random.shuffle(oozes)
        total_food = total_food + 50 
        plant_offspring = [] 
        for i in blobs: 
            total_food = i.day(total_food)
        for i in oozes: 
            total_food = i.day(total_food)
        for i in plants: 
            i.day(world_light)
        for i in range(len(blob_offspring)): 
            blobs.append(blob_offspring[i])
        for i in range(len(ooze_offspring)): 
            oozes.append(ooze_offspring[i])
        for i in range(len(plant_offspring)): 
            plants.append(plant_offspring[i]) 
        blob_offspring = [] 
        ooze_offspring = [] 

        hp_start_list = []
        speed_list = []
        e_max_list = []
        lifespan_list = []
        sence_list = [] 
        efficiency_list = [] 
        blob_x = [] 
        blob_y = []
        ooze_x = []
        ooze_y = [] 
        plant_x = [] 
        plant_y = [] 
        fears = [] 
        day_count = day_count + 1 
        avg_hp_start = 0
        avg_speed = 0
        avg_e_max = 0
        avg_lifespan = 0 
        avg_sence = 0
        avg_efficiency = 0
        avg_fear = 0 
        for i in blobs: 
            hp_start_list.append(i.hp_start)
            speed_list.append(i.speed)
            e_max_list.append(i.e_max)
            lifespan_list.append(i.lifespan)
            sence_list.append(i.sence)
            efficiency_list.append(i.efficiency)
            blob_x.append(i.x) 
            blob_y.append(i.y)
            fears.append(i.fear)
        if len(hp_start_list) > 0:
            avg_hp_start = numpy.mean(hp_start_list)
        if len(speed_list) > 0: 
            avg_speed = numpy.mean(speed_list)
        if len(e_max_list) > 0: 
            avg_e_max = numpy.mean(e_max_list)
        if len(lifespan_list) > 0: 
            avg_lifespan = numpy.mean(lifespan_list)
        if len(sence_list) > 0: 
            avg_sence = numpy.mean(sence_list)
        if len(efficiency_list) > 0: 
            avg_efficiency = numpy.mean(efficiency_list)
        if len(fears) > 0: 
            avg_fear = numpy.mean(fears)
        blob_y_hp_start.append(avg_hp_start)
        blob_y_speed.append(avg_speed) 
        blob_y_e_max.append(avg_e_max)
        blob_y_lifespan.append(avg_lifespan)
        blob_y_sence.append(avg_sence)
        blob_y_efficiency.append(avg_efficiency)
        fears_list.append(avg_fear)
        hp_start_list = []
        speed_list = []
        e_max_list = []
        lifespan_list = []
        sence_list = [] 
        efficiency_list = [] 
        avg_hp_start = 0
        avg_speed = 0
        avg_e_max = 0
        avg_lifespan = 0 
        avg_sence = 0
        avg_efficiency = 0
        for i in oozes: 
            hp_start_list.append(i.hp_start)
            speed_list.append(i.speed)
            e_max_list.append(i.e_max)
            lifespan_list.append(i.lifespan)
            sence_list.append(i.sence)
            efficiency_list.append(i.efficiency)
            ooze_x.append(i.x) 
            ooze_y.append(i.y)
        if len(hp_start_list) > 0:
            avg_hp_start = numpy.mean(hp_start_list)
        if len(speed_list) > 0: 
            avg_speed = numpy.mean(speed_list)
        if len(e_max_list) > 0: 
            avg_e_max = numpy.mean(e_max_list)
        if len(lifespan_list) > 0: 
            avg_lifespan = numpy.mean(lifespan_list)
        if len(sence_list) > 0: 
            avg_sence = numpy.mean(sence_list)
        if len(efficiency_list) > 0: 
            avg_efficiency = numpy.mean(efficiency_list)
        ooze_y_hp_start.append(avg_hp_start)
        ooze_y_speed.append(avg_speed) 
        ooze_y_e_max.append(avg_e_max)
        ooze_y_lifespan.append(avg_lifespan)
        ooze_y_sence.append(avg_sence)
        ooze_y_efficiency.append(avg_efficiency)
        x_vals.append(day_count) 
        blob_population.append(len(blobs))
        ooze_population.append(len(oozes))
        for i in plants: 
            plant_x.append(i.x)
            plant_y.append(i.y) 
        if len(blob_y_hp_start) > 100 and clip == True: 
            format_blob_hp_start = blob_y_hp_start[-100:-1] 
            format_ooze_hp_start = ooze_y_hp_start[-100:-1] 
            format_blob_speed = blob_y_speed[-100:-1] 
            format_ooze_speed = ooze_y_speed[-100:-1] 
            format_blob_e_max = blob_y_e_max[-100:-1] 
            format_ooze_e_max = ooze_y_e_max[-100:-1] 
            format_blob_population = blob_population[-100:-1]
            format_ooze_population = ooze_population[-100:-1]
            format_blob_efficiency = blob_y_efficiency[-100:-1] 
            format_ooze_efficiency = ooze_y_efficiency[-100:-1] 
            format_blob_sence = blob_y_sence[-100:-1] 
            format_ooze_sence = ooze_y_sence[-100:-1] 
            format_fears = fears_list[-100:-1]
            format_x_vals = x_vals[-100:-1]
        else: 
            format_blob_hp_start = blob_y_hp_start 
            format_ooze_hp_start = ooze_y_hp_start 
            format_blob_speed = blob_y_speed 
            format_ooze_speed = ooze_y_speed 
            format_blob_e_max = blob_y_e_max
            format_ooze_e_max = ooze_y_e_max
            format_blob_population = blob_population
            format_ooze_population = ooze_population
            format_blob_efficiency = blob_y_efficiency 
            format_ooze_efficiency = ooze_y_efficiency 
            format_blob_sence = blob_y_sence 
            format_ooze_sence = ooze_y_sence
            format_fears = fears_list
            format_x_vals = x_vals
    plt.close() 
    fig, (ax1) = plt.subplots(2, 2)
    ax1[0,0].set_title('hpstart, speed, emax')
    ax1[0,0].plot(format_x_vals, format_blob_hp_start, color = 'green')
    ax1[0,0].plot(format_x_vals, format_blob_speed, color = 'red')
    ax1[0,0].plot(format_x_vals, format_blob_e_max, color = 'blue')
    ax1[0,0].plot(format_x_vals, format_ooze_hp_start, color = 'green', ls = ':')
    ax1[0,0].plot(format_x_vals, format_ooze_speed, color = 'red', ls = ':')
    ax1[0,0].plot(format_x_vals, format_ooze_e_max, color = 'blue', ls = ':')
    ax1[0,0].plot(format_x_vals, format_fears, color = 'orange')
    ax1[1,0].set_title('population')
    ax1[1,0].plot(format_x_vals, format_blob_population, color = 'black')
    ax1[1,0].plot(format_x_vals, format_ooze_population, color = 'black', ls = ':')
    ax1[0,1].set_title('positions')
    ax1[0,1].scatter(blob_x, blob_y, 1, color = 'blue')
    ax1[0,1].scatter(ooze_x, ooze_y, 1, color = 'red')
    ax1[0,1].scatter(plant_x, plant_y, 1, color = 'green')
    ax1[1,1].set_title('efficiency, sence')
    ax1[1,1].plot(format_x_vals, format_blob_efficiency, color = 'purple')
    ax1[1,1].plot(format_x_vals, format_blob_sence, color = 'brown')
    ax1[1,1].plot(format_x_vals, format_ooze_efficiency, color = 'purple', ls = ':')
    ax1[1,1].plot(format_x_vals, format_ooze_sence, color = 'brown', ls = ':')
    plt.show()
    print('Blob/Ooze Average Starting HP:', round(blob_y_hp_start[-1],2), '/', round(ooze_y_hp_start[-1],2))
    print('BLob/Ooze Average Speed:      ', round(blob_y_speed[-1],2), '/', round(ooze_y_speed[-1],2))
    print('Blob/Ooze Average Energy Max: ', round(blob_y_e_max[-1],2), '/', round(ooze_y_e_max[-1],2)) 
    print('Blob/Ooze Average Lifespan:   ', round(blob_y_lifespan[-1],2), '/', round(ooze_y_lifespan[-1],2)) 
    print('Blob/Ooze Average Sence:      ', round(blob_y_sence[-1],2), '/', round(ooze_y_sence[-1],2))
    print('Blob/Ooze Average Efficiency: ', round(blob_y_efficiency[-1],2), '/', round(ooze_y_efficiency[-1],2))
    print('Blob/Ooze Population:         ', len(blobs), '/', len(oozes))
            

            
        