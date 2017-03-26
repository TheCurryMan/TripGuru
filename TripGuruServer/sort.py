import math
import random
import json
import requests


class City:
   def __init__(self, name, x=None, y=None):
      self.name = name
      self.x = None
      self.y = None
      if x is not None:
         self.x = x
      else:
         self.x = int(random.random() * 200)
      if y is not None:
         self.y = y
      else:
         self.y = int(random.random() * 200)
   
   def getX(self):
      return self.x
   
   def getY(self):
      return self.y

   def getName(self):
      return self.name
   
   def distanceTo(self, city):
      lat1 = math.radians(self.x)
      lat2 = math.radians(self.y)
      lng1 = math.radians(city.x)
      lng2 = math.radians(city.y)
      a = (math.pow(math.sin((lat2-lat1)/2), 2) + math.cos(lat1)*math.cos(lat2)*math.pow(math.sin((lng2-lng1)/2,2)))
      c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
      #Radius of earth (m)
      R = 6371000
      dist = R * c
      return dist
   
   def __repr__(self):
      return str(self.getX()) + ", " + str(self.getY())


class TourManager:
   destinationCities = []
   
   def addCity(self, city):
      self.destinationCities.append(city)
   
   def getCity(self, index):
      return self.destinationCities[index]
   
   def numberOfCities(self):
      return len(self.destinationCities)


class Tour:
   def __init__(self, tourmanager, tour=None):
      self.tourmanager = tourmanager
      self.tour = []
      self.fitness = 0.0
      self.distance = 0
      if tour is not None:
         self.tour = tour
      else:
         for i in range(0, self.tourmanager.numberOfCities()):
            self.tour.append(None)
   
   def __len__(self):
      return len(self.tour)
   
   def __getitem__(self, index):
      return self.tour[index]
   
   def __setitem__(self, key, value):
      self.tour[key] = value
   
   def __repr__(self):
      geneString = "|"
      for i in range(0, self.tourSize()):
         geneString += str(self.getCity(i)) + "|"
      return geneString
   
   def generateIndividual(self):
      for cityIndex in range(0, self.tourmanager.numberOfCities()):
         self.setCity(cityIndex, self.tourmanager.getCity(cityIndex))
      random.shuffle(self.tour)
   
   def getCity(self, tourPosition):
      return self.tour[tourPosition]
   
   def setCity(self, tourPosition, city):
      self.tour[tourPosition] = city
      self.fitness = 0.0
      self.distance = 0
   
   def getFitness(self):
      if self.fitness == 0:
         self.fitness = 1/float(self.getDistance())
      return self.fitness
   
   def getDistance(self):
      if self.distance == 0:
         tourDistance = 0
         for cityIndex in range(0, self.tourSize()):
            fromCity = self.getCity(cityIndex)
            destinationCity = None
            if cityIndex+1 < self.tourSize():
               destinationCity = self.getCity(cityIndex+1)
            else:
               destinationCity = self.getCity(0)
            tourDistance += fromCity.distanceTo(destinationCity)
         self.distance = tourDistance
      return self.distance
   
   def tourSize(self):
      return len(self.tour)
   
   def containsCity(self, city):
      return city in self.tour


class Population:
   def __init__(self, tourmanager, populationSize, initialise):
      self.tours = []
      for i in range(0, populationSize):
         self.tours.append(None)
      
      if initialise:
         for i in range(0, populationSize):
            newTour = Tour(tourmanager)
            newTour.generateIndividual()
            self.saveTour(i, newTour)
      
   def __setitem__(self, key, value):
      self.tours[key] = value
   
   def __getitem__(self, index):
      return self.tours[index]
   
   def saveTour(self, index, tour):
      self.tours[index] = tour
   
   def getTour(self, index):
      return self.tours[index]
   
   def getFittest(self):
      fittest = self.tours[0]
      for i in range(0, self.populationSize()):
         if fittest.getFitness() <= self.getTour(i).getFitness():
            fittest = self.getTour(i)
      return fittest
   
   def populationSize(self):
      return len(self.tours)


