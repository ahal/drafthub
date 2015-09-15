# -*- coding: utf-8 -*-

import argparse
import sys

from jinja2 import Environment, PackageLoader

def format_report(csv_path):
    env = Environment(extensions=['jinja2.ext.loopcontrols'],
                      loader=PackageLoader('fantasy_report', 'templates'))

    context = { 'players': [] }
    with open(csv_path, 'r') as f:
        first = True
        for line in f.readlines():
            line = line.decode('utf8', 'replace')
            tokens = [t.strip('"') for t in line.split(',')]

            if first:
                context['header'] = tokens
                first = False
            else:
                context['players'].append(tokens)

    template = env.get_template('report.html')
    return template.render(context)

def cli(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv',
                        dest='csv',
                        help='Path to csv file.')
    parser.add_argument('-o', '--output-file',
                        dest='output',
                        default='report.html',
                        help='Path to save report to.')
    args = parser.parse_args(args)
    content = format_report(args.csv)

    with open(args.output, 'w') as f:
        f.write(content.encode('utf8'))


if __name__ == '__main__':
    sys.exit(cli())
