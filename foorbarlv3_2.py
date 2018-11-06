import functools
def answer(food, grid):
    # your code here
    x = 0
    mem = [[[-10 for i in range(20)] for j in range(20)] for k in range(200)]
    def traverse(food, x, y):      
        if(x == len(grid) or y == len(grid[0]) or food < 0):
            return -1
        if(mem[food][x][y] > -10):
            return mem[food][x][y]
        #x += 1
        #print(x)
        ration = food - grid[x][y]
        if ration < 0 :
            return -1
        elif(len(grid) - 1 == x and len(grid) - 1 == y):
            return ration
        else:
            right = traverse(ration,  x + 1, y)
            down = traverse(ration,  x, y+1)
            if right < 0:
                ration = down
            elif down < 0:
                ration  = right
            else:
                ration = down if down < right else right
                
        mem[food][x][y] = ration
        return ration
        
    return traverse(food, 0,0)

print(answer(25, [[0, 2, 5, 2], [1, 1, 3, 3], [2, 1, 1,7], [2, 1, 4,7]]))
    
         