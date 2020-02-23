# movie_screenshoter


Command line application using openCV to take given numbers of screenshots/frames from a movie file at random timeslot.
Checks whether taken screenshot is not blurry , if so takes another screenshot until a non-blurry frame is taken.

Allows single file conversion and conversion of all subtitle files in a folder/directory.

Usage:


    sub2text.py [-h] fileLocation [-d DEST] 

    Convert a single subtitle file OR Enter a folder path to convert all subtitles
    in it

    positional arguments:
    fileLocation          Complete FileDirectory/Folder or a single filename(Enclose it inside
                          quotations " ")

    optional arguments:
    -h, --help            show this help message and exit
    -d DEST, --dest DEST  File location for output files (Enclose it inside
                          quotations " ")
