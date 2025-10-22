import os
import cv2

def frames_to_videos(input_root, output_root, fps=25):
    """
    将每个小文件夹下的帧图片按顺序合成为视频。
    
    参数:
        input_root  : 大文件夹路径，包含多个子文件夹（每个子文件夹是一段视频帧）
        output_root : 输出视频保存路径
        fps         : 视频帧率（默认25）
    """
    os.makedirs(output_root, exist_ok=True)

    # 遍历所有子文件夹
    for folder in sorted(os.listdir(input_root)):
        folder_path = os.path.join(input_root, folder)
        if not os.path.isdir(folder_path):
            continue

        # 获取所有帧文件并排序
        frames = sorted([
            f for f in os.listdir(folder_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])

        if len(frames) == 0:
            print(f"⚠️ 跳过 {folder} ：未找到图片")
            continue

        # 读取第一帧，确定视频尺寸
        first_frame = cv2.imread(os.path.join(folder_path, frames[0]))
        if first_frame is None:
            print(f"⚠️ 跳过 {folder} ：无法读取第一帧")
            continue
        height, width, _ = first_frame.shape

        # 输出视频路径
        output_video_path = os.path.join(output_root, f"{folder}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

        print(f"🎞️ 正在生成视频：{folder}.mp4 ({len(frames)}帧)...")

        # 逐帧写入
        for frame_name in frames:
            frame_path = os.path.join(folder_path, frame_name)
            frame = cv2.imread(frame_path)
            if frame is None:
                print(f"⚠️ 无法读取帧：{frame_path}")
                continue
            video_writer.write(frame)

        video_writer.release()
        print(f"✅ 已保存：{output_video_path}\n")


if __name__ == "__main__":
    input_root = r"G:\new_test\output\cow_wanzheng"       # 大文件夹路径（帧图片所在位置）
    output_root = r"G:\new_test\output\cow_video"       # 输出视频保存路径
    frames_to_videos(input_root, output_root, fps=25)
