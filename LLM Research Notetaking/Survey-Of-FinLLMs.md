# Notes for *Survey of Large Language Models in Finance*


## Introduction


### Pre-trained Language Models

- PLMs, or pre-trained language models inspired LLMs. They are basically the same; LLMs are PLMs but with a parameter size of over 7 billion.


### From General LMs to Finance

- As PLMs developed, there was growing interest in applying NLP (natural language processing) on financial tasks such as sentiment analysis, question answering, and stock market prediction. This spurred research on Financial LLMs.

- These Financial LLMs used methods such as mixed-domain LLMs with prompt engineering and instruction fine-tuned LLMs with prompt engineering.


#### GPT series

- GPT: Generative Pre-trained Transformer

- GPTs first started with different models, with GPT-3 being a significant milestone going from GPT-2's 1.5B to GPT-3's 175B parameters.

- GPT-3 introduced in-context learning for LLMs. This is when the model acquires capabilities that were not explicitly trained, which allows language models to understand human language and produce outcomes beyond their original pre-training objectives.

- Eventually, further releases of models led to ChatGPT. 

- ChatGPT combined GPT-3, Codex, and InstructGPT.

    - What was so special about ChatGPT was that it took each revolutionary property the three models had in in-context learning, LLMs for code, and Reinforcement Learning With Human feedback (RLHF) and put it into a single application.

    - Additionally, the success of ChatGPT inspired the further development of significantly larger models, include GPT-4 which is around 1.7T parameters.


#### Open-source LLMs

- BERT: Bidirectional Encoder Representations from Transformers

- BERT is the foundational model for many early PLMs, including FinBERT.

- Meta AI released the open-source LLM LLaMA which encouraged the development of diverse LLMs using LLamA.

- Variants quickly proliferated by adopting various techniques such as Instruction Fine-Tuning (IFT) and Chain-of-Though (CoT) Prompting.

- Additionally, the research community was motivated to generate open-source LLMs to reduce the reliance on corporate research and propietary models.

    - BLOOM was built by a collaboration of hundreds of researches from the BigScience Workshop.


#### Financial-domain LMs

- In financial-domain LMs, there are primarily four financial PLMs (FinPLMs) and four financial LLMs (FinLLMs).

- Within the four FinPLMs, FinBERT-19, FinBERT-20, and FinBERT-21 are all based on BERT, while FLANG is based on ELECTRA.

- Within the four FinLLMs, FinMA, InvestLM, and FinGPT are based on LLaMA or other open-source-based models, while BloombergGPT is a BLOOM-style closed-source model.
