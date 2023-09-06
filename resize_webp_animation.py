import argparse
from PIL import Image, ImageSequence
import os

def resize_image(input_file, output_file, new_width, new_height):
    with Image.open(input_file) as img:
        # 이미지 리사이즈
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        img_resized.save(output_file)

def resize_webp_animation(input_folder, output_folder, new_width, new_height):
    # 만약 출력 폴더가 존재하지 않으면 폴더를 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 입력 폴더에서 모든 파일 찾기
    for filename in os.listdir(input_folder):
        input_file = os.path.join(input_folder, filename)
        if filename.endswith(".webp"):
            # webp 애니메이션 리사이즈
            output_file = os.path.join(output_folder, filename)
            with Image.open(input_file) as img:
                frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
                resized_frames = [frame.resize((new_width, new_height), Image.LANCZOS) for frame in frames]
                resized_frames[0].save(
                    output_file,
                    save_all=True,
                    append_images=resized_frames[1:],
                    duration=img.info['duration'],
                    loop=img.info['loop'],
                )
                print(f"{filename} 이미지가 리사이즈되어 {output_file}로 저장되었습니다.")
        elif filename.endswith(".png"):
            # PNG 이미지 리사이즈
            output_file = os.path.join(output_folder, filename)
            resize_image(input_file, output_file, new_width, new_height)
            print(f"{filename} 이미지가 리사이즈되어 {output_file}로 저장되었습니다.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize WebP animations and PNG images.")
    parser.add_argument("input_folder", help="Input folder containing WebP animations and PNG images.")
    parser.add_argument("output_folder", help="Output folder for resized images.")
    parser.add_argument("new_width", type=int, help="Desired width for resizing.")
    parser.add_argument("new_height", type=int, help="Desired height for resizing.")
    args = parser.parse_args()

    resize_webp_animation(args.input_folder, args.output_folder, args.new_width, args.new_height)
