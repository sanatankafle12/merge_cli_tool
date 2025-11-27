import zlib
import cv2
import numpy as np
from tqdm import tqdm
import json

def load_zlib_data(depth_map_path, num_of_frames, frame_h, frame_w, dtype=np.uint8):
  depth_map = []
  with open(depth_map_path, "rb") as f:
      compressed_depth_map = f.read()
      try:
          b_depth_map = zlib.decompress(compressed_depth_map, wbits=-zlib.MAX_WBITS)
          print("Decompressed data:", b_depth_map[:100])  # Print first 100 bytes
          matrix_shape = (num_of_frames, frame_h, frame_w)

          print("matrix shape: ", matrix_shape)
          print("dtype: ", dtype)

          depth_map = np.frombuffer(b_depth_map, dtype=dtype).reshape(matrix_shape)
      except zlib.error as e:
          print("Decompression failed:", e)
      return depth_map
  
def alight_map_with_rbg_frame(depth_map, image_height, image_width):
  rotated_depth_image_90 = cv2.rotate(depth_map, cv2.ROTATE_90_CLOCKWISE)
  return cv2.resize(
    rotated_depth_image_90.astype(np.float32),
    (image_width, image_height),
    interpolation=cv2.INTER_LINEAR,
  )
  
  
def load_video_as_array(video_path):
    cap = cv2.VideoCapture(video_path)
    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    # List to store the frames
    frames = []

    # Read frames from the video
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Exit the loop when the video ends

        # Append each frame (NumPy array) to the list
        frames.append(frame)
    # Convert the list of frames to a 4D NumPy array (frames, height, width, channels)
    video_array = np.array(frames)
    cap.release()
    print(f"Video shape: {video_array.shape}")
    return video_array

def merge_two_frames(frame_1, frame_2, cmap=cv2.COLORMAP_JET):
    """
    frame_1: rgb
    frame_2: confidence Map
    """
    # Merge the RGB image and the colored depth map
    height, width, channel = frame_1.shape

    resized_frame_2 = cv2.resize(frame_2.astype(np.float32), (width, height), interpolation=cv2.INTER_LINEAR)

    frame_2_normalized = cv2.normalize(resized_frame_2, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    # # Convert the normalized depth map to a 3-channel image
    frame_2_colored = cv2.applyColorMap(frame_2_normalized, cmap)

    merged_image = cv2.addWeighted(frame_1, 0.1, frame_2_colored, 0.9, 0)

    return merged_image

def meta_data(meta_data_path):
    with open(meta_data_path, "r") as fp:
        meta_data = json.load(fp)
        
    for item in meta_data["streams"]:
        if item.get("file_extension") == "depth.zlib":
            # print(item)
            d_number_of_frames = item["number_of_frames"]
            d_freq = item["frequency"]
            d_resolution = item["resolution"]
            
    return(d_number_of_frames, d_resolution,d_freq)
  
  
def merge_two_matrix(output_path, fps, rgb_matrix, depth_map,image_height, image_width, merge_func, cmap=cv2.COLORMAP_JET):
    num_frames, height, width = rgb_matrix.shape[:3]
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for AVI video
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width*2, height*2))

    for idx in tqdm(range(num_frames)):
        depth_frame = depth_map[idx]
        rgb_frame = rgb_matrix[idx]

        depth_frame = alight_map_with_rbg_frame(depth_frame, image_height, image_width)

        if cmap is None:
          merged_frame = merge_func(rgb_frame, depth_frame)
        else:
          merged_frame = merge_func(rgb_frame, depth_frame, cmap=cmap)

        if merged_frame.shape[0] != height*2 or merged_frame.shape[1] != width*2:
          merged_frame = cv2.resize(merged_frame, (width*2, height*2))

        video_writer.write(merged_frame)  # Write the frame to the video

    video_writer.release()
    print(f"Video saved to {output_path}")
    
def merge_depth_and_video(video_path, meta_data_path, zlib_path, output_path):
    d_number_of_frames, d_resolution, d_freq = meta_data(meta_data_path)
    depth_map = load_zlib_data(zlib_path, d_number_of_frames, d_resolution[0], d_resolution[1], dtype=np.float16)
    rgb_matrix = load_video_as_array(video_path)
    image_height, image_width = rgb_matrix[0].shape[0], rgb_matrix[0].shape[1]
    merge_two_matrix(output_path, 5, rgb_matrix, depth_map,image_height, image_width, merge_func=merge_two_frames)

