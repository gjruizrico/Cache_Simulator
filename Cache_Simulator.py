# -*- coding: utf-8 -*-
"""
CS472 Spring 2019 at Boston University - Project #2: Cache Simulation.
Deliverable by Guillermo Ruiz-Rico using Python 3.7.1,  Spyder and PyCharm as IDEs.
"""
##################################### Step 1 - Create and initialize arrays. Set up the bitwise method. #####################################
MM = [0x00]*2048 #Main Memory array of 2048 elements.
MMCounter = 0x00 #This is used below to initialize the Main Memory array.
for x in range(len(MM)): #Initialize Main Memory from 0x00 to 0xFF
    if MMCounter > 0xFF:
        MMCounter = 0
    MM[x] = hex(MMCounter)
    MMCounter += 1

#Block with 16 slots created in this order: 1.Slots, 2.Valid boolean, 3.Tag,  4.Data and 5.Dirty Bit
Slot = [0x0]*16 #16 slots
for x in range(len(Slot)):#Initialize by incrementing values from 0 to F.
    Slot[x] = hex(x)
Valid = [0x0]*16 #Valid for each slot. Set to 0.
Tag = [0x0]*16 #Tag for each slot. Set to 0.
Data = [[0x00] * 16 for i in range(16)] #This is the actual slot content. Set to 0. It is a list of 16 elements, each of them a list themselves with 16 items too.
Dirty = [0x0]*16 #Dirty Bit for each slot. Set to 0.This is also shown in the "Display" output.

def AddressBitwiser(Address):#Define a method to obtain output via bitwise and shift.
    AddressBitwiser.Slot= (Address & 0xf0) >> 4
    AddressBitwiser.Tag = Address >> 8
    AddressBitwiser.Offset = (Address & 0xf)
    AddressBitwiser.AddressStart = (Address & 0xfff0)
    return hex(AddressBitwiser.Tag).upper(), hex(AddressBitwiser.Slot).upper(), hex(AddressBitwiser.Offset).upper(), hex(AddressBitwiser.AddressStart).upper() #The AddressStart will be useful to determine what to bring from Main Memory.

##################################### Step 2 - Ask the user and perform appropriate actions. #####################################
QuestionCounter = 0
QuestionCap = 100
UserInput = ""
while QuestionCounter < QuestionCap:
  UserInput = input("Please type in 'D' to Display Cache, 'R' to Read Byte, 'W' to Write Byte or 'exit' to end this program.")

  if UserInput == "exit":
      print("You chose to exit the program. Goodbye now.")
      QuestionCounter = QuestionCap #To exit the loop and finish the script, the counter's variable is assigned the cap's value.


  elif UserInput == "R" or UserInput == "r": #This part handles Read operations.
      StringAddress = input("Please specify an address to be read.")
      Address = int(StringAddress, 16) #Python takes all user input as strings, hence they must be converted to an int of base 16.
      AddressBitwiser(Address) #Run address through the Bitwiser method.
      if (Tag[AddressBitwiser.Slot] == AddressBitwiser.Tag) and (Valid[AddressBitwiser.Slot] == 1): #Code for Read Cache Hit starts here.
            print("At that byte there is the value " + Data[AddressBitwiser.Slot][AddressBitwiser.Offset] + " (Cache Hit)")
      else: #Code for Read Cache Miss starts here.
          if (Dirty[AddressBitwiser.Slot] == 1):
                for x in range(len(Data[AddressBitwiser.Slot])): #Write back to main memory prior to overwriting with main memory pattern based on the address to be read.
                    MM[(AddressBitwiser.AddressStart) + x] = Data[AddressBitwiser.Slot][x]
                Dirty[AddressBitwiser.Slot] = 0 #Update that slot's dirty bit to 0 after the write back.
          Valid[AddressBitwiser.Slot] = 1 #Set Valid bit to 1.
          Tag[AddressBitwiser.Slot] = AddressBitwiser.Tag #Get tag from entered address.
          for x in range(len(Data[AddressBitwiser.Slot])): #Bring MM's data to the cache since it was a miss.
              Data[AddressBitwiser.Slot][x] = MM[(AddressBitwiser.AddressStart)+x]
          print("At that byte there is the value " + Data[AddressBitwiser.Slot][AddressBitwiser.Offset] + " (Cache Miss)")


  elif UserInput == "W" or UserInput == "w": #This part handles Write operations.
      StringAddress = input("Please specify an address to write to.")
      Address = int(StringAddress, 16) #Python takes all user input as strings, hence they must be converted to an int of base 16.
      AddressBitwiser(Address) #Run address through the Bitwiser method.
      StringWriteData = input("Please specify the data you would like to write on address "+ str(hex(Address)) + ".")
      WriteData = int(StringWriteData, 16)
      if (Tag[AddressBitwiser.Slot] == AddressBitwiser.Tag) and (Valid[AddressBitwiser.Slot] == 1): #Code for Write Cache Hit starts here.
            Data[AddressBitwiser.Slot][AddressBitwiser.Offset] = hex(WriteData) #Locate element within the Data list of lists and overwrite value based on input.
            Dirty[AddressBitwiser.Slot] = 1 #Update that slot's dirty bit to 1 after the change deriving from this write operation and the fact that we are not bringing the slot to Main Memory.
            print("Value " + str(hex(WriteData)) + " has been written to address " + str(hex(Address) + " (Cache Hit)"))
      else:#Code for Write Cache Miss starts here
          if (Dirty[AddressBitwiser.Slot] == 1):
                for x in range(len(Data[AddressBitwiser.Slot])):  #Write back to main memory.
                    MM[(AddressBitwiser.AddressStart) + x] = Data[AddressBitwiser.Slot][x]
                Dirty[AddressBitwiser.Slot] = 0 #Update that slot's dirty bit to 0 after the write back.
          Valid[AddressBitwiser.Slot] = 1 #Set Valid bit to 1.
          Tag[AddressBitwiser.Slot] = AddressBitwiser.Tag #Get tag from entered address.
          for x in range(len(Data[AddressBitwiser.Slot])): #Bring main memory's data to the cache since it was a Cache Miss.
              Data[AddressBitwiser.Slot][x] = MM[(AddressBitwiser.AddressStart)+x]
          Data[AddressBitwiser.Slot][AddressBitwiser.Offset] = hex(WriteData)#Locate element within the Data list of lists and overwrite value based on input.
          Dirty[AddressBitwiser.Slot] = 1 #Reset the dirty bit to 1 since the previous statement just made a  new write that will not be brought into Main Memory yet.
          print("Value " + str(hex(WriteData)) + " has been written to address " + str(hex(Address) + " (Cache Miss)"))


  elif UserInput == "D" or UserInput == "d": #This part handles Display operations.
      print("Dirty  Slot  Valid  Tag     Data")
      for x in range(len(Data)):
        print(Dirty [x], '    ',Slot[x], '   ',Valid[x], '   ', Tag[x], '    ', (*Data[x]))
        print #This statement starts a new line for presentation purposes.
  else:
     print("Please try again.") #This is in case the user types something other than the allowed 3 options.
  QuestionCounter += 1 #Increment the counter to reach set maximum or until the user enters "exit". This is the end of the for-loop.