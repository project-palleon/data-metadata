import os
import subprocess

from palleon.data_plugin import DataPlugin


def extract_metadata(path):
    raw_output = subprocess.run(["exiftool", path], capture_output=True).stdout.decode().splitlines()

    # parse output
    raw_output = [e.split(":", 1) for e in raw_output]
    raw_output = [[e[0].strip(), e[1].strip()] for e in raw_output]

    # interesting keys
    keys = ['File Name', 'File Size', 'MIME Type', 'Major Brand', 'Create Date', 'Modify Date', 'Duration', 'Video Frame Rate',
            'Image Size', 'Avg Bitrate', 'Rotation']

    data = {}

    for key, value in raw_output:
        if key in keys:
            if value == "0000:00:00 00:00:00":
                continue
            data[key] = value

    return data


# custom defined environment variables
path = os.environ["file_path"]
metadata = extract_metadata(path)

input_sources = os.environ["input_sources"].split(",")


class MetadataPlugin(DataPlugin):
    def __init__(self):
        super().__init__(image=False)

    def image_received_hook(self, data, image, input_source, other_metadata):
        if input_source in input_sources:
            return metadata
        return {}


if __name__ == "__main__":
    MetadataPlugin().run()
