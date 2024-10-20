# Notes for *Transformers for Machine Learning*


## Transformers, pg. 46

- The source or target are tokenized and passed through:
    - **word embedding**, which can convert words into a sentence and into a matrix
    - **positional encoding**, which makes sure the words are passed in a specific order.

- Self attention blocks are the **basic building blocks** in transformers for encoders and decoders. 

- An input is mapped to **query, key and value**, and generates an output.


## Query, key, and value, pg. 50

- The role of the *query* vector of a token is to combine with every other key vector to influence the weights for its own output.

- The role of the *key* vector of a token is to be matched with every other query vector to get similarity with query and to influence the output through query-key product scoring.

- The role of the *value* vector of a token is extracting information by combining with the output of the query-key scores to get the output vector.


## Other attentions, pg. 51

- Multi-head attention have multiple sets of query/key/value weight matrices, each resulting in different query/key/value matrices for the inputs, finally generating output matrices. Each output matrices are concatenated and multiplied with an additional weight matrix to get a single final matrix.

- Masked multi-head attention masks tokens that are not previous target tokens. This is implemented by having a masking weight matrix M that has negative infinity for future tokens and 0 for previous tokens. This can help the decoder learn from the encoder sequence and a particular decoder sequence to predict the next word or character.

- In encoder-decoder multi-head attention, the query vectors from the target sequence (before a given time) and the keys and valuesfrom the entire input sequence of the encoder are passed to the self-attention layer in the decoder. This is for the decoder side to learn the attention relationship between the entire source input and the target output at a given time.


## Residuals and Layer Normalization, pg. 53

**Covariate shift:** the gradient dependencies between each layer, or the distribution of input data shifts between the training environment and live environment

- Layer normalization reduces covariate shift by speeding up the convergence as fewer iterations are needed.

- It works independent of the batch size


## Positionwise Feed-forward Networks

- Decoders and encoders have a connected feed-forward network after the attention layers. For each position, linear transformations with a ReLU activation in between is performed. Each go through the same transformations and are only different vat the layer level.


## Encoder, pg. 54

- Every layer of multi-head attention attends to the input or the source; attention between inputs and inputs such as: part-of-speech, constituents, dependencies, entity resolution, etc.


## Decoder

- The first layer attends to the target, or attention between masked outputs with themselves. The encoder-decoder attention layer creates attention between the source and the target.