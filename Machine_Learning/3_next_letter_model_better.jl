# In this model we will solve the problem faced with the result of the last model
# In the last model we could not determine the order of the predicted words

# In this model we use a better encoding method
# We will embedding the word in a vector space


using CSV  # to read data
using DataFrames
import Flux as Flux

df_train = CSV.read("3_dataset.csv", DataFrame)
# This is just extracted pairs from moby dick from project gutenberg

vocab = unique(vcat(df_train.Word, df_train.Ans))
# we have stored the all the words in vocab

word_to_idx = Dict(w => i for (i, w) in enumerate(vocab))

vocab_size = length(vocab)
embed_dim = 4   # use a vector of 4 dimensions

println("Loaded Dataset")


E=Flux.Embedding(vocab_size => embed_dim; init=Flux.randn32) # This is a built in Flux.jl Table 
# https://fluxml.ai/Flux.jl/stable/reference/models/layers/#Flux.EmbeddingBag

# EmbeddingBag(in => out, reduction=mean; init=Flux.randn32)
# A lookup table that stores embeddings of dimension out for a vocabulary of size in.

# initially each word vector is assigned a random value which will be tuned using Flux.jl

word_to_index = Dict(word => i for (i, word) in enumerate(vocab))


model = Flux.Chain(
    E,
    Flux.Dense(embed_dim => 16, tanh),
    Flux.Dense(16 => vocab_size)
)

loss(m, x, y) = Flux.logitcrossentropy(m(x), y)
# this loss function is used specifically for words
# https://fluxml.ai/Flux.jl/stable/reference/models/losses/#Flux.Losses.logitcrossentropy


opt_state = Flux.setup(Flux.Adam(0.01), model)

data = Tuple{Int,Flux.OneHotVector}[]
for (i, j) in zip(df_train.Word, df_train.Ans)
    x_index = word_to_index[i]
    y_onehot = Flux.onehot(word_to_index[j], 1:vocab_size)
    push!(data, (x_index, y_onehot))
end


# Onehot vector means 
# vectors where only one element is 1 and all others are 0 this is the input required by loss function

println("Encoded Dataset")

for i in 1:1000 # training loop
    println(i)
    Flux.train!(loss, model, data, opt_state)
    if i % 100 == 0
        x = word_to_index["are"]                              # e.g. 3  (a single Int)
        y = Flux.onehot(word_to_index["you"], 1:vocab_size)   # e.g. [0,0,0,0,0,0,0,0,0,0,0,0,1,0,...,0]
        println("Epoch $i | loss: $(loss(model,x,y))")

    end
end


while true
    print("Enter a word: ")
    word = readline()

    if !haskey(word_to_index, word)
        println("Word not in vocabulary, try another.")
        continue
    end

    x = word_to_index[word]
    scores = model(x)              # vocab_size-length raw logits
    pred_idx = argmax(scores)      # index of highest score
    pred_word = vocab[pred_idx]    # look up the actual word

    println("Predicted next word: ", pred_word)
end

#-----------------------------------
# Drawbacks
# can only predict words for input in the small dictionary
# SLOW :(
