import argparse
import shutil
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly
import tempfile
import os
import uuid

def parse_args():
    parser = argparse.ArgumentParser(
        description="Manipulate a WAV file"
    )

    parser.add_argument(
        "input",
        type=str,
        help="Input WAV file path"
    )

    parser.add_argument(
        "output",
        type=str,
        help="Output WAV file path"
    )

    parser.add_argument(
        "-r", "--rate",
        type=int,
        required=False,
        help="Target sample rate (e.g. 16000, 44100)",
        default=None
    )

    parser.add_argument(
        "-g", "--gain",
        type=float,
        required=False,
        help="Target amplification (e.g. 2.0)",
        default=1.0
    )

    return parser.parse_args()


def resample_wav(in_path, target_sr):
    try:
        sr, data = wavfile.read(in_path)

        if target_sr == sr:
            print("file already has a sample rate of", sr)
            return

        if data.ndim > 1:
            data = data.mean(axis=1)

        gcd = np.gcd(sr, target_sr)
        up = target_sr // gcd
        down = sr // gcd

        y = resample_poly(data, up, down)

        if data.dtype == np.int16:
            y = np.clip(y, -32768, 32767).astype(np.int16)

        temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.wav")
        wavfile.write(temp_path, target_sr, y)

        return temp_path

    except Exception as ex:
        print(ex)
        return
    
def amplify(in_path, gain):
    sr, data = wavfile.read(in_path)
    original_dtype = data.dtype

    data = data.astype(np.float64)
    if original_dtype in [np.int16, np.int32]:
        data = data / np.iinfo(original_dtype).max

    amplified = np.clip(data * gain, -1.0, 1.0)
    amplified = (amplified * 32767).astype(np.int16)

    temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.wav")

    wavfile.write(temp_path, sr, amplified)

    return temp_path



def main():
    args = parse_args()

    temp_paths = []

    if args.rate != None:
        temp_path = resample_wav(
            args.input,
            args.rate
        )
        temp_paths.append(temp_path)

    if args.gain != 1.0:
        if temp_paths:
            input = temp_paths[-1]
        else:
            input = args.input

        temp_path = amplify(
            input,
            args.gain
        )
        temp_paths.append(temp_path)

    if temp_paths:
        final_file = temp_paths[-1] 
        shutil.copy(final_file, args.output)
    else:
        shutil.copy(args.input, args.output)

    for path in temp_paths:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    print("file saved at", args.output)





if __name__ == "__main__":
    main()
