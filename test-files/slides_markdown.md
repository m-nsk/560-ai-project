###### Spring 2025
#### Artificial Intelligence
### Language Models & Transformers
###### Tianlong Chen


1


-----

### What is it?

Donald Trump … was the 45th president … … of … the … United … States

***Language models*** *(such as ChatGPT) just predict the next word likely to a given*

*sequence of words*

*Auto-complete on your phone message app does the same thing!*

*Learn to do this from billions of documents on the web*

**Just bigger! Better! Stronger!**


-----

### What is it?

*Can learn what words are similar, what words tend to occur*

*together, what words follow each other …*


-----

### What is ChatGPT?




*ChatGPT is a complicated function described by about 175 billion numbers* *(or ‘parameters’)*


-----

### What does it do?


-----

## Language Modeling with FFNs?


This is modeling
fixed-length context


6


-----

## Word embeddings


7


-----

### How it works?

GPT: Generative Pretrained Transformers

Pretrained Transformers
Generative


-----

### How it works?

Intelligent behavior of language models is

**emergent**, not pre-programmed

Neural network parameters (those 175 billion

numbers!) are very hard to interpret

*Actual answer: No one knows!*


-----

### How to build it?






Encoder


my        dog      ​jumped

Transformer Encoder Stack


10


-----

### Self-Attention

L x d

My

Dog

​jumped

with

|Col1|Col2|Col3|
|---|---|---|
||||
||||
||||


Input


11


-----

### Self-Attentio n

L x d

|Col1|Col2|Col3|
|---|---|---|
||||
||||
||||



Input

Value


L x d’

|Col1|Col2|
|---|---|
|||
|||
|||



Query

L x d’

|Col1|Col2|
|---|---|
|||
|||
|||



Key

L x d



L x d

|Col1|Col2|Col3|
|---|---|---|
||||
||||
||||



Output

=Value[max(Query * Key)]

|1|0|0|0|
|---|---|---|---|
|0|0|1|0|
|0|0|0|1|
|1|0|0|0|


12

|Col1|Col2|Col3|
|---|---|---|
||||
||||
||||


-----

### Self-Attentio n

L x d

|Col1|Col2|Col3|
|---|---|---|
||||
||||
||||



Input

Value


L x d’

|Col1|Col2|
|---|---|
|||
|||
|||



Query

L x d’

|Col1|Col2|
|---|---|
|||
|||
|||



Key

L x d



L x d

|Col1|Col2|Col3|
|---|---|---|
||||
||||
||||



Output

=AttnScore(Query, Key)Value

13

|Col1|Col2|Col3|
|---|---|---|
||||
||||
||||

|Col1|Col2|Col3|Col4|
|---|---|---|---|
|||||
|||||
|||||


-----

### What does self attention do?

Attn Score 14

Image from https://jalammar.github.io/illustrated-transformer/


-----

### Multi-Head Attention


15


Image from https://jalammar.github.io/illustrated-transformer/


-----

##### Feedforward Network (FFN)

 For each position in the sequence




W₁, W₂, b₁, b₂ are parameters of the feedforward network


-----

##### Parameters of a Transformer



Parameters

𝑊 1, 𝑊 2, 𝑏 1, 𝑏 2

For each head,
we have 𝑊 [𝑄], 𝑊 [𝐾], 𝑊 [𝑉]


-----

##### Multiple Layers!



*Embeddings are learnable too.*


-----

##### Pretraining and Fine-Tuning



My           dog          ​jumped         with        excitement


-----

##### Pretraining and Fine-Tuning

V₁ V₂ V₃ V₄


*Bidirectional*

*information*

|flow!|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Prediction layer||||||||||||||||||||||||
|||||||||||||||||||||||||



My           dog         <MASK>         with        excitement


-----

##### Fine-Tuning

 Need small amount of data for downstream task for training

 Only one additional (final) layer is trained for specific tasks

Zero shot Few shot Full language model

Image from Fine-Tuned Language Models Are Zero-Shot Learners


-----

# Advanced Transformer Architectures


-----

##### Outline

Encoder only Transformers

Decoder only Transformers

Encoder-Decoder Transformers

Future Directions & Challenges


-----

# Encoder-Only Transformers


-----

##### Encoder-Only Transformers

 Process input sequences without generating outputs

 Excel in tasks such as text classification and sentiment analysis



-----

##### Encoder-Only Transformers (cont.)

 - **Text classification** **Sequence labeling**


*NNP*


*VB*



*NNP*







Carolina beat Duke <CLS>


Carolina beat Duke <CLS>


-----

###### BERT (Bidirectional Encoder Representations From Transformers)

Image from [BERT: Devlin et al., 2019]


-----

##### Pretraining

 Pretraining can allow learning of useful Inductive biases about the data,

usually in an unsupervised way.

 Empirically, results in faster convergence and better performance on the

downstream task.

 Also, usually requires much less labeled data for the downstream task.

 How to pretrain with unlabeled data?


-----

##### Masked Language Model (MLM)



My           dog          ​jumped         with        excitement


-----

##### Masked Language Model (MLM)

V₁ V₂ V₃ V₄


*Bidirectional*

*information*

|flow!|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|Col24|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Prediction layer||||||||||||||||||||||||
|||||||||||||||||||||||||



My           dog         <MASK>         with        excitement


-----

