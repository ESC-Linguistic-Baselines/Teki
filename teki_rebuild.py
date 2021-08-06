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
        for path, subdirs, files in os.walk("app_core_resources"):
            for name in files:
                resources.write(os.path.join(path, name)+"\n")
    print("The requirement_resources.txt file has been updated.")

def feature_extraction():
    """
    This function is for extracting features based on their tags from the respective corpora.

    :param
        There are no parameters as it has access to the necessary data which

     :return
        :rtype None
        The data is written to the respective files
    """

    document = r"C:\Users\chris\Desktop\Bachleorarbeit\app_resources\app_dev\dev_files\sms_0_29507.xml"
    outfile = "emoticons.csv"
    corpus = "SMS"
    text = ""
    # SMS files
    with open(document, mode="r", encoding="utf-8") as in_file, open(outfile, mode="a+", encoding="utf-8",
                                                                     newline="") as out_file:
        soup = bs4.BeautifulSoup(in_file, "lxml")
        fieldnames = "token", "type", "token_tag"
        csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        tag_results = dict()

        if corpus == "SMS":
            for element in soup.find_all("distinct", type="emoticon"):
                emoticon = element.getText()
                tag_results[emoticon] = tag_results.get(emoticon, 0) + 1

            for emo in sorted(tag_results, key=tag_results.get, reverse=False):
                csv_writer.writerow({
                    "token": emo,
                    "type": "emoticon",
                    "token_tag": "sms_0_29507",
                })

        # Ebay Corpus
        else:
            tag = ("bon", "ego", "sty", "stn", "pre", "vst", "emo", "enc",
                   "imp", "att", "acc", "ann", "con", "info", "lex", "ort", "slo", "syn")

            for t in sorted(tag):
                types = {" ".join(element.getText().split()) for element in soup.find_all(t)}
                for element in types:
                    print(bool(types))
                    csv_writer.writerow({
                        "token": element,
                        "type": t,
                        "token_tag": text
                    })

if __name__ == "__main__":
    _rebuild_requierement_resources()