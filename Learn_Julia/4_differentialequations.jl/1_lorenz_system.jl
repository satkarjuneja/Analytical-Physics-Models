# Lorenz System
# The Lorenz system is a set of three ordinary differential equations,
# first developed by the meteorologist Edward Lorenz while studying
# atmospheric convection. It is a classic example of a system that can
# exhibit chaotic behavior, meaning its output can be highly sensitive to small
# changes in its starting conditions.

# Checkout https://en.wikipedia.org/wiki/Lorenz_system

#Edward Lorenz was attempting to model the way air moves when heated from below and cooled from above. 
#The model describes how three key properties of this system change over time:
#    x is proportional to the intensity of the convection (the rate of fluid flow).
#    y is proportional to the temperature difference between the rising and falling air currents.
#    z is proportional to the distortion of the vertical temperature profile from a linear one.

# or more precisely
# dx/dt = σ(y-x)
# dy/dt = x(ρ-z)-y
# dz/dt = xy-β(z)

#The constants σ, ρ, and β are parameters representing physical properties of the system:
# σ is the Prandtl number, ρ is the Rayleigh number, and β relates to the physical dimensions
# of the fluid layer itself

using DifferentialEquations
using Plots

function lorenz!(du, u, p, t) #these have to be passed in this exact order 
    σ, ρ, β = p
    du[1] = σ * (u[2] - u[1])        # dx/dt
    du[2] = u[1] * (ρ - u[3]) - u[2] # dy/dt
    du[3] = u[1] * u[2] - β * u[3]   # dz/dt
end

u0 = [1.0, 0.0, 0.0]          # initial conditions [x, y, z]
p = (10.0, 28.0, 8/3)   # σ, ρ, β (Lorenz's original values)
tspan = (0.0, 50.0)   # time period to run the simulation for 


prob = ODEProblem(lorenz!, u0, tspan, p)
sol = solve(prob, Tsit5()) # choose your algorithm and pass the problem

#Tsit5 is a 4th/5th order explicit Runge-Kutta method with adaptive step size. 
#The "5" is the order. It's the default recommendation in DifferentialEquations.jl
# for non-stiff ODE systems because it's more efficient than the classical 
# RK4 it uses an embedded error estimate to automatically shrink or grow the step
# size based on how fast the solution is changing.

display(plot(sol, idxs = (1, 2, 3))) # 3D phase portrait, x vs y vs z
xlabel!("x")
ylabel!("y")
zlabel!("z")
readline()
