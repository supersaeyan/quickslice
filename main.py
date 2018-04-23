from cct.build import build
from cct.slice import slice
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    
    build_parser = subparsers.add_parser('build')
    build_parser.add_argument('path', type=str)
    build_parser.add_argument('--size', type=int, nargs='+',default=[128, 128, 128])
    
    slice_parser = subparsers.add_parser('slice')
    slice_parser.add_argument('cct', type=str)
    slice_parser.add_argument('-x', '--x', type=float)
    slice_parser.add_argument('-y', '--y', type=float)
    slice_parser.add_argument('-z', '--z', type=float)
    slice_parser.add_argument('-t', '--threshold', type=int, nargs='+',default=[0, 255])
    slice_parser.add_argument('-c', '--colormap', type=str)
    
    args = parser.parse_args()
    if args.command == 'build':
        if build(args.path, args.size):
            sys.exit('Finished building CCT File')
        sys.exit('Failed to generate CCT File')
    
    elif args.command == 'slice':
        if (args.x and args.y) or (args.y and args.z) or (args.z and args.x):
            sys.exit('Only one of x, y, or z allowed')
        plane = None
        if isinstance(args.x, (int, float)) and args.x >= 0 and args.x <= 1:
            plane = '{}{}'.format('x', args.x)
        elif isinstance(args.y, (int, float)) and args.y >= 0 and args.y <= 1:
            plane = '{}{}'.format('y', args.y)
        elif isinstance(args.z, (int, float)) and args.z >= 0 and args.z <= 1:
            plane = '{}{}'.format('z', args.z)
        if not plane:
            sys.exit('Enter a number between range 0-1.00 for x,y, or z')
        done, message = slice(args.cct, plane, args.threshold, args.colormap)
        sys.exit(message)
    sys.exit('Unknown command')
    
    