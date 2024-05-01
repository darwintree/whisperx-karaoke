# %%
song_path = "./raw/song1/1_自分REST@RT (M@STER VERSION)_(Vocals)"
whisper1stout_path = f"{song_path}.json"
import json

whisper1stout = json.load(open(whisper1stout_path))

# %%
for segment in whisper1stout["segments"]:
    print(f"[{segment['start']}] {segment['text']} [{segment['end']}]")

# %%
# cleared = json.load(open("./raw/song1/cleared.json"))
from resolver import parse_file

cleared = parse_file("./raw/song1/lrc.lrc", "ja", offset=-0.8)

# %%
import whisperx

device = "cuda"

audio = whisperx.load_audio(f"{song_path}.mp3")

model_a, metadata = whisperx.load_align_model(
    language_code=cleared["language"], device=device
)

result = whisperx.align(
    cleared["segments"], model_a, metadata, audio, device, return_char_alignments=False
)


# %%
# {\kf20}blabla
# mark duration of a word in aegisub
def formatted_word_with_length(text: str, milliseconds: int):
    return "{\\kf" + str(milliseconds) + "}" + text


def words_to_ass_line(segment, next_segment=None):
    words = segment["words"]
    next_segment_start = segment["end"]
    if next_segment != None:
        next_segment_start = next_segment["start"]

    line = f"Dialogue: 0,{segment['start']},{next_segment_start},orig,,0,0,0,,"
    last_end = segment["start"]
    # append word to the line
    for i in range(len(words)):
        word = words[i]
        if word.get("end"):
            # for the last word of the segment, use next segment start rather than output "end" to count duration
            if i == len(words) - 1:
                line += formatted_word_with_length(
                    word["word"], int(100 * next_segment_start - 100 * last_end)
                )
            else:
                line += formatted_word_with_length(
                    word["word"], int(100 * word["end"] - 100 * last_end)
                )
            last_end = word["end"]
        else:
            line += word["word"]
    return line


for i in range(len(result["segments"])):
    segment = result["segments"][i]
    next_segment = (
        None if (i + 1) == len(result["segments"]) else result["segments"][i + 1]
    )
    # line = ""
    # for word in segment["words"]:
    #     line += formatted_word_with_length(word["word"], word["end"] - word["start"])
    print(words_to_ass_line(segment, next_segment))
