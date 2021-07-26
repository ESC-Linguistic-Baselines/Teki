try:
    """
    If the user has entered a valid selection, 
    then this range i.e. selection is extracted from the desired corpus. 
    The sentences are then parsed using the sentence_tokenizier located in the auxiliary_functions.
    It returns the parsed sentences and they are saved together with their respective id in a dictionary.
    """

    corpus_range_choice = corpus_range_choice.split()
    start, stop = int(corpus_range_choice[0]), int(corpus_range_choice[1])
    collective_results = dict()
    sentence_count = 0

    if corpus_choice == 1:

    for i in range(start, stop):
        # Extracting the selection and tokenizing it.
        corpus_text = soup.find("div", id=xml_tag_id[i]).getText().strip().split()
        results = sentence_tokenizer(corpus_text)
        collective_results[xml_tag_id[i]] = results

    #  Calculating the total amount of sentences
    for sentence in collective_results:
        sentence_count += len(collective_results[sentence])

    while True:
        user = input(
            f"The text has been parsed into {sentence_count} sentences. Would you like to tag or save the sentences (tag/save): ")

        if user == "tag":
            return collective_results
        elif user == "save":
            print("Please select the directory:")
            save_sentences(collective_results, file_finder())
            break
        else:
            print(f"{user} that is not a valid option.")

    if corpus_choice == 2 or 3:

        for i in range(start, stop):
            corpus_text = soup.find("post", {"xml:id": xml_tag_id[i]}).getText().strip().split()
            results = sentence_tokenizer(corpus_text)
            collective_results[xml_tag_id[i]] = results

        input(msg)
        return collective_results

except Exception as error:
    logging.exception(error)
    print(f"{corpus_range_choice} is not a valid selection. Please enter a valid choice.\n")














try:
    """
    If the user has entered a valid selection, 
    then this range i.e. selection is extracted from the desired corpus. 
    The sentences are then parsed using the sentence_tokenizier located in the auxiliary_functions.
    It returns the parsed sentences and they are saved together with their respective id in a dictionary.
    """

    corpus_range_choice = corpus_range_choice.split()
    start, stop = int(corpus_range_choice[0]), int(corpus_range_choice[1])
    collective_results = dict()
    sentence_count = 0

    if corpus_choice == 1:

    for i in range(start, stop):
        # Extracting the selection and tokenizing it.
        corpus_text = soup.find("div", id=xml_tag_id[i]).getText().strip().split()
        results = sentence_tokenizer(corpus_text)
        collective_results[xml_tag_id[i]] = results

    #  Calculating the total amount of sentences
    for sentence in collective_results:
        sentence_count += len(collective_results[sentence])

    while True:
        user = input(
            f"The text has been parsed into {sentence_count} sentences. Would you like to tag or save the sentences (tag/save): ")

        if user == "tag":
            return collective_results
        elif user == "save":
            print("Please select the directory:")
            save_sentences(collective_results, file_finder())
            break
        else:
            print(f"{user} that is not a valid option.")

    if corpus_choice == 2 or 3:

        for i in range(start, stop):
            corpus_text = soup.find("post", {"xml:id": xml_tag_id[i]}).getText().strip().split()
            results = sentence_tokenizer(corpus_text)
            collective_results[xml_tag_id[i]] = results

        input(msg)
        return collective_results

except Exception as error:
    logging.exception(error)
    print(f"{corpus_range_choice} is not a valid selection. Please enter a valid choice.\n")
