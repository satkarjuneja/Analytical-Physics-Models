# Model:
# Initial: a 2D sheet of metal plate with one hot spot in the middle, modelled as a grid of cells
# Each step every cell's temperature depends on its own temperature and its 4 neigbours

# Using GPU every cell can be updated at the same time :)


using oneAPI, KernelAbstractions

@kernel function step!(unew, @Const(u), @Const(α))
    i, j = @index(Global, NTuple) # tell the GPU to give each instance a index

    if i > 1 && i < size(u, 1) && j > 1 && j < size(u, 2)
        unew[i, j] = u[i, j] + α * (u[i+1, j] + u[i-1, j] +u[i, j+1] + u[i, j-1] - 4 * u[i, j])
    end
end

# Integerated graphics support Float32 not Float64
function simulate(n, steps)

    u_cpu = zeros(Float32, n, n) # for comparision
    u_cpu[n÷2, n÷2]=100f0
    u=oneArray(u_cpu)
    unew=copy(u)
    backend=get_backend(u)
    α=0.2f0

    for _ in 1:steps
        step!(backend)(unew, u, α, ndrange = size(u))
        u, unew = unew, u
    end
    KernelAbstractions.synchronize(backend)

    return Array(u)

end


simulate(64, 5)   # warm-up, so compile time isn't counted

for n in (512, 1024, 2048,10000)
    t = @elapsed simulate(n, 500)
    println("n = $n: ", round(t, digits = 3), " s")
end