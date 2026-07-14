# Lets train a slightly better model which will try to predict the next word 
# we will use the julia library Flux.jl this time for our backprogagation

# Here is the procedure we will try to follow:
# 1. Convert the input into a tangible form for our NN
# 2. Train it on data
# 3. Look at the letter frequencies and judge the output



using CSV  # to read data
using DataFrames
import Flux as Flux

df_train = CSV.read("2_dataset_train.csv", DataFrame)
df_test=CSV.read("2_dataset_test.csv", DataFrame)

# Convert word into a numeric form 
# Here for each word we are assigning a 26 length vector which will have the frequencies of all the characters in the word

X_train=[]
for word in df_train.Word
    w=zeros(Float32, 26)
    word=lowercase(word)
    for letter in word
        w[Int(letter)-Int('a')+1]+=1
    end
    push!(X_train, w)
end
# same for the output
Y_train=[]
for word in df_train.Ans
    w=zeros(Float32, 26)
    word=lowercase(word)
    for letter in word
        w[Int(letter)-Int('a')+1]+=1
    end
    push!(Y_train, w)
end


X_test=[]
for word in df_test.Word
    w=zeros(Float32, 26)
    word=lowercase(word)
    for letter in word
        w[Int(letter)-Int('a')+1]+=1
    end
    push!(X_test, w)
end
# same for the output
Y_test=[]
for word in df_test.Ans
    w=zeros(Float32, 26)
    word=lowercase(word)
    for letter in word
        w[Int(letter)-Int('a')+1]+=1
    end
    push!(Y_test, w)
end

#convert them into matrix form cause thats how Flux.jl expects input

X_train = hcat(X_train...)   # 26 × 300 matrix
Y_train = hcat(Y_train...)   # 26 × 300 matrix

X_test = hcat(X_test...)     # 26 × 100 matrix
Y_test = hcat(Y_test...)     # 26 × 100 matrix

model = Flux.Chain(
    Flux.Dense(26 => 128, tanh),
    Flux.Dense(128 => 128, tanh),
    Flux.Dense(128 => 26)
)

loss(m, x, y) = Flux.mse(m(x), y) # loss function  

data = [(X_train, Y_train)]

opt_state = Flux.setup(Flux.Adam(0.01), model) # Adam: Adamtive Moment Estimation

for i in 1:length(X_train) # training loop
    Flux.train!(loss, model, data, opt_state)
    if i % 100 == 0
        println("Epoch $i | loss: $(loss(model, X_train, Y_train))")
    end
end

preds = model(X_test)
println("Test loss: ", loss(model, X_test, Y_test))

#------------------

alphabet = Dict(1=>'a', 2=>'b', 3=>'c', 4=>'d', 5=>'e', 6=>'f', 7=>'g', 8=>'h',
    9=>'i', 10=>'j', 11=>'k', 12=>'l', 13=>'m', 14=>'n', 15=>'o',
    16=>'p', 17=>'q', 18=>'r', 19=>'s', 20=>'t', 21=>'u', 22=>'v',
    23=>'w', 24=>'x', 25=>'y', 26=>'z')

# Now after training lets take a word as input and see the prediction
while (true)
    print("Enter a word: ")

    w=readline()

    # encode it
    arr=zeros(Float32, 26)
    w=lowercase(w)
    for letter in w
        arr[Int(letter)-Int('a')+1]+=1
    end

    # give it to the model
    ans=model(arr)

    # Now since we have set this up in a very rudementory way
    # we can only determine the letters used not the order in which they are predicted

    alpha_word = ""
    for i in 1:length(ans)
        if ans[i] > 0.5
            alpha_word *= alphabet[i]
        end
    end
    println(alpha_word)


    #This will be print predicted letters alphabetically
end
