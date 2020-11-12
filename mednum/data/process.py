import argparse
from mednum.data import download_geojson as dgj


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "choix",
        help="Choix",
        choices=[
            "all",
            "download_geojson",
        ],
    )

    args = parser.parse_args()

    if args.choix == "download_geojson":
        dgj.generer()
    else:
        dgj.generer()
