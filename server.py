import os
import random
import sys
import collections
import cherrypy
import math
import json
"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""
class Cell:
  def __init__(self, dist = sys.maxsize, visited= False, parent= None):
    self.dist = dist
    self.parent = parent 
    self.visited = visited

  def reset(self):
    self.dist = sys.maxsize
    self.parent = None 
    self.visited = False 



class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "Prakort",  # TODO: Your Battlesnake Username
            
            "color": "#3E338F",
            "head": "beluga",
            "tail": "curled"
          
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
              
        def findDirection(head, move):
            move = list(move)
            print('head----->', head,'target----->', move)
            if head[0] == move[0]:
                if head[1] == move[1] - 1: 
                    return 'right'
                elif head[1] == move[1] + 1:
                    return 'left'
            elif head[1] == move[1]:
                if head[0] - 1 == move[0]:
                    return 'up'
                else:
                    return 'down' 
        # loop to find food
        def getAllPath(height, width, start, ob, foods):
            paths = {}
            next_move = 'up'
            chosen = []
            for food in foods:
                # print('food', food)
                path = bfs( height, width, start, ob, tuple(food))
                if path:
                    paths[tuple(food)] = path 
                    if not chosen or len(path) < len(chosen):
                        chosen = path

            # print('chosen', chosen[1])
            next_move = findDirection(start, chosen[1])
            # print('next move', next_move)
            return chosen, chosen[1], next_move
          
          

        # @param grid: List[List] table
        # @param start: List[] head coordinate
        # @param ob: List[List obstical such as snakes body and other snakes coord
        # @param foods: List[List] list of target food
        def bfs(height, width, start, ob, food):
            queue = collections.deque([[start]])
            seen = set([start])
            # print('new target', food)
            while queue:
                path = queue.popleft()
                row, col= path[-1]
                if (row,col) == food:
                    return path
                for row2, col2 in ((row+1,col), (row-1,col), (row,col+1), (row,col-1)):
                    if 0 <= row2 < height and 0 <= col2 < width and (row2,col2) not in ob and (row2, col2) not in seen:
                      # print('x2',row2,'y2',col2)
                        queue.append(path + [(row2, col2)])
                        seen.add((row2, col2))

        # Goal: find the shortest food coordinate
        # @param foods: List[List]
        # @param head: List[int]
        def findNearestFood(foods, head):
            def distance(x1, y1, x2, y2):
                return math.sqrt((x1-x2)**2 + (y1-y2)**2)
            
            nearest = foods[0]
            dist = distance(nearest[0], nearest[1],head[0],head[1])
            for pair in foods:
                temp = distance(pair[0],pair[1],head[0],head[1])
                if dist > temp:
                    nearest = pair
            
            return nearest
          






        data = cherrypy.request.json
       
        print('data', data)
        board = data["board"]
        game = data["game"]
        # print("board gamessss", data) 
        height = data["board"]["height"]
        width = data["board"]["width"]
       
        # head coordination
        head =tuple([height - 1 - data["you"]["head"]["y"], data["you"]["head"]["x"] ])

        snakes = data["board"]["snakes"]
        
        # obstical
        obstical = set()
        for body in snakes:
          pairs = body["body"]
          for pair in pairs:
            obstical.add((height - 1 - pair["y"],pair["x"]))
          
      
        # get all the foods coordinate
        foods = list([ height - 1 - x["y"] , x["x"]   ] for x in board["food"])


        c ,paths, next_move = getAllPath(height, width, head, obstical, foods)
        print('\n---chosen path-----',c)
        print('\n---chosen move-----',paths)
        print("\n--------head------", head)
        print("\nfood", foods)
        print('\n------next-move-----', next_move)

        # Choose a random direction to move in
        # possible_moves = ["up", "down", "left", "right"]
        # move = random.choice(possible_moves)

        print(f"MOVE: {next_move}")
        return {"move": next_move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
