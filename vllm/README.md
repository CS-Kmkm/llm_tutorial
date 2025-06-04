# vLLM
## 概要
LLMの推論高速化のためのライブラリ「vllm」についての情報を整理

## 本資料のスコープ
+ vLLMの概要
+ vLLMのインストール
+ vLLMの基本的な使い方
    + 1つのプロンプトを単純に推論
+ 少し応用的な使い方
    + OpenAI API互換のAPIとしての利用
    + Structured Output

## 本資料が対象としないもの
+ vLLMの内部実装
    + PagedAttention
+ 一部環境へのインストール
    + CUDA11.8以前の環境
        + (本研究室のGPU４号機以前の環境)
+ OpenAI API互換APIとしての詳細な利用方法
    + (別の方がしっかり紹介してくれるため)
+ その他上で記述していない実装
    + Streaming output

