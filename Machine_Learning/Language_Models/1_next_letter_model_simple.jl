# Letter build a Neural Network which give any 2 letters will try to predict the next letter 
# eg- INPUT: 'by'
# OUTPUT: 'e' ->'bye'

# we will do this with a simple linear model for now
# y=Wx+b
# dimension of y,b will be (26,1) cause there are 26 letters in the english alphabet
# dimension of x will be (52,1) cause there are 2 letters (26*2)
# dimension of W will be (26,52) can be seen with basic Matrix Multiplication Compatebility rules


W = rand(26, 52) # start 
b = rand(26)


function NN(x)
    return W * x + b
end

function backpropagate(first_letter, second_letter, y_pred, y_true, alpha)

    if (y_pred==Int(y_true))
        return # if prediction is correct do nothing
    end

    y_true = Int(y_true[1]) - 96 # convert to index form

    W[y_pred, first_letter] -= alpha
    W[y_true, first_letter] += alpha

    W[y_pred, second_letter] -= alpha
    W[y_true, second_letter] += alpha


end

function predict()
    while (true)
        println("INPUT")
        input=readline()
        first_letter=input[1]
        second_letter=input[2]

        first_letter = Int(first_letter) - 96
        second_letter = Int(second_letter) - 96

        x=zeros(52)
        x[first_letter]=1
        x[second_letter+26]=1

        y=NN(x)
        println(y)
        output=argmax(y)
        println("Prediction")
        println(Char(output+96))

        print("Expected Output: ")
        y_true=readline()
        backpropagate(first_letter, second_letter+26, output, y_true, 0.5)
    end
end

predict()
