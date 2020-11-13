import argparse
from mednum.data import download_geojson as dgj
from mednum.data import download_insee as dins


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "choix",
        help="Choix",
        choices=[
            "all",
            "download_geojson",
            "download_insee"
        ],
    )

    args = parser.parse_args()

    if args.choix == "download_geojson":
        dgj.generer()
    elif args.choix == "download_insee":
        dins.generer()
    else:
        dgj.generer()
        dins.generer()
