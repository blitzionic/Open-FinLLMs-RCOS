# Notes for 'Open Multimodal Large Language Models for Financial Applications'


OpenFinLLMs is a series of multimodal large language models designed for 
financial applications. Recognizing that traditional LLMs often lack specific 
financial knowledge, FinLLaMA3-8B was introduced, which is a foundational 
model pretrained on a large financial corpus. Furthermore, FinLLaVA-8B was 
also created, which fine-tunes the previous model to handle multimodal inputs, 
including language, vision, and tabular data. The models were evaluated 
on various financial and general tasks, demonstrating superior performance 
compared to existing financial LLMs and achieving results comparable 
to GPT-4o in multimodal tasks.


Financial AI has been driven by advancements in natural language processing 
(NLP), particularly through large language models (LLMs) like GPT-4 and 
Meta's LLaMA series. While these models excel in general tasks, they struggle 
with finance-specific knowledge due to their training on general datasets. 
To address this gap, researchers have developed specialized financial LLMs, 
such as BloombergGPT and FinTral, but these still face limitations, 
particularly in handling multimodal data (text, tabular, and visual) and being 
open-source.


In response, OpenFinLLMs were introduced, a series of open financial 
LLMs designed for multimodal financial applications. The foundational model, 
FinLLaMA-8B, was pretrained on a substantial financial corpus of 52 billion 
tokens. The authors then developed FinLLaMA-Instruct-8B for instruction-based 
tasks and FinLLaVA-8B to handle multimodal financial data.


Key features of OpenFinLLMs include:

Comprehensive Financial Corpus: Curated from diverse sources to enhance 
financial knowledge.

Multimodal Capability: The ability to process both textual and structured 
financial data.

Extensive Evaluations: Comprehensive assessments across various financial 
and general tasks in zero-shot and few-shot settings.

Results indicate that FinLLaMA-8B outperforms existing models in multiple 
financial tasks and exhibits strong trading performance. FinLLaVA-8B leads 
in multimodal financial tasks, even surpassing larger models like GPT-4o in 
certain areas. The authors plan to publicly release their models and evaluation 
benchmarks to promote further academic innovation in financial AI.