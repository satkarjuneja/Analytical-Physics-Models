#Checkout the python version if not familier with Logistic Maps
using Plots  # Import Plots

r_samples = range(2, 4, length=2000) #numpy equivalent of linspace

x0 = 0.5 # dynamically typed like python
N = 1000
transient = 500

xs_plot = [] # initialize arrays
rs_plot = Float64[] # can specify type also

step=0
for r in r_samples # iterate through lists
    global step
    x = x0
    print("Step: $step\r")
    flush(stdout)
    for i in 1:N # iterate through a range
        x = r * x * (1 - x)
        if i > transient
            push!(xs_plot, x) # append element to an array
            push!(rs_plot, r)
        end
    end
    step+=1
end

p=scatter(
    rs_plot,
    xs_plot,
    markersize=0.2,
    markerstrokewidth=0,
    color=:black,
    legend=false,
    xlabel="r",
    ylabel="x",
    title="Logistic Map Bifurcation Diagram"
)
display(p) # shows the plot

readline() # the plot closes as soon as the file execution is done so to stop that a readline is generally used