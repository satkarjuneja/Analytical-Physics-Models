# one of the most simple QUBO formulations
# the problem is as follows:

# Given an undirected graph G(V, E) with a vertex set V and an edge set E, the Max Cut problem seeks to
# partition V into two sets such that the number of edges between the two sets (considered to be
# severed by the cut), is a large as possible.

function bit_strings(n)
    arr = []

    for i = 0:(2^n-1)
        s = digits(i, base = 2, pad = n) # convert number to bit string
        push!(arr, s)
    end

    return arr
end

n = parse(Int, readline())
e = parse(Int, readline())

edges = Tuple{Int,Int}[]

for _ = 1:e
    a, b = parse.(Int, split(readline()))
    push!(edges, (a, b))
end

bits = bit_strings(n)

sol = 0

for b in bits

    count = 0

    for (u, v) in edges
        count += xor(b[u], b[v])
    end

    global sol = max(sol, count)
end

println(sol)
