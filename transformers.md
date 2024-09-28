# Notes for 'Transformers for Machine Learning'



Transformers


- The source or target are tokenized and passed through word embedding, which can convert words into a sentence and into a matrix, and positional encoding, which makes sure the words are passed in a specific order.

- Self attention blocks are the basic building blocks in transformers for encoders and decoders. An input is mapped to query, key and value, and generates an output.



Query, key, and value


- The role of the query vector of a token is to combine with every other key vector to influence the weights for its own output.

- The role of the key vector of a token is to be matched with every other query vector to get similarity with query and to influence the output through query-key product scoring.

- The role of the value vector of a token is extracting information by combining with the output of the query-key scores to get the
output vector.



Other attentions


- Multi-head attention have multiple sets of query/key/value weight matrices, each resulting in different query/key/value matrices for the inputs, finally generating output matrices. Each output matrices are concatenated and multiplied with an additional weight matrix to get a single final matrix.

- Masked multi-head attention masks tokens that are not previous target tokens. This is implemented by having a masking weight matrix M that has negative infinity for future tokens and 0 for previous tokens. This can help the decoder learn from the encoder sequence and a particular decoder sequence to predict the next word or character.

- In encoder-decoder multi-head attention, the query vectors from the target sequence (before a given time) and the keys and values from the entire input sequence of the encoder are passed to the self-attention layer in the decoder. This is for the decoder side to learn the attention relationship between the entire source input and the target output at a given time.