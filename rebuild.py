import os
def _rebuild_requierement_resources():
    """
        This function generates the dependencies that that the main script needs to run properly.

    :param str
        'error_log': The name of the log file to be cleared.

     :return
        :rtype None
        There is no object, but a file is created that is placed in the main directory.py
    """

    with open("requirement_resources.txt", mode="w+", encoding="utf-8") as resources:

        for path, subdirs, files in os.walk("app_resources"):
            for name in files:
                resources.write(os.path.join(path, name)+"\n")
    print("The app resource directory.py file has been updated.")
_rebuild_requierement_resources()