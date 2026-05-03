using Plots
gr()

function heiles_potential(x, y)
    return 0.5 * (x^2 + y^2) + x^2 * y - y^3 / 3
end

function Fx(x, y)
    return -(x + 2 * x * y)
end

function Fy(x, y)
    return -(y + x^2 - y^2)
end

function generate(x0, y0, px0, py0, N, delta_t)
    px = [px0]
    py = [py0]
    x = [x0]
    y = [y0]
    steps = 0
    # Implementing Stormer Verlet Algorithm (a standard for hamiltonian systems)
    while (steps != N)

        p_halfy = py[end] + delta_t / 2 * Fy(x[end], y[end]) # Half Step momentum
        ynew = y[end] + delta_t * p_halfy

        p_halfx = px[end] + delta_t / 2 * Fx(x[end], y[end])
        xnew = x[end] + delta_t * p_halfx

        pxnew = p_halfx + delta_t / 2 * Fx(xnew, ynew)
        pynew = p_halfy + delta_t / 2 * Fy(xnew, ynew)

        push!(px, pxnew)
        push!(x, xnew)
        push!(py, pynew)
        push!(y, ynew)
        steps += 1
    end

    # Masking for making Poincare Sections
    
    mask = (y[1:end-1] .< 0) .& (y[2:end] .> 0) .& (py[2:end] .> 0)
    x_m = x[1:end-1]
    px_m = px[1:end-1]

    return x_m[mask], px_m[mask]
end

function run_energy(E, N, dt)

    p = scatter(title="E = $E", xlabel="x", ylabel="px",
        legend=false, markersize=1, markerstrokewidth=0)

    for x0 in range(-0.4, 0.4, length=10)
        rem = E - heiles_potential(x0, 0.0) # KE
        rem <= 0 && continue
        py0 = sqrt(2 * rem)
        sx, spx = generate(x0, 0.0, 0.0, py0, N, dt)
        scatter!(p, sx, spx, markersize=1, markerstrokewidth=0)
    end

    return p
end

N = 200_000
dt = 0.01

p1 = run_energy(0.08, N, dt)
p2 = run_energy(0.12, N, dt)
p3 = run_energy(0.167, N, dt)

fig = plot(p1, p2, p3, layout=(1, 3), size=(1400, 500), plot_title="Henon-Heiles Poincare Sections")

display(fig)
readline()