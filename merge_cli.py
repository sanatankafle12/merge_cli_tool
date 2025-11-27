import argparse
from merger.merge_logic import merge_depth_and_video

def main():
    parser = argparse.ArgumentParser(description="Merge RGB video + ZLIB depth into one merged video")
    parser.add_argument("--video", required=True, help="Path to input video file")
    parser.add_argument("--meta", required=True, help="Path to metadata JSON file")
    parser.add_argument("--zlib", required=True, help="Path to depth.zlib file")
    parser.add_argument("--output", required=True, help="Path to save merged video")

    args = parser.parse_args()

    print("Merging...")

    merge_depth_and_video(
        video_path=args.video,
        meta_data_path=args.meta,
        zlib_path=args.zlib,
        output_path=args.output
    )

    print(f"Done! Output saved to: {args.output}")


if __name__ == "__main__":
    main()
