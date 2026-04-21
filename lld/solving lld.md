# Framework

## clarify & scope
- what are clarifying questions?
  - example? "Are we handling just one type of vehicle or multiple types?"
- what is scope and how is it different? ("must-have" vs "nice-to-have" features)
  - example? "For the parking lot, let's start with cars only and a single entry/exit gate. We can discuss different vehicle types and multiple gates as extensions. Does that sound good?"
- what are requirements then?


## core objects & relationships
- how to identify the core classes and methods from requirements? (nouns, verbs)
  - example? The nouns are your potential classes (Vehicle, ParkingSpot, Ticket). The verbs are your methods (parkVehicle(), calculateFee())
- how to define class properties, relationships? 
  - example? What does each class need to know? A Vehicle needs a licensePlate. A Ticket needs an entryTime and is associated with a Vehicle and a ParkingSpot


## code the core logic
1. start with simple classes representing core objects
    - example? (Vehicle, Spot, etc)
2. implement controller or Orchestrator of workflow
    - example? ParkingLot
3. Focus on happy path
    - example? a car successfully parks and unparks, don't worry about all the edge cases initially. write clean, readable code

## refactor & discuss extensions
1. apply design patterns
    - example? instead of putting pricing logic inside the ParkingLot class, to make the core more modular, refactor it out into a FeeCalculationStrategy class.
2. address extensions (nice to have features)
    - example? To support motorcycles and trucks, I would make Vehicle a base class and create subclasses. Then, I'd use a Factory pattern to create the correct vehicle object
3. discuss principles
    - example? Talk about concurrency (threading.Lock to prevent race conditions), error handling (custom exceptions), and persistence (using a database)
4. what are some of the useful design patterns?
  - strategy:
  - factory
  - observer
  - singleton
  
  
  # designing a parking lot system
  ## 1. clarifying the requirments
  
  The system should be able to:
  - find an available parking sport for a vehicle
  - park a vehicle in that spot
  - issue a ticket for the parked vehicle
  - allow the vehicle to exit, calculate the fee and free up the spot
  
  initially we are considering one type of vehicle and all parking spots are same
  
  ## 2. initial design
  
  nouns:
  - Vehicle: needs an identifier, license plate number
  - ParkingSpot: needs a spot number, whether it was occupied
  - Ticket: link vehicle to the spot, record entry time
  - ParkingLot: main container. it needs to know all its parking spots. It's main jobs are to park a vehicle(find a spot and issue a ticket) and unpark a vehicle (process the ticket and free the spot)
  
  
  ## 3. translating initial design to code
  
  ```python
  # v1
  import datetime
 import uuid 
 
 class Vehicle:
    def __init__(self, license_plate):
        self.license_plate = license_plate
    
class 
  
  
  ```
  ## 4. adding more details: iteration 1
