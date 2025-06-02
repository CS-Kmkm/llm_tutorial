# enable_prefix_cachingを変更して、time python (ファイル名)で計測
from transformers import AutoTokenizer

from vllm import LLM, SamplingParams

model_name = "tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.3"

tokenizer = AutoTokenizer.from_pretrained(model_name)
llm = LLM(
    model=model_name,
    tensor_parallel_size=1,
    enable_prefix_caching=True,
    max_num_batched_tokens = 4096
)

sampling_params = SamplingParams(temperature=0.0, max_tokens=512, stop="<|eot_id|>")

system_prompt = "あなたは誠実で優秀な日本人のアシスタントです。"
user_prompts = [
    "歩き方について教えてください。",
]*1000

messages = [
    [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    for user_prompt in user_prompts
]

prompts = [tokenizer.apply_chat_template(message, tokenize=False, add_generation_prompt=True) for message in messages]
output = llm.generate(prompts, sampling_params)

# for i, result in enumerate(output):
#     print(f"--- Prompt {i+1} ---")
#     print(result.outputs[0].text)
