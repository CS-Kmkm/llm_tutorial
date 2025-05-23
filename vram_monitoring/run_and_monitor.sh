#!/bin/bash

# Pythonスクリプトを実行し、VRAMを監視するスクリプト
# 使用法: ./run_and_monitor.sh <python_script.py> [sampling_interval_seconds]

PYTHON_SCRIPT=$1
SAMPLING_INTERVAL=${2:-1} # デフォルトは1秒

if [ -z "$PYTHON_SCRIPT" ]; then
    echo "Usage: $0 <python_script.py> [sampling_interval_seconds]"
    exit 1
fi

# Pythonスクリプトのファイル名から拡張子を除いた部分を取得
# 例: path/to/hoge.py -> hoge
SCRIPT_BASENAME=$(basename "$PYTHON_SCRIPT" .py)

# ログファイル名を設定 (スクリプトのベース名.log)
LOG_DIR="./vram_logs"
mkdir -p "$LOG_DIR"
# ここでYYYYMMDD_HHMMSSのようなタイムスタンプも維持したい場合は、以下のように結合します
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_LOG_FILE="${LOG_DIR}/${SCRIPT_BASENAME}_${TIMESTAMP}.log" # ここを修正

echo "Starting Python script: $PYTHON_SCRIPT"
echo "VRAM log will be saved to: $OUTPUT_LOG_FILE"
echo "Sampling interval: ${SAMPLING_INTERVAL} seconds"

# Pythonスクリプトをバックグラウンドで実行し、PIDを取得
python3 "$PYTHON_SCRIPT" &
PYTHON_PID=$!
echo "Python script PID: $PYTHON_PID"

# VRAM監視スクリプトをバックグラウンドで実行
./monitor_vram.sh "$OUTPUT_LOG_FILE" "$SAMPLING_INTERVAL" "$PYTHON_PID" &
MONITOR_PID=$!
echo "VRAM monitor PID: $MONITOR_PID"

# Pythonスクリプトが終了するまで待機
wait "$PYTHON_PID"

# VRAM監視スクリプトがまだ実行中であれば終了させる
if kill -0 "$MONITOR_PID" 2>/dev/null; then
    echo "Python script finished. Stopping VRAM monitor..."
    kill "$MONITOR_PID"
fi

echo "All processes finished."