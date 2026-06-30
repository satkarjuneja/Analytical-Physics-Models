# Lets train a NN to solve a simple ODE uwing Flux.jl (ML library of Julia)
# Lets start with a simple pendulum
# d^2/dt^2(θ)+ Lg​sin(θ)=0

# g denoting acceleration due to gravity
# L denoting length of string
# θ denoting angle of string with normal
# ω denoting angular velocity

using DifferentialEquations

# Setup classical solver
const g=9.81
L=1

# Initial conditions
u=[0,pi/2] #   θ, ω
tspan=(0,1)

function pendulum(du,u,p,t)
    θ, ω=u
    du[1]=ω
    du[2] = -(g / L) * sin(θ)
end

prob = ODEProblem(pendulum, u, tspan)
sol = solve(prob, Tsit5())

import Flux as Flux

x_train = rand(length(sol.t))
y_train = sol.(x_train)

x_test = rand(length(sol.t))
y_test = sol.(x_test)

# y_train is currently a vector of [θ, ω] vectors. Flux wants a matrix where columns are samples

X_train = Float32.(reshape(x_train, 1, :))        # (1, N)
Y_train = Float32.(hcat(y_train...))              # (2, N)

X_test = Float32.(reshape(x_test, 1, :))
Y_test = Float32.(hcat(y_test...))


# model defination
model = Flux.Chain(
    Flux.Dense(1 => 32, tanh),
    Flux.Dense(32 => 32, tanh),
    Flux.Dense(32 => 2)              # outputs [θ, ω]
)

loss(m, x, y) = Flux.mse(m(x), y) #function can be defined this way
data = [(X_train, Y_train)]

opt_state = Flux.setup(Flux.Adam(0.01), model) # Adam: Adamtive Moment Estimation

for i in 1:1000
    Flux.train!(loss, model, data, opt_state)
    if i % 100 == 0
        println("Epoch $i | loss: $(loss(model, X_train, Y_train))")
    end
end

preds = model(X_test)
println("Test loss: ", loss(model, X_test, Y_test))