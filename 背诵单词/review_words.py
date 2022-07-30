#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
import os
import random
import re
import simplejson
from playsound import playsound
from boto3 import client
from contextlib import closing

__author__ = '__L1n__w@tch'

WORDS_FILE = r"D:\Code\Mac-Python-3.X\背诵单词\current_words.json"
CONDITION_REVIEW_TIME = 5
CONDITION_FORGET_TIME = 1


class Words:
    global FILE, CONDITION_REVIEW_TIME, CONDITION_FORGET_TIME

    def __init__(self):
        self.file_name = WORDS_FILE
        # update words
        all_words = self.generate_words()

        # get the words list for review
        self.review_words = self.filter_words(all_words)

    def get_words_to_review(self):
        review_words = self.review_words
        print(f"[*] Total words: {len(review_words)}")
        return review_words

    def generate_words(self):
        current_words = self.get_current_words()

        # update words from csv
        with open(r"D:\Code\Mac-Python-3.X\背诵单词\【2022-07】TOEFL && GRE - Word List - 生词.csv", encoding="utf8") as f:
            next(f)
            for i, line in enumerate(f):
                if str(line).startswith("2022"):
                    continue
                word, meaning, tips = re.findall("""(.+?),("?.+"?),(.*)""", line)[0]
                if word not in current_words:
                    current_words[word] = {"meaning": meaning, "tips": tips, "forget times": 0, "review times": 0}
                else:
                    current_words[word]["meaning"] = meaning
                    current_words[word]["tips"] = tips

        self.save_current_words(current_words)
        return current_words

    @staticmethod
    def filter_words(raw_words):
        result = dict()
        words = filter(
            lambda x: raw_words[x]["forget times"] >= CONDITION_FORGET_TIME or raw_words[x][
                "review times"] <= CONDITION_REVIEW_TIME, raw_words)
        for word in words:
            result[word] = raw_words[word]
        return result

    def get_current_words(self) -> dict:
        """
        get current words data base from json file
        :return:
        """
        file_name = self.file_name
        if not os.path.exists(file_name):
            return dict()
        with open(file_name, encoding="utf8") as f:
            return simplejson.load(f)

    def save_current_words(self, current_words):
        file_name = self.file_name
        with open(file_name, encoding="utf8", mode="w") as f:
            simplejson.dump(current_words, f, ensure_ascii=False)


class Checker:
    global WORDS_FILE

    def __init__(self):
        self.polly = client("polly", region_name="us-east-1")

    def review_words(self, words):
        random_word_list = list(words.keys())
        random.shuffle(random_word_list)
        length = len(random_word_list)
        for i, word in enumerate(random_word_list):
            print(f"[*] Total: {length}, Current: {i + 1}, Proceed: {(i + 1) / length:%}")
            print(f"[?] Do you know the meaning: ==== \033[1;36;40m{word}\033[0m ====")
            self.play_word_sound(word)
            response = input("Press enter: ")
            print(f"""[*] \033[1;31;40m{words[word]["meaning"]}\033[0m""")
            print(f"""[*] \033[1;31;40m{words[word]["tips"]} \033[0m""")
            if response == "n":
                self.update_forget_times(word)
            else:
                response = input("Enter: pass | n: forget --- ")
                if response == "n":
                    self.update_forget_times(word)
            self.update_review_times(word)
            print(f"{'=' * 60}")

    def update_word(self, word, field):
        with open(WORDS_FILE, "r", encoding="utf8") as f:
            words = simplejson.load(f)

        words[word][field] += 1

        with open(WORDS_FILE, "w", encoding="utf8") as f:
            simplejson.dump(words, f, ensure_ascii=False)

    def update_forget_times(self, forget_word):
        self.update_word(forget_word, "forget times")

    def update_review_times(self, forget_word):
        self.update_word(forget_word, "review times")

    def generate_word_mp3_by_aws_service(self, word):
        response = self.polly.synthesize_speech(Text=word, OutputFormat="mp3", VoiceId="Joanna")
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join("words_mp3", f"{word}.mp3")
                with open(output, "wb") as file:
                    file.write(stream.read())

    def play_word_sound(self, word):
        word_mp3_path = f"words_mp3/{word}.mp3"
        if not os.path.exists(word_mp3_path):
            self.generate_word_mp3_by_aws_service(word)
        for i in range(2):
            playsound(word_mp3_path)


if __name__ == "__main__":
    words = Words()
    checker = Checker()

    # do the review
    checker.review_words(words.get_words_to_review())
