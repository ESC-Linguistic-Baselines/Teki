import re
a = r"C:\Users\chris\Desktop\B.A\Teki\app_program_resources\app_corpora\app_dev\results\scoring\wikiconflits_0_53_sentences_scoring_results.csv"
file =open(a,
           mode="r", encoding="utf-8").read()

print(file.count("LIT"))
print(file.count("ORAL"))