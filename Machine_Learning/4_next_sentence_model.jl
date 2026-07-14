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

df_train=CSV.read("3_dataset.csv",DataFrame)

vocab = unique(vcat(df_train.Word, df_train.Ans))

println(vocab)

