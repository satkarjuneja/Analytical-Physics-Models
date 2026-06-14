# Lets build our own small neural network(NN)

# a simple NN just consists of composition of functions acting on an input
# lets train a NN to predict the value of sin(x) from [-pi,pi]

# A standard non linear prediction function is
# h=tanh(W1*x .+b1)
# output= W2*h .+b2

# Where W1,W2,b1,b2 are appropiate weight vectors

# Why are they vectors ?
# Well a tanh is basically just an S shaped curve but if you 
# take many such curves and add them together with appropiate 
# weights you can approximate any curve


# then we calculate how far away from the true value this was and calculate the gradient wrt each parameter
# If gradient is positive → decrease the weight 
# If gradient is negative → increase the weight (loss is decreasing)
# this is called back propagation

# and DONE
using Plots
using Distributions

W1 = randn(8, 1) # vector of dim [8,1]
b1 = randn(8)  # array of length 8
W2 = randn(1, 8) #vector of dim[1,8]
b2 = randn(1)

function NN(x)
    h = tanh.(W1 * x .+ b1)
    y = W2 * h .+ b2
    return y
end

function backpropogate(y,y_true, alpha,x) # alpha is the rate of changing the variables (learning rate)
    global W1, b1, W2, b2
    h=tanh.(W1 * x .+ b1)
    # now you can differentiate y the loss function wrt every variable and modify our weights

    dL_dy = 2 * (y .-y_true)

    dL_dW2 = dL_dy * h' # ' is the transpose operator in julia
    W2 = W2 - dL_dW2 * alpha


    dL_db2 = dL_dy
    b2 = b2 - dL_db2 * alpha

    dL_dh = W2' * dL_dy
    dL_dz1 = dL_dh .* (1 .- h .^ 2)

    dL_dW1 = dL_dz1 * x'
    W1 = W1 - dL_dW1 * alpha

    dL_db1 = dL_dz1

    b1 = b1 - dL_db1 * alpha

end

# Training loop
x_plot = range(-pi, pi, length=200)

@animate for i in 1:2000
    x = rand(Uniform(-pi,pi))
    y_true = sin(x)
    y = NN(x)
    loss = (y_true - y[1])^2 #cause of all the array stuff we did y is a Matrix of dim=1*1
    backpropogate(y,y_true,0.01,x)

    y_true_plot = sin.(x_plot)
    y_pred_plot = [NN(i)[1] for i in x_plot]

    plot(x_plot, [y_true_plot, y_pred_plot], label=["sin(x)" "NN(x)"],title="Step $i")
end


readline()


