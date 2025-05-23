import pandas as pd
import matplotlib.pyplot as plt
import sys
import os


def visualize_vram(log_file_path):
    """
    VRAMログファイルからデータを読み込み、VRAM使用量のグラフを可視化します。

    Args:
        log_file_path (str): VRAMログファイルへのパス。
    """
    if not os.path.exists(log_file_path):
        print(f"Error: Log file '{log_file_path}' not found.")
        sys.exit(1)

    try:
        # CSVファイルとして読み込む
        df = pd.read_csv(log_file_path)
    except pd.errors.EmptyDataError:
        print(
            f"Error: Log file '{log_file_path}' is empty. No data to visualize."
        )
        sys.exit(1)
    except Exception as e:
        print(f"Error reading log file '{log_file_path}': {e}")
        sys.exit(1)

    # Timestampをdatetimeオブジェクトに変換
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # グラフの準備
    plt.figure(figsize=(14, 7))

    # --- 全体のVRAM使用量をプロット ---
    # Process_PIDが 'N/A' の行が全体のVRAM使用量に相当
    df_overall = df[df["Process_PID"] == "N/A"]
    if not df_overall.empty:
        # 同じタイムスタンプで複数のGPUがある場合、通常は各GPUの全体使用量が記録される
        # ここでは、各GPU IDごとに全体のVRAM使用量をプロットする
        for gpu_id in df_overall["GPU_ID"].unique():
            gpu_overall_data = df_overall[df_overall["GPU_ID"] == gpu_id]
            plt.plot(
                gpu_overall_data["Timestamp"],
                gpu_overall_data["VRAM_Used_MiB"],
                label=f"Total VRAM Used (GPU {gpu_id})",
                linestyle="--",
            )
    else:
        print("Warning: No 'Overall' VRAM usage data found in the log file.")

    # --- 監視対象プロセスのVRAM使用量をプロット ---
    # Process_PIDが 'N/A' ではない行の中から、ユニークなPIDを取得
    # run_and_monitor.sh で監視対象としたPIDがログに含まれるはず
    monitored_pids = (
        df[df["Process_PID"] != "N/A"]["Process_PID"].dropna().unique()
    )

    if monitored_pids.size > 0:
        # 監視対象のPIDが複数ある場合は、それぞれをプロット
        for pid in monitored_pids:
            df_process_data = df[df["Process_PID"] == pid]
            if not df_process_data.empty:
                # プロセスは通常、単一のGPUで実行されるが、念のためGPU IDごとにプロット
                for gpu_id in df_process_data["GPU_ID"].unique():
                    gpu_process_data = df_process_data[
                        df_process_data["GPU_ID"] == gpu_id
                    ]
                    plt.plot(
                        gpu_process_data["Timestamp"],
                        gpu_process_data["Process_VRAM_Used_MiB"],
                        label=f"Process {pid} VRAM Used (GPU {gpu_id})",
                    )
            else:
                print(f"Warning: No VRAM data found for process PID {pid}.")
    else:
        print(
            "Warning: No specific process VRAM usage data found in the log file."
        )
        plt.title("Overall VRAM Usage Over Time (No specific process data)")

    plt.xlabel("Time")
    plt.ylabel("VRAM Usage (MiB)")
    plt.title("VRAM Usage Over Time")
    plt.legend()
    plt.xticks(rotation=45, ha="right")  # タイムスタンプが重ならないように回転
    plt.tight_layout()  # レイアウトを自動調整
    plt.grid(True)  # グリッド線を表示
    plt.show()  # グラフを表示


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 visualize_vram.py <vram_log_file.log>")
        sys.exit(1)

    log_file = sys.argv[1]
    visualize_vram(log_file)
