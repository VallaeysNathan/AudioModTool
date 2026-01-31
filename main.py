import argparse
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly


def parse_args():
    parser = argparse.ArgumentParser(
        description="Resample a WAV file using polyphase FIR filtering"
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
        required=True,
        help="Target sample rate (e.g. 16000, 44100)"
    )

    return parser.parse_args()


def resample_wav(in_path, out_path, target_sr):
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

        wavfile.write(out_path, target_sr, y)
        print("file saved at", out_path)

    except Exception as ex:
        print(ex)
        return


def main():
    args = parse_args()

    resample_wav(
        args.input,
        args.output,
        args.rate
    )


if __name__ == "__main__":
    main()
