#!/bin/bash

# VRAM監視スクリプト
# 使用法: ./monitor_vram.sh <output_log_file> <sampling_interval_seconds> <pid_to_monitor>

OUTPUT_LOG_FILE=$1
SAMPLING_INTERVAL=${2:-1} # デフォルトは1秒
PID_TO_MONITOR=$3

if [ -z "$OUTPUT_LOG_FILE" ]; then
    echo "Usage: $0 <output_log_file> <sampling_interval_seconds> <pid_to_monitor>"
    exit 1
fi

echo "Timestamp,GPU_ID,GPU_Name,VRAM_Used_MiB,VRAM_Total_MiB,Process_PID,Process_Name,Process_VRAM_Used_MiB" > "$OUTPUT_LOG_FILE"

# PythonスクリプトのPIDが有効である間、VRAMを監視
while kill -0 "$PID_TO_MONITOR" 2>/dev/null; do
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

    # 全体VRAM使用量とプロセスごとのVRAM使用量を同時に取得
    # コマンド出力例:
    # 0,NVIDIA GeForce RTX 3080,2000,10240
    # 0,python,12345,1500
    nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv,noheader --unit=MiB | while IFS=, read -r gpu_id gpu_name vram_used vram_total; do
        # 全体VRAM使用量を記録
        echo "$TIMESTAMP,$gpu_id,$gpu_name,$vram_used,$vram_total,N/A,Overall,N/A" >> "$OUTPUT_LOG_FILE"

        # プロセスごとのVRAM使用量を記録 (対象PIDがある場合のみ)
        if [ -n "$PID_TO_MONITOR" ]; then
            nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory --format=csv,noheader,nounits | while IFS=, read -r uuid process_pid process_name used_memory; do
                if [ "$process_pid" == "$PID_TO_MONITOR" ]; then
                    # GPU IDをUUIDから取得 (nvidia-smi -LでUUIDとIDの対応を確認できるが、ここでは簡易的に対象PIDの情報をそのまま記録)
                    # より正確にはGPU UUIDからIDへのマッピングが必要だが、複雑になるため簡略化
                    # 通常、単一のGPUであれば問題ない
                    echo "$TIMESTAMP,$gpu_id,$gpu_name,N/A,N/A,$process_pid,$process_name,$used_memory" >> "$OUTPUT_LOG_FILE"
                fi
            done
        fi
    done

    sleep "$SAMPLING_INTERVAL"
done

echo "Monitoring finished. Python process $PID_TO_MONITOR is no longer running."