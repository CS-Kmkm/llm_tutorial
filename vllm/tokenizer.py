from transformers import AutoTokenizer

model_name = "tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.3"

tokenizer = AutoTokenizer.from_pretrained(model_name)
message = [
    {
        "role": "system",
        "content": "あなたは誠実で優秀な日本人のアシスタントです。",
    },
    {
        "role": "user",
        "content": "tokenizerについて教えてください。",
    },
]

is_tokenize = [True, False]
is_add_generation_prompt = [True, False]

for tokenize in is_tokenize:
    for add_generation_prompt in is_add_generation_prompt:
        prompt = tokenizer.apply_chat_template(
            message,
            tokenize=tokenize,
            add_generation_prompt=add_generation_prompt,
        )
        print(
            f"Tokenize: {tokenize}, Add Generation Prompt: {add_generation_prompt}"
        )
        print(prompt)
        print("=" * 50)
