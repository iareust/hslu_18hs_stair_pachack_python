import bottle
import os
import numpy as np
from heapq import heappop, heappush
from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer
from app.dto.ReturnDirections import ReturnDirections


class Counter:
    count = 0


alreadyVisited = np.zeros(1)
player = 1

@bottle.post('/start')
def start():
    return "BlauesTeam"


@bottle.post('/chooseAction')
def move():
    Counter.count+=1
    print (Counter.count)
    data = PublicGameState(ext_dict=bottle.request.json)
    playground = np.copy(data.gameField)
    playground[playground != '%'] = 0
    playground[playground == '%'] = 1
    playground = np.array(playground).astype(bool)

    foodOnMap = np.copy(data.gameField)
    foodOnMap[foodOnMap != '°'] = 0
    foodOnMap[foodOnMap == '°'] = 1
    foodOnMap.astype(int)

    shape = foodOnMap.shape
    y = shape[0]
    x = int(shape[1] / 2)

    if player == 1:
        foodOnMap[:, x:] = 0
    else:
        foodOnMap[:, :x] = 0

    done = False
    for i in range(0, foodOnMap.shape[0]):
        for j in range(0, foodOnMap.shape[1]):
            if foodOnMap[i, j] == '1':
                done = True
                break
        if done:
            break

    playerPos = data.publicPlayers[player]['position']
    playerPos = (int(playerPos[1]), int(playerPos[0]))
    goto = (i, j)

    if (Counter.count > 200) and (Counter.count < 300):
        goto = (15, 32)


    # print (" Point on Map", foodOnMap[goto[0], goto[1]])


    pathStr = find_path_astar(playground, playerPos, goto)
    action = pathStr.split(";")[0]

    if action == "N":
        #print("Action N")
        return ReturnDirections.NORTH
    elif action == "S":
        #print ("Action S")
        return ReturnDirections.SOUTH
    elif action == "W":
        #print("Action W")
        return ReturnDirections.WEST
    else:
        #print("Action E")
        return ReturnDirections.EAST


def normalizeMapFromArray(arr: np.ndarray, stringToSetAsOne: str ):
    arr[arr != str] = 0
    arr[arr == str] = 1
    return arr

def maze2graph(maze):
    height = len(maze)
    width = len(maze[0]) if height else 0
    graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j]}
    for row, col in graph.keys():
        if row < height - 1 and not maze[row + 1][col]:
            graph[(row, col)].append(("N;", (row + 1, col)))
            graph[(row + 1, col)].append(("S;", (row, col)))
        if col < width - 1 and not maze[row][col + 1]:
            graph[(row, col)].append(("E;", (row, col + 1)))
            graph[(row, col + 1)].append(("W;", (row, col)))
    return graph

def heuristic(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def find_path_astar(maze, start, goal):
    pr_queue = []
    heappush(pr_queue, (0 + heuristic(start, goal), 0, "", start))
    visited = set()
    graph = maze2graph(maze)
    while pr_queue:
        _, cost, path, current = heappop(pr_queue)
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            heappush(pr_queue, (cost + heuristic(neighbour, goal), cost + 1,
                                path + direction, neighbour))
    return "ERR;"



if __name__ == '__main__':
    application = bottle.default_app()
    bottle.run(application, host=os.getenv('IP', '127.0.0.1'), port=os.getenv('PORT', '8080'))