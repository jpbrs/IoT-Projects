#!/Users/mac/anaconda3/bin/python

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Echo your input') 
    parser.add_argument('message',               
                        help='Message to echo')

    parser.add_argument('message2',              #Sempre que declaramos um argumento assim ele se torna obrigatorio 
                        help='Message2 to echo') 

    parser.add_argument('--twice', '-t',         
                        help='Do it twice',
                        action='store_true')

    parser.add_argument('--threetimes','-tt', help='Do it three times', action='store_true')

    parser.add_argument('--times',type=int, help='Do it N times. Ex : --times 3 => Do it 3 times')

    args = parser.parse_args()  

    print(args)
  
    if args.twice:
        print(args.message)  
        print(args.message)
    elif args.threetimes:
        print(args.message)  
        print(args.message)
        print(args.message)
    elif args.times:
        for i in range(args.times):
            print(args.message)

