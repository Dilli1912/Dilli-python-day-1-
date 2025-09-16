import os
import glob
import json
import argparse
import pandas as pd


def load_json_with_encodings(path, encodings=['utf-8', 'utf-16', 'ascii', 'latin1']):
    last_exc = None
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as f:
                return json.load(f)
        except UnicodeDecodeError as e:
            last_exc = e
        except Exception as e:
            last_exc = e
            break
    raise last_exc


def load_and_flatten(path, sep='.'):
    """Load JSON file, trying multiple encodings, and flatten."""
    obj = load_json_with_encodings(path)
    if isinstance(obj, list):
        obj = {'_root': obj}
    df = pd.json_normalize(obj, sep=sep)
    return df


def serialize_lists_and_dicts(df):
    """
    Convert list/dict cells into strings so that each file remains a single row.
    - If a list contains only primitives, join with '|' for readability.
    - Otherwise JSON-dump the list/dict.
    """
    def serialize(v):
        if isinstance(v, list):
            if all(isinstance(i, (str, int, float, bool)) for i in v):
                return '|'.join(map(str, v))
            else:
                return json.dumps(v, ensure_ascii=False)
        if isinstance(v, dict):
            return json.dumps(v, ensure_ascii=False)
        return v

    
    return df.applymap(serialize)

def main(input_dir, output_csv, sep='.'):
    files = sorted(glob.glob(os.path.join(input_dir, '*.json')))
    if not files:
        print(f"No JSON files found in {input_dir}")
        return

    frames = []
    for p in files:
        try:
            df = load_and_flatten(p, sep=sep)
            
            df['__source_file'] = os.path.basename(p)
            frames.append(df)
        except Exception as e:
            print(f"Error reading {p}: {e}")

    
    combined = pd.concat(frames, ignore_index=True, sort=False)
    combined = serialize_lists_and_dicts(combined)

    
    outdir = os.path.dirname(output_csv) or '.'
    os.makedirs(outdir, exist_ok=True)
    combined.to_csv(output_csv, index=False)
    print(f"Wrote {len(combined)} rows to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", default="data", help="Input directory containing .json files")
    parser.add_argument("--output", "-o", default="output/tickets.csv", help="Output CSV path")
    parser.add_argument("--sep", default=".", help="Separator to use when flattening nested keys (default='.')")
    args = parser.parse_args()
    main(args.input, args.output, sep=args.sep)
