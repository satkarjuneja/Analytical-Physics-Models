# Conways game of life is a zero players game which runs on a 2D grid Here are the rules:
#1. A live cell with fewer than 2 live neighbours dies: underpopulation
#2. A live cell with 2 or 3 live neighbours survives
#3. A live cell with more than 3 live neighbours dies: overpopulation
#4. A dead cell with exactly 3 live neighbours becomes alive: reproduction
# Periodic boundaries so patterns can travel forever
using Plots
print("Enter Size: ")
N = parse(Int64, readline())
print("Enter Steps: ")
steps = parse(Int64, readline())
gr() # for plotting GR is highperformance plotting backend in Julia
row = [0, 0, 1, 1, 1, -1, -1, -1]
col = [1, -1, 1, -1, 0, 1, -1, 0]

grid = rand(Bool, N, N)  # random 2d array
dummy = deepcopy(grid)

anim = @animate for p in 1:steps # instead of plotting everything again julia has a builint setup
    heatmap(grid,
        color=:binary,
        aspect_ratio=1,
        axis=false,
        legend=false,
        title="Generation $p")

    for i in 1:N
        for j in 1:N
            count = 0
            for k in 1:8 #inclusive
                if (dummy[mod1(i + row[k], N), mod1(j + col[k], N)])
                    count += 1
                end
            end

            if (count < 2)
                grid[i, j] = 0

            elseif (count > 3)
                grid[i, j] = 0

            elseif (count == 3)
                grid[i, j] = 1
            end

        end
    end
    dummy .= grid # normal dummy will just reference it like python
end


print(grid)