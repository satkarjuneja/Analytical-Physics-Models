# --------- Set UP ----------

n=10000 # Cardinality of set U
N = 1000 # Cardinality of Set V
using Random
U=Set(1:n)

V=Set() # Set of subsets of u
for i = 1:N
    random_subset = Set(randsubseq(collect(U), 0.5))
    push!(V, random_subset)
end
print(V)

# ------ QUBO ------
function build_qubo(V, P = 2.0)
    V_list = collect(V)
    n = length(V_list)
    Q = zeros(n, n)

    # objective: maximize count → diagonal = -1
    for i = 1:n
        Q[i, i] = -1.0
    end

    # constraint: penalize overlapping pairs
    for i = 1:n
        for j = (i+1):n
            if !isempty(intersect(V_list[i], V_list[j]))
                Q[i, j] += P
                Q[j, i] += P  # symmetric
            end
        end
    end

    return Q, V_list
end

using PythonCall   # or PyCall, PythonCall is the modern recommended one

dimod = pyimport("dimod")
dwave_system = pyimport("dwave.system")

# Q is your Julia matrix from build_qubo
n = size(Q, 1)
Q_dict = Dict((i-1, j-1) => Q[i, j] for i = 1:n, j = 1:n if Q[i, j] != 0)
# note: i-1, j-1 since D-Wave/Python is 0-indexed, Julia is 1-indexed

bqm = dimod.BinaryQuadraticModel.from_qubo(pydict(Q_dict))

sampler = dwave_system.EmbeddingComposite(dwave_system.DWaveSampler())
result = sampler.sample(bqm, num_reads = 100)

println(result)
