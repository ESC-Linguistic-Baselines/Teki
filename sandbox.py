import bs4
from bs4 import BeautifulSoup


document=r"C:\Users\chris\iCloudDrive\Documents\Academic Documents\RUB UNI\0 - Files\Lingustik PL\B.A\Bachleorarbeit\app_resources\app_dev\dev_files\wikiconflits_0_79.xml"
with open(document, mode="r", encoding="utf-8") as file:
    soup = bs4.BeautifulSoup(file, "lxml")

def extract_text():
    """
    This function extracts the entries from the respective .xml.
    """

    while True:
        corpus = "eBay", "SMS", "Wikiconflit"
        for num, cor in enumerate(corpus, start=1):
            print(num, cor)

        corpus_search = input("\nFrom which corpus are you extracting the message?")

        xml_tag_id = list()

        if corpus_search == "1":
            # eBay listing
            for tag in soup.select("div[id]"):
                xml_tag_id.append(tag["id"])

        elif corpus_search in ("2", "3"):
            # SMS, Wikiconflict
            for tag in soup.select("post"):
                xml_tag_id.append(tag["xml:id"])
        else:
            print("You did not enter a valid corpus number.\n")
        print(xml_tag_id[1])
        while True:
            print(f"There are {len(xml_tag_id)} tags. Please enter a number from 0 - {len(xml_tag_id)}.")
            corpus_tag_choice = input("Please enter a valid tag: ")

            try:
                choice = int(corpus_tag_choice)
                print(corpus_search)
                if corpus_search == "1":
                    corpus_text = soup.find("div", id=xml_tag_id[choice]).getText().strip().split()

                else:
                    print(xml_tag_id[choice])
                    corpus_text = soup.find("post", {"xml:id": xml_tag_id[choice]}).getText().strip().split()

                return {xml_tag_id[choice]: " ".join(corpus_text)}

            except:
                print(f"{corpus_tag_choice} is not a valid choice. Please try again.\n")


extract_text()