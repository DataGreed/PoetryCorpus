# -*- coding: utf-8 -*-
# Автор: Гусев Илья
# Описание: Модуль фильтров языковой модели по разным признакам.

from collections import defaultdict

from poetry.apps.corpus.scripts.rhymes.rhymes import Rhymes


class Filter(object):
    """
    Фильтр языковой модели.
    """
    def filter_word(self, word):
        raise NotImplementedError()

    def filter_model(self, model, vocabulary):
        """
        Фильтрация языковой модели.
        :param model: изначальная модель.
        :param vocabulary: словарь
        :return: модель после фильтрации и нормирования.
        """
        for i in range(len(model)):
            if not self.filter_word(vocabulary.get_word(i)):
                model[i] = 0.0
        s = sum(model)
        for i in range(len(model)):
            model[i] = model[i]/s if s != 0.0 else 0.0
        return model

    def filter_words(self, words):
        """
        Фильтрация набора слов
        :param words: слова.
        :return: слова после фильтрации.
        """
        return [word for word in words if self.filter_word(word)]


class MetreFilter(Filter):
    """
    Фильтр по шаблону метра.
    """
    def __init__(self, metre_pattern):
        self.metre_pattern = metre_pattern
        self.position = len(metre_pattern) - 1

    def filter_word(self, word):
        """
        Фильтрация слова по метру в текущей позиции.
        :param word: слово (Word).
        :return: подходит слово или нет.
        """
        syllables_count = len(word.syllables)
        if syllables_count > self.position + 1:
            return False
        for i in range(syllables_count):
            syllable = word.syllables[i]
            syllable_number = self.position - syllables_count + i + 1
            if syllables_count >= 2 and syllable.accent == -1 and self.metre_pattern[syllable_number] == "+":
                for j in range(syllables_count):
                    other_syllable = word.syllables[j]
                    other_syllable_number = other_syllable.number - syllable.number + syllable_number
                    if i != j and other_syllable.accent != -1 and self.metre_pattern[other_syllable_number] == "-":
                        return False
        return True

    def pass_word(self, word):
        """
        Сдвинуть позицию в шаблоне метра на слово.
        :param word: слово (Word).
        """
        self.position -= len(word.syllables)

    def reset(self):
        """
        Сброс позиции в шаблоне.
        """
        self.position = len(self.metre_pattern) - 1


class RhymeFilter(Filter):
    """
    Фильтр по шаблону рифмы.
    """
    def __init__(self, rhyme_pattern, letters_to_rhymes=None):
        self.rhyme_pattern = rhyme_pattern
        self.position = len(self.rhyme_pattern) - 1
        self.letters_to_rhymes = defaultdict(set)
        if letters_to_rhymes is not None:
            for letter, words in letters_to_rhymes.items():
                for word in words:
                    self.letters_to_rhymes[letter].add(word)

    def pass_word(self, word):
        """
        Сдвинуть позицию в шаблоне рифмы на строчку.
        :param word: рифмующееся слово (Word).
        """
        self.letters_to_rhymes[self.rhyme_pattern[self.position]].add(word)
        self.position -= 1

    def filter_word(self, word):
        """
        Фильтрация слова по рифме в текущей позиции.
        :param word: слово (Word).
        :return: подходит слово или нет.
        """
        if len(word.syllables) <= 1:
            return False
        if len(self.letters_to_rhymes[self.rhyme_pattern[self.position]]) == 0:
            return True
        first_word = list(self.letters_to_rhymes[self.rhyme_pattern[self.position]])[0]

        is_rhyme = Rhymes.is_rhyme(first_word, word, score_border=5, syllable_number_border=2) and \
            first_word.text != word.text
        return is_rhyme
