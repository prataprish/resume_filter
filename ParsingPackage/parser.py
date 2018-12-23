import sys
from pdfminer.pdf_to_text import p2t
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.corpus import wordnet
import requests
import re

class Parsing:

    def skill_cmp(self,skill_set,pdf_clean):
        if not skill_set:
            return 0
        counter = 0
        clean_skill_set = []
        pdf_len = len(pdf_clean)
        for skill in skill_set:
            clean_skill_set.append(skill.lower())
        print(len(clean_skill_set))
        for skill in clean_skill_set:
            skill_len = len(re.findall(r"[\w']+", skill))
            for point in range(pdf_len):
                if pdf_clean[point:point+skill_len][0] == skill:
                    counter += 1
        return counter/len(clean_skill_set)

    def parse(self,skill_set,sec_set,path):
        counter = 0
        email = None
        name = None
        stops = stopwords.words('english')
        punctuations = string.punctuation
        pdf = p2t(path).lower()
        for word in pdf.split('\n'):
            for each in word.split(' '):
                each = each.strip()
                if name == None:
                    name = each
                if not email:
                    if re.match(r"[^@]+@[^@]+\.[^@]+", each):
                        email = each
                        break
        pdf_clean = nltk.tokenize.word_tokenize(pdf)
        pdf_clean = [word for word in pdf_clean if word not in stops if word not in punctuations]
        pdf_clean = list(set(pdf_clean))
        pdf_len = len(pdf_clean)
        primary = self.skill_cmp(skill_set,pdf_clean)
        secondary = self.skill_cmp(sec_set,pdf_clean)
        name = list(name)
        name = [str(name[0]).upper()] + name[1:]
        name = ''.join(name)

        return [primary,secondary,email,name]
