import sys, getopt
import os

PER_MAX_SIZE = 48*1024*1024 # 48M
SPLIT_CHAR = '_'

def concat_filename(filename,idx,ext):
    return filename + SPLIT_CHAR + str(idx) + ext

def split_into_files(file):
    path,filename,ext = get_file_info(file)
    print("path: %s\nfilename: %s\next: %s"%(path,filename,ext))
    f = open(os.path.join(path, filename+ext),'rb')
    idx = 1
    while True:
        chunk = f.read(PER_MAX_SIZE)
        if not chunk:
            break
        fname = concat_filename(filename,idx,ext)
        print("split fname:",fname)
        nfile = open(os.path.join(path, fname),'wb')
        nfile.write(chunk)
        nfile.close()
        idx += 1
    f.close()

def concat_files(file):
    path,filename,ext = get_file_info(file)
    print("path: %s\nfilename: %s\next: %s"%(path,filename,ext))
    f = open(os.path.join(path, filename+ext),'wb')
    for i in range(50):
        fname = concat_filename(filename,i,ext)
        fname = os.path.join(path, fname)
        if os.path.exists(fname):
            print("concat fname:",fname)
            nfile = open(fname,'rb')
            f.write(nfile.read())
    f.close()

help = '''split file: python filesplit.py -s <originfile>

concat file: python filesplit.py -c <originfile>'''

def get_file_info(file):
    path = os.path.dirname(file)
    ext = os.path.splitext(file)[1]
    filename = os.path.basename(file)[:-len(ext)]
    return path, filename, ext

def main(argv):
    opts, args = getopt.getopt(argv, "-h-s:-c:", ["help","split=","concat="])
    # print(opts)
    for opt,arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        elif opt in ("-s", "--split"):
            if os.path.exists(arg):
                print("split file:", arg)
                split_into_files(arg)
            else:
                print("file not exists")
        elif opt in ("-c", "--concat"):
            print("concat file:", arg)
            concat_files(arg)

if __name__ == "__main__":
	main(sys.argv[1:])
