import os
import whisperx
from whisperx_karaoke.resolver import parse_file, SingleSegment
from whisperx_karaoke.ass import segments_to_ass_text


def get_audio_and_song_path(dir_path: str) -> tuple[str, str]:
    # 获取音频文件路径和歌曲文件路径
    # ...
    files = os.listdir(dir_path)
    audio_postfixes = [".mp3", ".wav", ".opus", ".m4a", ".aac"]
    for file in files:
        for audio_postfix in audio_postfixes:
            if file.endswith(audio_postfix):
                audio_path = os.path.join(dir_path, file)
        if file.endswith(".lrc"):
            lrc_path = os.path.join(dir_path, file)

    print(f"Audio file: {audio_path}")
    print(f"Song file: {lrc_path}")
    return audio_path, lrc_path


# modify aligned_segments based on lrc_segments
def use_lrc_start_and_end(
    aligned_segments: list[SingleSegment], lrc_segments: list[SingleSegment]
):
    last_find_lrc_index = -1
    lrc_list = [segment["text"] for segment in lrc_segments]
    for segment in aligned_segments:
        try:
            latest_found = lrc_list.index(segment["text"], last_find_lrc_index+1)
            last_find_lrc_index = latest_found
            # print("Correcting start and end time...")
            # print(
            #     "Original: ",
            #     segment["start"],
            #     " -> ",
            #     segment["end"],
            #     ": ",
            #     segment["text"],
            # )
            segment["start"] = lrc_segments[last_find_lrc_index]["start"]
            segment["end"] = lrc_segments[last_find_lrc_index]["end"]
            # print(
            #     "Current: ",
            #     segment["start"],
            #     " -> ",
            #     segment["end"],
            #     ": ",
            #     segment["text"],
            # )
        except ValueError:
            print("No corresponding LRC segment found.")


def main():
    dir_path = "./raw/song2"
    device = "cuda"
    language_code = "ja"
    offset = 0
    audio_path, lrc_path = get_audio_and_song_path(dir_path)
    audio = whisperx.load_audio(audio_path)
    cleared = parse_file(lrc_path, language_code, offset)
    # print(cleared)
    for i in range(len(cleared["segments"])):
        index = len(cleared["segments"]) - 1 - i
        if cleared["segments"][index]["text"].strip() == "":
            # print(i)
            cleared["segments"].pop(index)
    model_a, metadata = whisperx.load_align_model(
        language_code=cleared["language"], device=device
    )
    result = whisperx.align(
        cleared["segments"],
        model_a,
        metadata,
        audio,
        device,
        return_char_alignments=False,
    )

    use_lrc_start_and_end(result["segments"], cleared["segments"])

    ass_output = segments_to_ass_text(result["segments"])
    ass_filename = os.path.join(dir_path, f"{os.path.basename(audio_path)}.ass")
    with open(ass_filename, "w", encoding="utf-8") as f:
        f.write(ass_output)


if __name__ == "__main__":
    main()
