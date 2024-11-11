from argparse import ArgumentParser
from . import web


def cli():
    # Initialize the parser object
    parser = ArgumentParser()

    # Initialize sub-parsers under the "subcommand"
    subparsers = parser.add_subparsers(dest="subcommand")

    # Generate the "web" subcommand
    subparser_web = subparsers.add_parser("web", help="Run the Cryonogen JSON REST API server")
    subparser_web.add_argument("--host", type=str, required=False, default="127.0.0.1")
    subparser_web.add_argument("--port", type=int, required=False, default=5000)
    subparser_web.add_argument("--db", type=str, required=False, default="datasheet/cryonogen.db")

    # Complete the activation of ArgumentParser
    args = parser.parse_args()

    # Conditional switching
    if args.subcommand == "web":
        web(db=args.db, host=args.host, port=args.port)
