# Boids is an artificial life algorithm, 
# developed by Craig Reynolds in 1986, which simulates the flocking behaviour of birds

# The rules applied in the simplest Boids world are as follows:
#   separation: steer to avoid crowding local flockmates
#   alignment: steer towards the average heading of local flockmates
#   cohesion: steer to move towards the average position (center of mass) of local flockmates

using Plots
using Statistics

LENGTH=5000

mutable struct Bird # structs by default in julia are immutable
    x::Float64
    y::Float64
    speed::Float64
    angle::Float64
end

Bird() = Bird(rand(0:2000), rand(0:2000), 1000, rand()*(pi*2))

function separation!(b::Bird, flock::Vector{Bird})
    for other in flock
        other === b && continue
        dx = b.x - other.x
        dy = b.y - other.y
        dist = sqrt(dx^2 + dy^2) # ^ is for power xor() is used for xor in julia
        if dist < 15 && dist > 0
            b.angle += pi/4
        end
    end
end


function alignment!(flock::Vector{Bird}) # ! means inplace change of values
    for b in flock
        neighbours=Bird[] # type declaration
        for other in flock
            other === b && continue
            dx = b.x - other.x
            dy = b.y - other.y
            dist = sqrt(dx^2 + dy^2)
            if dist < 250 && dist > 0
                push!(neighbours,other)
            end
        end
        if !isempty(neighbours)
            avg = mean(o.angle for o in neighbours)
            b.angle += 0.05 * (avg - b.angle)
        end
    end
end

function cohesion!(flock::Vector{Bird})
    # assuming mass of each bird to be one and calculating center of mass
    for b in flock
        neighbours=Bird[]
        for other in flock
            other === b && continue
            dx = b.x - other.x
            dy = b.y - other.y
            dist = sqrt(dx^2 + dy^2)
            if dist < 250 && dist > 0
                push!(neighbours,other)
            end
        end
        if !isempty(neighbours)
            x_cm = mean(o.x for o in neighbours)
            y_cm=mean(o.y for o in neighbours)
            b.angle += 0.01 * (atan((b.y-y_cm), (b.x-x_cm)) - b.angle) # cos,sin,acos,etc are native in julia
        end
    end

end

dt=0.02

function move!(flock)
    for b in flock
        b.x = (b.x + dt*b.speed*cos(b.angle))%LENGTH # Periodic boundaries
        b.y = (b.y + dt*b.speed*sin(b.angle))%LENGTH
        if(b.x<0)
            b.x=LENGTH-b.x
        end
        if(b.y<0)
            b.y=LENGTH-b.y
        end
    end
end


flock=[Bird() for i = 1:100] # make a flock of 100 birds

anim = @animate for t = 1:500

    cohesion!(flock)
    alignment!(flock)
    for b in flock
        separation!(b, flock)
    end 
    move!(flock)
    quiver( # for making arrows
    [b.x for b in flock],
    [b.y for b in flock],
    quiver = ([cos(b.angle)*30 for b in flock], [sin(b.angle)*30 for b in flock]),
    legend = false,
    xlims = (0, 5000), ylims = (0, 5000),
    aspect_ratio = :equal,
    arrow = true,
    linewidth = 2,
    size = (1200, 1200),
    title = "Boids t=$t",
    )
end