##### Next Sentence Prediction (NSP)

 MLM trains model to learn relationships between tokens.

 NSP trains model to learn relationship between sentence.


-----

##### Fine-Tuning

 Need small amount of data for downstream task for training.

 Only one additional (final) layer is trained for specific tasks

Zero shot Few shot Full language model

Image from Fine-Tuned Language Models Are Zero-Shot Learners


-----

# Decoder-Only Transformers


-----

##### Decoder-Only Transformers

 Focus on generating output sequences

 Most suitable for language modeling tasks such as text generation and

completion

*Only* *pay* *attention* *to* *words* *already* *generated*

 Different idea from the bidirectionality in BERT

 Use a transformer stack for language generation


-----

|How to Train a Decoder-Only Transformer Stack?|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
|• Simply ignore attention scores for future tokens in self-attention 𝑞 • 1 Set upper-triangular portion of the 𝑇 𝑄t𝐾 matrix o −∞ 𝑞 . 2 • Softmax will convert these to 0 attention scores 𝑞 . 3||“Causal masking”|||||
||𝑞 1|. 𝑘 1|−∞|−∞|−∞|−∞|
||𝑞 . 2|𝑘 1|𝑞 . 𝑘 2 2|−∞|−∞|−∞|
||n 𝑞 . 3|𝑘 1|𝑞 . 𝑘 3 2|𝑞 . 𝑘 3 3|−∞|−∞|
||||𝑞 . 𝑘 4 2|𝑞 . 𝑘 4 3|𝑞 . 𝑘 4 4|−∞|
|That is, the model will only consider previous tokens when generating the next token.|||||||
||𝑞 . 𝑘 5 1||𝑞 . 𝑘 5 2|𝑞 . 𝑘 5 3|𝑞 . 𝑘 5 4|𝑞 . 𝑘 5 5|


-----

###### How to Train a Decoder-Only Transformer Stack? (cont.)

 Apart from causal masking, no


difference from the encoder-only

architecture

***Important:*** *Unlike RNN LMs, this*

*training can be completely*
*parallelized!*


|𝑞 . 𝑘 1 1|−∞|−∞|−∞|−∞|
|---|---|---|---|---|
|𝑞 . 𝑘 2 1|𝑞 . 𝑘 2 2|−∞|−∞|−∞|
|𝑞 . 𝑘 3 1|𝑞 . 𝑘 3 2|𝑞 . 𝑘 3 3|−∞|−∞|
|𝑞 . 𝑘 4 1|𝑞 . 𝑘 4 2|𝑞 . 𝑘 4 3|𝑞 . 𝑘 4 4|−∞|
|𝑞 . 𝑘 5 1|𝑞 . 𝑘 5 2|𝑞 . 𝑘 5 3|𝑞 . 𝑘 5 4|𝑞 . 𝑘 5 5|


-----

##### Advantages of Transformer-Based Generation

 Parallelized training can enable larger models and training sets

 Training is stable compared to RNNs

   Due to layer normalization and residual connections

   No vanishing or exploding gradients, “path length” is always 1

*Empirically, we see log-linear*
*relationships between model size*
*and loss, and training data size and*
*loss.*

Figure from: Scaling Laws for Neural Language Models, Kaplan et al., 2020.


-----

##### GPT Series of LMs

Figure from: Scaling Laws for Neural Language Models, Kaplan et al., 2020.


-----

# Encoder-Decoder Transformers


-----

##### Encoder-Decoder RNNs


-----

##### Encoder-Decoder Transformers


-----

##### Encoder-Decoder Transformers (cont.)

 Original transformer

   The original model introduced an encoder-decoder architecture

   Tasks like machine translation, summarization

   Why might this be better than decoder only?

   *For example: Even when* ***he*** *was a young boy, George Washington …*

 T5 (Text-to-Text Transfer Transformer)

   Unified approach where all NLP tasks are reformulated as text-to-test tasks

   *For example: Classify sentiment: The movie was horrendous …*

 BART (Bidirectional and Auto-Regressive Transformers)

   Combines bidirectional and auto-regressive training objective

   Good with both generation and sequence-to-sequence tasks


-----

##### Challenges and Future Directions

 Computational issues and scalability

 Interpretability

 Domain adaptation

 
…


-----

##### Scalability: Computational Issue With Transformers


|Col1|L x d|Col3|
|---|---|---|
||||
||||
||||
||||


Output



|Col1|Col2|Col3|Col4|
|---|---|---|---|
|||||
|||||
|||||

|Col1|L x d|Col3|
|---|---|---|
||||
||||
||||
||||


=AttnScore(Query, Key)Value


Input




Value

|Col1|Col2|Col3|
|---|---|---|
||||
||||
||||


-----

##### Scalability: Approximate Attention

L x r
###### Attention = Softmax


L x d


r x L


Query Key [T] Value

*O(rLd)*

*O(Lrd)*


Fast Autoregressive Transformers With Linear Attention


-----

##### Scalability: Sparse Graphs


New

to


The

sent


The

firm

for

which

Jacob

worked

sent

him

to

New York


n x n


which


Attn Scores

[Figure from Manzil Zaheer | Big Bird: Transformers for Longer Sequences](https://www.youtube.com/watch?v=_oSy_QvjHTs)


-----

##### Interpretability

 Decision-making processes of transformers can be unclear

 Techniques for interpreting attention weights?

 What do different heads in multi-head attention do?


-----

