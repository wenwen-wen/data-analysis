import argparse
import json

IGNORE_LIST_IDS = [
    '0W32ILgOdSa85UhefBdZHSRxIh13', '3RUhaJWLuAUrDKU0uTYVeq5Ejl03', '9cF7zzfMKLace5zpVwwrL6fyMd23', 'BhTjFGDPwTV6P0TmJKAoI4ASVQ72', 'CNJXw0c5w9OzF8pmxENwDoiK4iE3', 'CYEMCTg8kLUJE8A8GoX2lpBdTBK2', 'DjRPaIdHoTb513mJRPrPbJzDwb73', 'IdeSrIyNHtXORarmV1U7Zc5j3Kx2', 'JUdpZPpUmfZeM7SnOlLY4QmNIbC2', 'Jfme6C3t88b7jIfvYmjI5pwEZyI2', 'LonvvQfZMngpESyg6iWKarMUOmF3', 'Pmht4EOFFbYXAavhtpuZlnKt0tZ2', 'Q06tXzUJPWRnaflv6RsHGnaaFHo2', 'QdrtobYfukU9LzaXIHM5iHvD4K82', 'R8JcS71ixJWnhEZOkSu5YodJXgl1', 'RAuVcqmKkmY3MzcO2DHLuIrfYJ83', 'XUwXij2S1ncWXgzuiIjWCzhE8lY2', 'Zk3eBeA5T6TrBCZ01KPDtILJEK62', 'bwfuvwf3kBRNvFwMhU1tOe3IMdf1', 'hcCDWu1Y1xYO2dwr0XGeDe8xYpy2', 'iu3IAXxnGUZz3SX0UOg51RlJPXI3', 'jQrSV87WQETcP8hDFX8wOKtTbdX2', 'mxShKu9BnHVQ9bipYiSpXZxqg1v2', 'nAsrRI6hcxQDp81JvNsVyKz1VsJ2', 'pvLyr7J33iSA2QVpdhrm6tQddgu1', 'qsAktgt4OKeNYy8QfgtHPunsypa2', 'rpYZFleO3gN7qm6XqXi0qm7N7gz2', 't0P50qc1gRao3ybPwWt4LpP0o9C2', 'y4mP3Qp9KGUOzpTcdWj7UEXEI0U2',
]

IGNORE_LIST_NAMES = [
    "王佳盈",
    "梁家萁",
    "王潔方",
    "黃崇豪",
    "林家瑋",
    "Jia-Yin Wang",
    "翁愷貽",
    "王尉穎",
    "宋宇倫",
    "江佳容",
    "葉承瑄",
    "yuclick",
    "林永婕",
    "蕭煥錫",
    "黃柏源",
    "李後璋",
    "管子涵",
    "應桂華",
    "温彥丞",
    "邱炳齡",
    "周育緯",
    "張逸哲",
    "Suar",
    "程式好難 我不會寫",
    "呂敏瑜",
    "施富耀",
    "李政穎",
    "李正豐",
]

# Run the following code to update the LIST_IDS if LIST_NAMES is updated
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List All Ignore Users")
    parser.add_argument("input_file", help="Path to the user file")
    args = parser.parse_args()

    if args.input_file.endswith('/'):
        args.input_file = args.input_file[:-1]

    with open(args.input_file, 'r') as file:
        users = json.load(file)
    print("==========Ignore Users==========")
    ignore_ids = [u["id"] for u in users if ("name" in u) and (u["name"] in IGNORE_LIST_NAMES)]
    print(ignore_ids)