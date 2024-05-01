from typing import TypedDict, List

class SingleSegment(TypedDict):
    start: float
    end: float
    text: str


class TranscriptionResult(TypedDict):
    segments: List[SingleSegment]
    language: str


def parse_lrc(
    lrc_content: str, language: str = "en", offset: float = 0
) -> TranscriptionResult:
    lines = lrc_content.strip().split("\n")
    segments = []

    for i in range(len(lines) - 1):
        start_time = lines[i].split("]")[0].strip("[")
        end_time = lines[i + 1].split("]")[0].strip("[")
        text = lines[i].split("]")[1].strip()

        start_seconds = (
            int(start_time.split(":")[0]) * 60
            + float(start_time.split(":")[1])
            + offset
        )
        end_seconds = (
            int(end_time.split(":")[0]) * 60 + float(end_time.split(":")[1]) + offset
        )

        segments.append({"start": start_seconds, "end": end_seconds, "text": text})

    # Handle last line
    last_line = lines[-1]
    last_start_time = last_line.split("]")[0].strip("[")
    last_text = last_line.split("]")[1].strip()
    last_start_seconds = (
        int(last_start_time.split(":")[0]) * 60
        + float(last_start_time.split(":")[1])
        + offset
    )

    # Assuming the last segment duration is the same as the previous one
    last_segment_duration = (
        segments[-1]["end"] - segments[-1]["start"] if segments else 30
    )
    segments.append(
        {
            "start": last_start_seconds,
            "end": last_start_seconds + last_segment_duration,
            "text": last_text,
        }
    )

    return {"segments": segments, "language": language}


def parse_file(file_path: str, language: str = "ja", offset: float = 0):
    with open(file_path, "r", encoding="utf8") as file:
        return parse_lrc(file.read(), language, offset)
