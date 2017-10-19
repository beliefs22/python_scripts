import os
import sys
import subprocess
import time
import argparse

parser = argparse.ArgumentParser(prog='Mp4 Video Converter', description='Converts videos of given file type to Mp4')
parser.add_argument('vin', help='directory to search videos for.')
parser.add_argument('ftype', help='video type to search for')
parser.add_argument('-vout', help='directory to save converted video too. If blank will save in vin')
parser.add_argument('-threads', choices=['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                    help='Number of threads to limit ffmpeg to')


def main():
    # TODO: can you use a try except block with argparse exceptions?
    try:
        args = parser.parse_args(sys.argv[1:])
        dir_to_search = args.vin
        file_type = args.ftype
        dir_to_save = args.vout
        threads = args.threads
        print_header()
        dir_to_search = get_folder_from_user(dir_to_search)
        # TODO: see if you can add directory checks into argparser
        if dir_to_search is None:  # confirm you got a directory
            print(dir_to_search)
            print("Sorry we can't search that location.")
            sys.exit(1)
        if dir_to_save:  # confirm you got a valid directory to save if you didn't get None from argparse
            dir_to_save = get_folder_from_user(dir_to_save)
            if dir_to_save is None:
                print("Sorry we can't save files there")
                sys.exit(1)

        if not file_type.strip():  # confirm you got a valid file type and not an empty line
            print("You did not provide a file type!")
            sys.exit(1)

        print("Searching {} for {} type files".format(dir_to_search, file_type))
        matches = search_folders(dir_to_search, file_type)
        for video in matches:
            print(video)
            video_name = os.path.basename(video)
            dir_to_search = os.path.dirname(video)
            start = time.time()
            # Both directory and threads will be done if not given when function was called
            convert_video_to_mp4(video_name, file_type, dir_to_search, dir_to_save=dir_to_save, threads=threads)
            end = time.time()
            print("Converted in {} minutes".format((end - start) / 60))
    except Exception as e:
        print("Sorry something went wrong")
        print(e)
        sys.exit(1)


def print_header():
    print('-------------------------------------')
    print('           Convert Video to Mp4')
    print('-------------------------------------')


def get_folder_from_user(folder):
    """
    Check that the given pathway is a directory
    :param folder: pathway to check
    :return: None if folder if not a director. The absolute path of the folder if it is a directory
    """
    if not folder or not folder.strip():
        return None

    if not os.path.isdir(folder):
        return None

    return os.path.abspath(folder)


def search_folders(folder, file_type):
    """
    Search a folder for files of the given file extention
    :param folder: directory to search
    :param file_type: file extention to search for
    :yield: files located in the directory that match the extention
    """
    print("Searching {} for {} type files".format(folder, file_type))
    items = os.listdir(folder)

    for item in items:
        full_item = os.path.join(folder, item)
        if os.path.isdir(full_item):
            yield from search_folders(full_item, file_type)
        else:
            yield from search_file(full_item, file_type)


def search_file(filename, file_type):
    """
    Search files for files that end with the given file type extension and return the path with the extension removed
    :param filename: file to search
    :param file_type: file type that matches
    :yield: the absolute path of the file name with the file type extension removed
    """
    if filename.endswith(file_type):
        yield filename


def convert_video_to_mp4(old_video, file_type_to_convert, input_folder, dir_to_save=None, threads=None):
    """

    :param old_video: name of video file
    :param file_type_to_convert: video extension converting from
    :param input_folder: directory the video was located in
    :param dir_to_save: directory to save the video to. If none will save in input_folder directory
    :param threads: number of threads to limit ffmpeg to. If blank will use all threads (ffmpeg default)
    :return:
    """
    old_video_path = os.path.join(input_folder, old_video)
    if dir_to_save is not None:
        new_video_path = os.path.join(dir_to_save, old_video.replace(file_type_to_convert, "mp4"))
    else:  # save in current directory
        new_video_path = old_video_path.replace(file_type_to_convert, "mp4")
    print("converting {}".format(old_video))
    if not os.path.isfile(old_video_path):
        print("{} is not a file".format(old_video_path))
        return
    if threads is not None:
        subprocess.run(['ffmpeg', '-i',
                        old_video_path, "-strict", "-2", "-threads", threads, new_video_path], stdin=subprocess.PIPE,
                       stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    else:
        subprocess.run(['ffmpeg', '-i',
                        old_video_path, "-strict", "-2", new_video_path], stdin=subprocess.PIPE,
                   stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    print("Finished converting {} saved at {}".format(old_video, new_video_path))


def find_and_convert_media_files(dir_to_search, file_type, dir_to_save=None, threads=None):
    """
    Locates media files or the given type in the given dir_to_search and converts them to mp4 format
    :param threads: number of threads to limit ffmpeg to. If blank will use all threads (ffmpeg default)
    :param dir_to_search: directory that contains the media files
    :param file_type: file type to search for i.e. avi
    :param dir_to_save: directory to save files to. If not given, will save in files current directory
    :return:
    """
    # TODO: Add options for different file types this can serve as the skelton for each type
    print_header()
    dir_to_search = dir_to_search
    dir_to_search = get_folder_from_user(dir_to_search)

    if dir_to_search is None:  # confirm you got a directory
        print(dir_to_search)
        print("Sorry we can't search that location.")
        sys.exit(1)
    if dir_to_save is not None:  # confirm you got a valid directory to save if you didn't get None from argparse
        dir_to_save = get_folder_from_user(dir_to_save)
        if dir_to_save is None:
            print("Sorry we can't save files there")
            sys.exit(1)

    if not file_type.strip():  # confirm you got a valid file type and not an empty line
        print("You did not provide a file type!")
        sys.exit(1)

    print("Searching {} for {} type files".format(dir_to_search, file_type))
    matches = search_folders(dir_to_search, file_type)
    for video in matches:
        print(video)
        video_name = os.path.basename(video)
        dir_to_search = os.path.dirname(video)
        start = time.time()
        # Both directory and threads will be done if not given when function was called
        convert_video_to_mp4(video_name, file_type, dir_to_search, dir_to_save=dir_to_save, threads=threads)
        end = time.time()
        print("Converted in {} minutes".format((end - start) / 60))


if __name__ == '__main__':
    main()
