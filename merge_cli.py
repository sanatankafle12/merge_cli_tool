import argparse
from pathlib import Path
from merger.merge_logic import merge_depth_and_video

def main():
    parser = argparse.ArgumentParser(description="Merge RGB video + ZLIB depth files in a folder")
    parser.add_argument("--folder", required=True, help="Path to folder containing video, meta, and zlib files")
    args = parser.parse_args()

    folder_path = Path(args.folder)
    if not folder_path.is_dir():
        print(f"Error: {folder_path} is not a valid directory")
        return
    

    # Assume file naming convention: <basename>.mp4, <basename>.json, <basename>.depth.zlib
    video_files = list(folder_path.glob("*_trimmed.mp4"))
    video_file = video_files[0]
    base_name = video_file.stem
    base_name_sanitized = base_name.split('_trimmed')[0]
    
    meta_file = folder_path / f"{base_name_sanitized}.json"
    zlib_file = folder_path / f"{base_name_sanitized}.depth.zlib"
    output_file = folder_path / f"{base_name_sanitized}_merged.mp4"
    
    if not meta_file.exists() or not zlib_file.exists():
        print(f"Skipping {base_name_sanitized}: missing meta or zlib file")
        return        

    print(f"Merging {base_name}...")
    merge_depth_and_video(
        video_path=str(video_file),
        meta_data_path=str(meta_file),
        zlib_path=str(zlib_file),
        output_path=str(output_file)
    )
    print(f"Done! Output saved to: {output_file}")

if __name__ == "__main__":
    main()
