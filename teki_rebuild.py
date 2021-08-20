import os

def _rebuild_requierement_resources():
    """
        This function regenerates the dependencies so that that the main script can  run properly
        in the event that certain files were deleted.

    :param
        There are no parameters.

     :return
        :rtype None
        There is no object, but a file is created that is placed in the main directory.
    """

    with open("requirement_resources.txt", mode="w+", encoding="utf-8") as resources:
        for path, subdirs, files in os.walk("app_program_resources"):
            for name in sorted(files):
                filename, file_extension = os.path.splitext(name)
                if file_extension != ".pyc":
                    resources.write(os.path.join(path, name)+"\n")
    print("The requirement_resources.txt file has been updated.")

if __name__ == "__main__":
    _rebuild_requierement_resources()