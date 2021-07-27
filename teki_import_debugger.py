import pickle

file = r"C:\Users\chris\Desktop\Bachleorarbeit\pickle_data.pickle"
load = pickle.load(open(file, "rb"))

class DiscourseAnalysis:
    """

    """

    class PosSyntacticalAnalysis:
        """
        This class contains various functions that rely on the syntactical and
        parts of speech tags to analyze the sentences and assign them a feature.

        """

        def __init__(self, sub_sentences):
            self.sub_sentences = sub_sentences

        def sentence_reconstruction(self):
            """

            :return:
            """

            sentence = " ".join([word[0] for word in self.sub_sentences])
            word_count = len(self.sub_sentences)

            return word_count, sentence

        def part_of_speech(self):
            """

            :return:
            """
            pos = [word[1] for word in self.sub_sentences]
            return pos

        def pos_grams(self):
            """

            :return:
            """

            gram_count = dict()

            pos = self.part_of_speech()
            for i in range(len(pos) - 1):
                gram=pos[i], pos[i+1]

                gram_count[gram] = gram_count.get(gram,0)+1

            for i in range(len(pos)):
                gram = pos[i]
                gram_count[gram] = gram_count.get(gram, 0) + 1

            return gram_count

        def feature_assignment(self):
            """

            :return:
            """

            sentence = self.sentence_reconstruction()[1]
            sentence_length = self.sentence_reconstruction()[0]
            pos = self.part_of_speech()
            gram_count = self.pos_grams()

            noun_count = gram_count.get("NOUN",0)+gram_count.get("PROPN",0)

            verb_count = gram_count.get("VERB", 0)

            instance_one = (
                    sentence_length < 8,
                    noun_count > verb_count,
                    "a" == "b"
                    )

            if instance_one.count(True) > instance_one.count(False):
                return "ORAL"

            else:
                return "UNKNOWN"

    class TokenAnalysis:

        def __init__(self, sub_sentences):
            self.sub_sentences = sub_sentences

        def reconstruct(self):
            sentence = " ".join([word[0] for word in self.sub_sentences])
            return sentence,  len(self.sub_sentences)

for i in load:
    check = DiscourseAnalysis.PosSyntacticalAnalysis(load[i])
    print(i, load[i], check.feature_assignment())