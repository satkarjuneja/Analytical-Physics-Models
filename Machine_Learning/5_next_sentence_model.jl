# Now using a tokenizer as we built in the last script we can try to predict the next sentence
# We are going to build a markov chain bigram model
# Features:
# 1. We have a transition matrix of size (token_count)²
# From each token what is the probablity of getting that particulear token
# 2. Using input tune that matrix
# 3. Bigram means we only consider one word to predict the next word

using CSV
using DataFrames
using StatsBase: sample, Weights

# lets import some tokens from our previous tokenizer (these could be any tokens or full words even)

df_token=CSV.read("5_tokens_dataset.csv", DataFrame)

tokens = df_token.token
idx_to_token = tokens
token_to_idx = Dict(token => i for (i, token) in enumerate(tokens))

n=2797 # number of tokens in csv
Transition_Matrix=zeros(n, n)
α = 0.1 # some arbitrary learning rate

# Now we must break  prompt into tokens 
# If the prompt has words which do not match to any token then they matched to the '<unk>' token

function word_tokenizer(word, tokenized_prompt) # Greedy Prefix algorithm to tokenize a word
    partial_token=""
    last_match=""
    for letter in word # take a letter of a word
        partial_token*=letter # add it to partial token
        matches = filter(:token => ==(partial_token), df_token)

        if nrow(matches) != 0 # if this matches a token in dict keep it in last_match
            last_match=partial_token # if no better match if found after this then add last_match
        elseif (last_match!="") # this is done so that the longest token always gets chosen eg. "lo","low" are both tokens then "low" should be chosen in "lower"
            push!(tokenized_prompt, last_match)
            partial_token=string(letter)
            last_match=""
        end
    end

    if (partial_token==word) && (last_match=="")
        push!(tokenized_prompt, "<unk>")
        return
    end

    if (partial_token==last_match)
        push!(tokenized_prompt, last_match)
    else
        push!(tokenized_prompt, last_match)
        remainder = partial_token[(length(last_match)+1):end]
        word_tokenizer(remainder, tokenized_prompt)
    end
end

df_train=CSV.read("5_train_sentence_dataset.csv", DataFrame)
num=0
for (prompt, ans) in zip(df_train.Input, df_train.Ans)
    # print the iteration
    global num
    if (num%100==0)
        println(num)
    end
    num+=1
    tokenized_prompt=[]
    prompt=split(prompt)
    ans=split(ans)

    for word in prompt
        word_tokenizer(word, tokenized_prompt)
    end
    tokenized_ans=[]
    for word in ans
        word_tokenizer(word, tokenized_ans)
    end

    for i in 2:length(tokenized_prompt)
        x=token_to_idx[tokenized_prompt[i-1]]
        y=token_to_idx[tokenized_prompt[i]]
        Transition_Matrix[x, y]+=α
    end
    for i in 2:length(tokenized_ans)
        x=token_to_idx[tokenized_ans[i-1]]
        y=token_to_idx[tokenized_ans[i]]
        Transition_Matrix[x, y]+=α
    end

end
println("DONE")
# now test with input
while (true)
    print("Input: ")
    input=split(readline())

    tokenized_prompt=[]
    for word in input
        word_tokenizer(word, tokenized_prompt)
    end

    for i in 2:length(tokenized_prompt)
        x=token_to_idx[tokenized_prompt[i-1]]
        y=token_to_idx[tokenized_prompt[i]]
    end

    # now lets make the ans
    # from the last word of the input look up max in transition matrix
    last_word=tokenized_prompt[end]
    i=token_to_idx[last_word]
    next=argmax(Transition_Matrix[i, :])
    next_token = idx_to_token[next]
    println(next_token)
    # lets go for next 10 tokens

    generated = String[next_token]
    recent = [next_token]

    for j in 1:10
        l = token_to_idx[generated[end]]

        if sum(Transition_Matrix[l, :]) == 0
            break
        end

        row = copy(Transition_Matrix[l, :])
        for t in recent
            row[token_to_idx[t]] = 0.0
        end

        if sum(row) == 0   # everything got zeroed out by the repeat-penalty — fall back to unpenalized row
            row = Transition_Matrix[l, :]
        end

        next_idx = sample(1:length(row), Weights(row))
        next_tok = idx_to_token[next_idx]

        push!(generated, next_tok)
        push!(recent, next_tok)
        if length(recent) > 3
            popfirst!(recent)   # keep only a short recent-history window
        end
    end

    println(join(generated, " "))

end
