import glob, sys, re, os
from argparse import ArgumentParser
import cv2
import numpy

def parse_args():
    """
    Parse command line arguments and format arguments containing paths.
    :return: tuple of (ArgumentParser, Namespace). Parser itself and all arguments.
    """
    parser = ArgumentParser(description='Convert a single movie OR '
                                        'Enter a folder path to convert all movie folders in it ')
    parser.add_argument('fileLocation', help='Complete FileDirectory/Folder or a single filename(Enclose it inside quotations " ")',type=str)
    parser.add_argument('-d','--dest',help='File location for output files (Enclose it inside quotations " "), Default location is the video location',type=str)
    args = parser.parse_args()
    if isinstance(args.fileLocation, str):
        args.fileLocation = os.path.normpath(args.fileLocation.strip())
    return parser, args

def check_for_errors(filesource):
    """
    Check for errors, return corresponding
    error statement if any errors occurred.
    Otherwise return None.
    :param filename: str. file path.
    :param folder: str. Folder path containing moives.
    :return: str or NoneType. Error statement or None.
    """
    message = None
    if filesource != None:
        if not os.path.exists(filesource):
            message = 'Error: path does not exist.'
    elif filesource is None:
        message = 'Error: You must provide either filepathname or folder path.'
    else:
        message = None
    return message

def estimate_blur(image: numpy.array, threshold: int = 100):
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur_map = cv2.Laplacian(image, cv2.CV_64F)
    score = numpy.var(blur_map)
    return score, bool(score < threshold)

def singleFile(filename,screenshot_no,threshold=50.0):
    """
    Reads a single video file, extracts given no of screenshots from it and checks whether its blurry or not , then outputs it into jpg.
    :param filename: str, File path and filename
            screenshot_no: int, no of screenshots to take
    :return: None
    """
    output = os.path.dirname(filename)
    cap = cv2.VideoCapture(filename)
    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
    totalmsecs = cap.get(cv2.CAP_PROP_POS_MSEC)
    per = 90 // screenshot_no
    inc = per

    for j, i in enumerate(range(screenshot_no), start=1):

        cur_msec = totalmsecs * (per / 100)
        cap.set(cv2.CAP_PROP_POS_MSEC, cur_msec)
        success, image = cap.read()
        scor, boo = estimate_blur(image, threshold)
        if boo:
            while boo:
                cur_msec += 10000
                cap.set(cv2.CAP_PROP_POS_MSEC, cur_msec)
                success, image = cap.read()
                scor, boo = estimate_blur(image, threshold)
        outFile = os.path.join(output, f"frames{j}.jpg")
        cv2.imwrite(outFile, image)
        per += inc
    cap.release()

def convert_folder(folder):
    files = []
    for ext in ('*.mp4'):
        files.extend(glob.glob(os.path.join(folder, ext)))
    for f in files:
        read_convert_singleFile(f,location)


if __name__ == '__main__':
    parser, args = parse_args()
    src = args.fileLocation
    to_folder = select_destination(args)
    # checking for errors
    error = check_for_errors(src)
    if error:
        sys.exit(error)
    if os.path.isfile(src):
        singleFile(src,to_folder)
    elif os.path.isdir(src):
        convert_folder(src,to_folder)
    print("Conversion Completed!!")
