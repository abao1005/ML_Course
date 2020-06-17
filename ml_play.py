class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        self.isLeft = False
        self.isPerfect = 0
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
     10 |  1 |  2 |  3 | 13
        |    |  5 |    |
     11 |  4 |  c |  6 | 14
        |    |    |    |
     12 |  7 |  8 |  9 | 15
        |    |    |    |       
        """
        def check_grid():
            grid = set()
            speed_ahead = 100
            if self.car_pos[0] <= 39: # left bound
                grid.add(1)
                grid.add(4)
                grid.add(7)
            elif self.car_pos[0] >= 591: # right bound
                grid.add(3)
                grid.add(6)
                grid.add(9)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 40 and x >= -40 :      
                        if y > 0 and y < 240:
                            grid.add(2)
                            if y < 170:
                                speed_ahead = car["velocity"]
                                grid.add(5) 
                        elif y < 0 and y > -150:
                            grid.add(8)
                    if x >= -80 and x < -40 :
                        if y > 80 and y < 250:
                            grid.add(3)
                        elif y < -80 and y > -110:
                            grid.add(9)
                        elif y < 80 and y > -80:
                            grid.add(6)
                    if x <= 80 and x > 40:
                        if y > 80 and y < 250:
                            grid.add(1)
                        elif y < -80 and y > -110:
                            grid.add(7)
                        elif y < 80 and y > -80:
                            grid.add(4)
                    if x <= 150 and x > 80:
                        if y > 80 and y < 250:
                            grid.add(10)
                        elif y < 80 and y > -80:
                            grid.add(11)
                    if x >= -150 and x < -80 :
                        if y > 80 and y < 250:
                            grid.add(13)
                        elif y < 80 and y > -80:
                            grid.add(14)
                    if self.isPerfect == 1:
                        grid.add(3)
                    elif self.isPerfect == 2:
                        grid.add(1)
            return move(grid= grid, speed_ahead = speed_ahead)
            
        def move(grid, speed_ahead): 
            if self.player_no == 0:
                print(grid)
            if ((1 not in grid) and (2 not in grid) and (3 not in grid) and(4 not in grid) and (5 not in grid)and(6 not in grid)) or (self.car_pos[0] <= self.lanes[0]+5 and (2 not in grid) and (3 not in grid) and(5 not in grid)and(6 not in grid)) or (self.car_pos[0] >= self.lanes[8]-5 and (1 not in grid) and (2 not in grid) and(4 not in grid)and(5 not in grid)):
                if(self.car_pos[0]>315):
                    self.isLeft = True
                    return ["SPEED", "MOVE_LEFT"]
                elif(self.car_pos[0]<315):
                    self.isLeft = False
                    return ["SPEED", "MOVE_RIGHT"]
                return ["SPEED"]
            else:
                if (2 not in grid): # Check forward 
                    # Back to lane center
                    if self.car_pos[0] > self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_RIGHT"]
                    else :return ["SPEED"]
                else:
                    if (5 in grid) and self.isLeft == True: # NEED to BRAKE
                        if (1 not in grid) and (4 not in grid):
                            self.isPerfect = 0
                            print("我在卡你1")
                            self.isLeft = True
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        elif (3 not in grid) and (6 not in grid):
                            self.isPerfect = 0
                            print("我在卡你2")
                            self.isLeft = False
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        if (1 in grid) and (3 in grid) and (4 not in grid) and (6 not in grid): #perfect
                            if(10 not in grid) and (11 not in grid): 
                                self.isPerfect = 1
                                print("perfect left with 5")
                                self.isLeft = True
                                if self.car_vel < speed_ahead:
                                    return ["SPEED", "MOVE_LEFT"]
                                else:
                                    return ["BRAKE", "MOVE_LEFT"]
                            elif(13 not in grid) and (14 not in grid):
                                self.isPerfect = 2
                                print("perfect right with 5")
                                self.isLeft = False
                                if self.car_vel < speed_ahead:
                                    return ["SPEED", "MOVE_RIGHT"]
                                else:
                                    return ["BRAKE", "MOVE_RIGHT"]
                        
                        if (4 not in grid) and (1 not in grid): # turn left 
                            self.isPerfect = 0
                            print("我在卡你3")
                            self.isLeft = True
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        elif (6 not in grid) and (3 not in grid): # turn right
                            self.isPerfect = 0
                            print("我在卡你4")
                            self.isLeft = False
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        
                        else : 
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]

                    elif (5 in grid) and self.isLeft == False:
                        if (3 not in grid) and (6 not in grid):
                            self.isPerfect = 0
                            print("我在卡你5")
                            self.isLeft = False
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        elif (1 not in grid) and (4 not in grid):
                            self.isPerfect = 0
                            print("我在卡你6")
                            self.isLeft = True
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        if (1 in grid) and (3 in grid) and (4 not in grid) and (6 not in grid): #perfect
                            if(13 not in grid) and (14 not in grid):
                                self.isPerfect = 2
                                print("perfect right with 5")
                                self.isLeft = False
                                if self.car_vel < speed_ahead:
                                    return ["SPEED", "MOVE_RIGHT"]
                                else:
                                    return ["BRAKE", "MOVE_RIGHT"]
                            elif(10 not in grid) and (11 not in grid): 
                                self.isPerfect = 1
                                print("perfect left with 5")
                                self.isLeft = True
                                if self.car_vel < speed_ahead:
                                    return ["SPEED", "MOVE_LEFT"]
                                else:
                                    return ["BRAKE", "MOVE_LEFT"]

                        if (6 not in grid) and (3 not in grid): # turn right
                            self.isPerfect = 0
                            print("我在卡你7")
                            self.isLeft = False
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                return ["BRAKE", "MOVE_RIGHT"]
                        elif (4 not in grid) and (1 not in grid): # turn left
                            self.isPerfect = 0
                            print("我在卡你8") 
                            self.isLeft = True
                            if self.car_vel < speed_ahead:
                                return ["SPEED", "MOVE_LEFT"]
                            else:
                                return ["BRAKE", "MOVE_LEFT"]
                        else : 
                            if self.car_vel < speed_ahead:  # BRAKE
                                return ["SPEED"]
                            else:
                                return ["BRAKE"]
                  
                    if(self.isLeft == True):
                        if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                            self.isPerfect = 0
                            print("我在卡你9")
                            self.isLeft = True
                            return ["SPEED", "MOVE_LEFT"]
                        elif (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            self.isPerfect = 0
                            print("我在卡你10")
                            self.isLeft = False
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 in grid) and (3 in grid) and (4 not in grid) and (6 not in grid): #perfect
                            if(10 not in grid) and (11 not in grid): 
                                self.isPerfect = 1
                                print("perfect left without 5")
                                self.isLeft = True
                                return ["SPEED", "MOVE_LEFT"]
                            elif(13 not in grid) and (14 not in grid):
                                self.isPerfect = 2
                                print("perfect right without 5")
                                self.isLeft = False
                                return ["SPEED", "MOVE_RIGHT"]
                        
                        if (1 not in grid) and (4 not in grid): # turn left 
                            self.isPerfect = 0
                            print("我在卡你11")
                            self.isLeft = True
                            return ["SPEED", "MOVE_LEFT"]
                        elif (3 not in grid) and (6 not in grid): # turn right
                            self.isPerfect = 0
                            print("我在卡你12")
                            self.isLeft = False
                            return ["SPEED", "MOVE_RIGHT"]
                        elif (4 not in grid) and (7 not in grid): # turn left 
                            self.isPerfect = 0
                            print("我在卡你13")
                            self.isLeft = True
                            return ["MOVE_LEFT"]    
                        elif (6 not in grid) and (9 not in grid): # turn right
                            self.isPerfect = 0
                            print("我在卡你14")
                            self.isLeft = False
                            return ["MOVE_RIGHT"]
                    elif(self.isLeft == False):
                        if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            self.isPerfect = 0
                            print("我在卡你15")
                            self.isLeft = False
                            return ["SPEED", "MOVE_RIGHT"]
                        elif (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                            self.isPerfect = 0
                            print("我在卡你16")
                            self.isLeft = True
                            return ["SPEED", "MOVE_LEFT"]
                        if (1 in grid) and (3 in grid) and (4 not in grid) and (6 not in grid): #perfect
                            if(13 not in grid) and (14 not in grid):
                                self.isPerfect = 2
                                print("perfect right without 5")
                                self.isLeft = False
                                return ["SPEED", "MOVE_RIGHT"]
                            elif(10 not in grid) and (11 not in grid): 
                                self.isPerfect = 1
                                print("perfect left without 5")
                                self.isLeft = True
                                return ["SPEED", "MOVE_LEFT"]

                        if (3 not in grid) and (6 not in grid): # turn right
                            self.isPerfect = 0
                            print("我在卡你17")
                            self.isLeft = False
                            return ["SPEED", "MOVE_RIGHT"]
                        elif (1 not in grid) and (4 not in grid): # turn left 
                            self.isPerfect = 0
                            print("我在卡你18")
                            self.isLeft = True
                            return ["SPEED", "MOVE_LEFT"]
                        elif (6 not in grid) and (9 not in grid): # turn right
                            self.isPerfect = 0
                            print("我在卡你19")
                            self.isLeft = False
                            return ["MOVE_RIGHT"]
                        elif (4 not in grid) and (7 not in grid): # turn left 
                            self.isPerfect = 0
                            print("我在卡你20")
                            self.isLeft = True
                            return ["MOVE_LEFT"]   
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass
