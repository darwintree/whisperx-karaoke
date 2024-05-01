import os
import torch, whisperx
import argparse
from whisperx.types import SingleAlignedSegment, SingleSegment
from whisperx_karaoke.resolver import parse_file
from whisperx_karaoke.ass import segments_to_ass_text


def get_audio_and_song_path(dir_path: str) -> tuple[str, str]:
    files = os.listdir(dir_path)
    audio_path = None
    lrc_path = None
    audio_postfixes = [".mp3", ".wav", ".opus", ".m4a", ".aac"]
    for file in files:
        for audio_postfix in audio_postfixes:
            if file.endswith(audio_postfix):
                audio_path = os.path.join(dir_path, file)
        if file.endswith(".lrc"):
            lrc_path = os.path.join(dir_path, file)

    if audio_path is None:
        raise ValueError("No audio found in the directory.")
    if lrc_path is None:
        raise ValueError("No lrc found in the directory.")
    print(f"Audio file: {audio_path}")
    print(f"LRC file: {lrc_path}")
    return audio_path, lrc_path


# modify aligned_segments based on lrc_segments
def use_lrc_start_and_end(
    aligned_segments: list[SingleAlignedSegment], lrc_segments: list[SingleSegment]
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


def cli():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "dir", type=str, help="audio(.mpc, .wav, .opus, .m4a, .aac) & .lrc file directory."
    )
    parser.add_argument(
        "--device",
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="device to use for PyTorch inference",
    )
    parser.add_argument(
        "--language",
        default="ja",
        help="language code for the audio",
    )
    parser.add_argument("--offset", type=float, default=0, help="offset for lrc time")

    args = parser.parse_args().__dict__
    dir_path = args.pop("dir")
    device = args.pop("device")
    language = args.pop("language")
    offset = args.pop("offset")

    audio_path, lrc_path = get_audio_and_song_path(dir_path)
    audio = whisperx.load_audio(audio_path)
    cleared = parse_file(lrc_path, language, offset)
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
        print("ASS file saved to: ", ass_filename)

