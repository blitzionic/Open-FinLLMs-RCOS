# Alex Lin's notes of certain texts.

## Some of these texts include:

- *Transformers for Machine Learning: A Deep Dive* by Kenneth L. Graham, Uday Kamath, Wael Emara
- *Open-FinLLMs: Open Multimodal Large Language Models for Financial Applications* by Anonymous authors
- *Survey of Large Language Models in Finance* by Jean Lee, Nicholas Stevens, Soyeon Caren Han, Minseok Song

### These articles served to help me learn about transformers, LLMs, and FinLLMs during my learning period, as this is my first year on Open-FinLLMs and I required pre-training before I could operate and experiment with the language models. There are three markdown files each documenting my findings on the texts.


# Data from FinLLMs.

### Additionally, I use Google Sheets to record data for different models that I find by running tasks with the models on a Google Colab evaluation script and documenting how well they perform. Each model takes 1-2 hours to collect responses from the 42 tasks given. Most of the work I commit will most likely be benchmarking, which is shown in the sheets files provided.

### For each model, I use Python to evaluate the efficiency. An example of the code I use is below:

!python PIXIU/src/eval.py \
    --model "hf-causal-vllm" \
    --model_args "pretrained=meta-llama/Llama-3.2-1B-Instruct,peft=meta-llama/Llama-3.2-1B-Instruct,tokenizer=meta-llama/Llama-3.2-1B-Instruct,dtype=float16,use_fast=False,max_gen_toks=25" \
    --tasks "flare_cra_travelinsurace" \
    --batch_size 20000 \
    --num_fewshot 0

## The models that I use include:

- Llama 3.2 3B Instruct
- Qwen2.5 7B
- Qwen2.5 7B Instruct
- Mistral 7B Instruct v0.3
- Marco-o1
- Falcon 7B instruct
- Hermes 3 - Llama-3.1 8B
- StarCoder2 7B
- Code Llama 7B Instruct
- GPT-Neo 2.7B

### For each model's data, I downloaded it separately into tab separated value files (.tsv) and added them to the repository, along with an overall Google Sheet downloaded as a Excel sheet file (.xlsx).
