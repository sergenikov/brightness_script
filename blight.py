import sys, getopt
from subprocess import call

def increase_brightness(amount):
    #brightness = call(["cat", "/home/sergey/bin/BACKLIGHT"])
    f = open('/home/sergey/bin/BACKLIGHT', 'rw')
    value = f.readline()
    brightness = value.replace("\n", "")
    print ("current brighness %s; increasing brightness by %s" % (brightness, amount))

def reduce_brightness(amount):
    print ("reducing brightness by %s" % amount)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hu:d:")
    except getopt.GetoptError:
        print("Usage: -u to increase brightness; -d to reduce brightness")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("Usage: -u to increase brightness; -d to reduce brightness")
        elif opt in ("-u"):
            increase_brightness(arg)
        elif opt in ("-d"):
            reduce_brightness(arg)
    
# Execute program
if __name__ == "__main__":
    main(sys.argv[1:])
