# Lets make simple RL model for tictactoe
# This will be a NN based model

# --------------Idea--------------
# Take 9 dim vector of current state
# take all possible legal move vectors and put them through the NN
# pick the move with the highest score

using Serialization # built in package to store parameters could also be stored in a plain txt

hidden_dim = 9

function save_params(path="params.jls")
    serialize(path, (W1, b1, W2, b2))
end

W1=rand(hidden_dim, 9) .- 0.5
b1=rand(hidden_dim) .- 0.5
W2=rand(1, hidden_dim) .- 0.5
b2=rand(1) .- 0.5

# save_params() 
#uncomment if running for the first time

function load_params(path="params.jls")
    global W1, b1, W2, b2
    if isfile(path)
        W1, b1, W2, b2 = deserialize(path)
    end
end

load_params() # comment if running for the first time

learning_rate=0.2
epsilon=0.2

function NN(x)
    h = tanh.(W1 * x .+ b1)
    y = tanh(first(W2 * h .+ b2))
    return y, h
end

function print_game(state)
    for i in 1:9
        print(state[i])
        print("  ")
        if (i%3==0)
            println()
        end
    end

end

function all_legal_moves(state)
    legal=[]
    for i in 1:9
        if (state[i]==-1)
            push!(legal, i)
        end
    end
    return legal
end

function is_game_over(state)
    lines = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9),   # rows
        (1, 4, 7), (2, 5, 8), (3, 6, 9),   # cols
        (1, 5, 9), (3, 5, 7)             # diagonals
    ]

    for (a, b, c) in lines
        if state[a] != -1 && state[a] == state[b] && state[b] == state[c]
            if state[a] == 1
                return 0   # player X won
            else
                return 1   # computer O won
            end
        end
    end

    if !any(x -> x == -1, state)
        return 2  # draw, board is full
    end

    return -1  # not over
end


function backprop(y, y_pred, h, x)
    global W1, b1, W2, b2
    # loss=(y-y_pred)^2
    delta2 = -2 * (y - y_pred) * (1 - y_pred^2)
    dW2 = delta2 .* reshape(h, 1, hidden_dim)
    db2 = delta2

    dh = vec(W2) .* delta2
    delta1 = dh .* (1 .- h .^ 2)

    dW1 = delta1 * reshape(x, 1, 9)
    db1 = delta1

    W1 = W1 - learning_rate * dW1
    b1 = b1 .- learning_rate * db1
    W2 = W2 - learning_rate * dW2
    b2 = b2 .- learning_rate * db2
    save_params()
end

function play_or_train(play, state)
    if (play==0)
        moves=all_legal_moves(state)
        return rand(moves)
    end
    if (play==1)
        println("Your Turn")
        X=readline()
        X=parse(Int, X)
        return X
    end
end

function game(play)
    state=fill('_', 9)
    NN_state=fill(-1, 9)
    print_game(state)

    while (true) # Game Loop
        X=play_or_train(play, NN_state)
        state[X]='X'
        NN_state[X]=1
        moves=all_legal_moves(NN_state)
        score=[]
        hiddens=[]

        for i in moves
            nn_state=copy(NN_state)
            nn_state[i]=0
            x, h=NN(nn_state)
            push!(score, x)
            push!(hiddens, h)
        end

        if (score==[]) # premature draw from player side
            println("Game is a Draw")
            break
        end

        if (rand() < epsilon) # for exploration
            move=rand(1:length(moves))
        else
            move=argmax(score)
        end

        nn_x=score[move]
        nn_h=hiddens[move]

        state[moves[move]]='O'
        NN_state[moves[move]]=0

        y=is_game_over(NN_state)

        if (y==2)
            println("Game is a Draw")
            backprop(2, nn_x, nn_h, NN_state)
            break
        elseif (y==1)
            println("Computer Won")
            backprop(1, nn_x, nn_h, NN_state)
            break
        elseif (y==0)
            println("You Won")
            backprop(0, nn_x, nn_h, NN_state)
            break
        end

        print_game(state)
    end



end

for i in 1:100000
    # put in zero if you want to train and 1 if you want to play
    game(1)
end