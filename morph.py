import cv2
import numpy as np
import os
import glob

def load_images(input_dir):
    image_files = sorted(glob.glob(os.path.join(input_dir, '*')))
    images = [cv2.imread(f) for f in image_files if cv2.imread(f) is not None]
    return images, image_files

def generate_morph_frames(img1, img2, steps=20):
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Resize to same size
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        img2_gray = cv2.resize(img2_gray, (img1.shape[1], img1.shape[0]))

    # Calculate dense optical flow
    flow = cv2.calcOpticalFlowFarneback(img1_gray, img2_gray,
                                        None, 0.8, 5, 25, 3, 5, 1.5, 0)

    morph_frames = []
    for i in range(steps + 1):  # Include the final frame
        alpha = i / float(steps)
        flow_scaled = flow * alpha
        h, w = flow.shape[:2]
        flow_map = np.dstack(np.meshgrid(np.arange(w), np.arange(h))).astype(np.float32)
        remap = flow_map + flow_scaled
        warped = cv2.remap(img1, remap, None, cv2.INTER_LINEAR)
        blended = cv2.addWeighted(warped, 1 - alpha, img2, alpha, 0)
        morph_frames.append(blended)
    return morph_frames

def save_video(frames, output_path, fps=30):
    h, w, _ = frames[0].shape
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    for frame in frames:
        out.write(frame)
    out.release()

def generate_morph_video(file_list: list[str], output_path: str, steps_per_morph: int = 20):
    images = [cv2.imread(f) for f in file_list]
    all_frames = []
    for i in range(len(images) - 1):
        print(f"Generating morph frames for {i + 1} of {len(images)}")
        morph = generate_morph_frames(images[i], images[i+1], steps=steps_per_morph)
        all_frames.extend(morph)
    save_video(all_frames, output_path)
    return output_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-images", required=True, help="Directory with ordered images")
    parser.add_argument("--output-video", required=True, help="Output video file path")
    parser.add_argument("--frames-per-morph", type=int, default=20, help="Frames per morph transition")
    args = parser.parse_args()

    generate_morph_video(args.input_images, args.output_video, args.frames_per_morph)
