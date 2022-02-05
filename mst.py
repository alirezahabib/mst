import argparse
import sys
sys.path.append('/')

from src.graph import parse_graph


def main(args):
    start, g = parse_graph(args.input)

    if args.kruskal:
        print('Starting Kruskal algorithm on graph . . .')
        out_g = g.kruskal()
    elif args.prim:
        print('Starting Prim algorithm on graph . . .')
        out_g = g.prim(start)
    else:
        raise ValueError('Please select an algorithm (-k/-p)')

    out_g.create_graphviz(attr_label_edge="WEIGHT", source=0).render(args.output, view=args.view)
    print('Output successfully generated at: ', args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Find the MST tree of the given graph using Kruskal or Prim algorithm"
    )

    parser.add_argument('-i', '--input',
                        help="provide input file",
                        type=str,
                        required=True
                        )

    parser.add_argument('-o', '--output',
                        help="output file name(s) prefix",
                        type=str,
                        default='out'
                        )

    parser.add_argument('-k', '--kruskal',
                        help="Finds MST using Kruskal algorithm.",
                        action="store_true",
                        )

    parser.add_argument('-p', '--prim',
                        help="Finds MST using Prim algorithm.",
                        action="store_true"
                        )

    parser.add_argument('-v', '--view',
                        help="View the output after generation.",
                        action="store_true"
                        )

    main(parser.parse_args())
