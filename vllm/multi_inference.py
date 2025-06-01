from transformers import AutoTokenizer

from vllm import LLM, SamplingParams

model_name = "tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.3"

tokenizer = AutoTokenizer.from_pretrained(model_name)
llm = LLM(
    model=model_name,
    tensor_parallel_size=1,
    enable_prefix_caching=True,
)

sampling_params = SamplingParams(temperature=0.6, top_p=0.9, max_tokens=512, stop="<|eot_id|>")

system_prompt = "あなたは誠実で優秀な日本人のアシスタントです。"
user_prompts = [
    "歩き方について教えてください。",
    "生きるコツを教えてください。",
    "体力回復のための食事について教えてください。",
    "無駄の省き方について教えてください。",
]

messages = [
    [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    for user_prompt in user_prompts
]

prompts = [tokenizer.apply_chat_template(message, tokenize=False, add_generation_prompt=True) for message in messages]
output = llm.generate(prompts, sampling_params)

print(output[0].outputs[0].text)