class GA:
   def __init__(self, tourmanager):
      self.tourmanager = tourmanager
      self.mutationRate = 0.015
      self.tournamentSize = 5
      self.elitism = True
   
   def evolvePopulation(self, pop):
      newPopulation = Population(self.tourmanager, pop.populationSize(), False)
      elitismOffset = 0
      if self.elitism:
         newPopulation.saveTour(0, pop.getFittest())
         elitismOffset = 1
      
      for i in range(elitismOffset, newPopulation.populationSize()):
         parent1 = self.tournamentSelection(pop)
         parent2 = self.tournamentSelection(pop)
         child = self.crossover(parent1, parent2)
         newPopulation.saveTour(i, child)
      
      for i in range(elitismOffset, newPopulation.populationSize()):
         self.mutate(newPopulation.getTour(i))
      
      return newPopulation
   
   def crossover(self, parent1, parent2):
      child = Tour(self.tourmanager)
      
      startPos = int(random.random() * parent1.tourSize())
      endPos = int(random.random() * parent1.tourSize())
      
      for i in range(0, child.tourSize()):
         if startPos < endPos and i > startPos and i < endPos:
            child.setCity(i, parent1.getCity(i))
         elif startPos > endPos:
            if not (i < startPos and i > endPos):
               child.setCity(i, parent1.getCity(i))
      
      for i in range(0, parent2.tourSize()):
         if not child.containsCity(parent2.getCity(i)):
            for ii in range(0, child.tourSize()):
               if child.getCity(ii) == None:
                  child.setCity(ii, parent2.getCity(i))
                  break
      
      return child
   
   def mutate(self, tour):
      for tourPos1 in range(0, tour.tourSize()):
         if random.random() < self.mutationRate:
            tourPos2 = int(tour.tourSize() * random.random())
            
            city1 = tour.getCity(tourPos1)
            city2 = tour.getCity(tourPos2)
            
            tour.setCity(tourPos2, city1)
            tour.setCity(tourPos1, city2)
   
   def tournamentSelection(self, pop):
      tournament = Population(self.tourmanager, self.tournamentSize, False)
      for i in range(0, self.tournamentSize):
         randomId = int(random.random() * pop.populationSize())
         tournament.saveTour(i, pop.getTour(randomId))
      fittest = tournament.getFittest()
      return fittest

def sortAttractions(data):
   tour_manager = TourManager()
   list_of_places = []
   list_of_cities = []
   ordered_list_of_places = []
   newData = data.split('|')
   latestData = [w.split(',') for w in newData]
   for string in latestData:
      tour_manager.addCity(City(string[0], string[1], string[2]))
      list_of_places.append(string[0])
      list_of_cities.append(City(string[0], string[1], string[2]))
   #Initialize pop and run GA
   pop = Population(tour_manager, 50, True);
   print "Initial distance: " + str(pop.getFittest().getDistance())
   
   # Evolve population for 50 generations
   ga = GA(tour_manager)
   pop = ga.evolvePopulation(pop)
   for i in range(0, 100):
      pop = ga.evolvePopulation(pop)
   
   bestPop = pop.getFittest()

   for city in bestPop:
      ordered_list_of_places.append(city.getName())
   list_of_durations = getTime(ordered_list_of_places)
   dictionary = dict(zip(ordered_list_of_places,list_of_durations))
   final = json.dumps(dictionary)
   return final

def getTime(self, list_of_cities):
   d = {}
   d['origin'] = list_of_cities[0].getX() + "," + list_of_cities[0].getY()
   d['destination'] = list_of_cities[len(list_of_cities) - 1].getX() + "," + list_of_cities[len(list_of_cities) - 1].getY()
   if(len(list_of_cities) > 2):
      waypoint = list_of_cities[2].getX() + "," + list_of_cities[2].getY() + "|"
   for city in list_of_cities[2:(len(list_of_cities) - 3)]:
      waypoint += city.getX() + "," + city.getY() + "|"
   waypoint += list_of_cities[len(list_of_cities) - 2].getX() + "," + list_of_cities[len(list_of_cities) - 2].getY()
   d['waypoint'] = waypoint
   d['key'] = "AIzaSyA_KUnYEKuOodre8lcfEhYQZbwmQhxqgwY"
   r = requests.get("https://maps.googleapis.com/maps/api/directions/json?", d)
   data = r.text
   data = convert(data)
   final = json.loads(data)
   list_of_durations = []
   list_of_durations.append(1)
   for leg in final['routes'][0]['legs']:
      list_of_durations.append(int(['duration']['value'])+1)
   return list_of_durations

def totalTime(self, list_of_cities):
   list_of_durations = getTime(list_of_cities)
   totalDur = 0
   for d in list_of_durations:
      totalDur += d
   return totalDur

   
   


