from argparse import ArgumentParser
from moodlecrack import Crack
from search_sessid import find_sessid

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('baseurl', help='baseurl of moodle')
    parser.add_argument('-c', '--course', help='course name or course ID', required=False)
    parser.add_argument('-s', '--sessid', help='sessid', required=False)
    parser.add_argument('-w', '--worker', help='max worker', default=100)

    args = parser.parse_args()

    if args.sessid:
        sessid = args.sessid
    else:
        assert args.course, 'course name or sessid is required'
        print('searching sessid...')
        sessid = find_sessid(args.baseurl,args.course)
    print('sessid found:',sessid)
    max_worker = 100 
    crack = Crack(args.baseurl,sessid,max_worker)
    crack.run()