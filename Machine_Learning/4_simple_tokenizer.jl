# In Part 3 We faced the following problems:
# Slow processing
# Fixed vocab
# No handling of typos
# (Design Choice) One word output

# To move to a reasonable sentence model we would need to fix all of these
# Here is the most simple version of the most commonly used method to solve the slow processing and fixed vocab problem

# Byte-Pair Encoding (BPE) or Tokenization
# It works by starting with individual characters, finding the most frequently occurring adjacent pairs,
# and merging them into new tokens until a desired vocabulary size is reached

# ---------Advantage--------------
# if you misspelled a word for eg.
# direction is misspelled as diruction
# then the algorithm will recognize this word as not in the dictionary and try to break it down into tokens for eg.
# It gets broken down into "dir","uc","tion" now assuming "dir" and "tion" are already in the dictionary some of the 
# context of the misspelled word somewhat extracted and can be used to predict the output

using CSV
using DataFrames
import Flux as Flux

df_train=CSV.read("3_dataset.csv", DataFrame)

vocab = unique(vcat(df_train.Word, df_train.Ans))

tokens=Dict{String,Int}()

threshold_freq=20 # if a pair of letter appear frequently enough merge them into one token

vocab_itimized=[] # convert word to ["w","o","r","d"]
for word in vocab
    letter_list = split(word, "")
    push!(vocab_itimized, letter_list)
end

for word in vocab_itimized
    for token in word
        if haskey(tokens, token) == false
            tokens[token]=1
        else
            tokens[token]+=1
        end
    end
end


function tokenizer(word)
    """Convert words into token by combining common pairs"""
    i = 1
    while i <= length(word) - 1
        token = word[i] * word[i+1]
        
        if haskey(tokens, token) == false
            tokens[token] = 1
        else
            tokens[token] += 1
        end
        
        if tokens[token] > threshold_freq
            for _word_ in vocab_itimized
                k = 1
                while k <= length(_word_) - 1
                    if _word_[k] * _word_[k+1] == token
                        _word_[k] = token
                        deleteat!(_word_, k+1)
                    end
                    k += 1
                end
            end
        end
        i += 1
    end
end

# this is not the eact BPE algorithm merger, In the orignal there is no threshold_freq the algorithm 
# just merges the most common pair
# this is just a design Choice (a poor one)

for i in 1:10 # run this an arbitarty number of times, each time it will lead to bigger tokens
    for word in vocab_itimized
        tokenizer(word)
    end
end



# Now here either we can use the old flux.chain by taking avg of all the vector of the input tokens
# then the ouput would be a single word and similar to what we have already done

# model = Flux.Chain(
#     E,
#     Flux.Dense(embed_dim => 16, tanh),
#     Flux.Dense(16 => vocab_size)
#     )


