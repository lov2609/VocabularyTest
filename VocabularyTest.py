import random
import toga
import emoji
import ast
from re import search
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER


class VocabularyTest(toga.App):

    def startup(self):

        my_file = open(toga.App.app.paths.app / "resources/{0}.txt".format('vocabulary'), 'r', encoding='utf-8')
        self.Vocabulary = ast.literal_eval(my_file.read())
        my_file.close()
        my_file = open(toga.App.app.paths.app / "resources/{0}.txt".format('total_stats'), 'r', encoding='utf-8')
        self.total_stats = ast.literal_eval(my_file.read())
        my_file.close()

        self.key_list = list(self.Vocabulary.keys())
        self.value_list = list(self.Vocabulary.values())
        self.stats = list(self.total_stats.values())
        self.errors_total = self.stats[0]
        self.answers_total = self.stats[1]
        self.rating_total = self.stats[2]
        self.words_total = len(self.key_list)
        self.answers_session = 0
        self.words_session = 0
        self.errors_session = 0
        self.skip_session = 0
        self.correct_session = 0

        self.main_box = toga.Box(style=Pack(direction=COLUMN, background_color='#000000'))
        self.box_main = toga.Box(style=Pack(direction=COLUMN))
        self.box_add = toga.Box(style=Pack(direction=COLUMN))
        self.box_stat = toga.Box(style=Pack(direction=COLUMN))

        self.switch_language = toga.Switch('Test: Rus-Eng', on_change=self.change_mode, style=Pack(font_size=20,
                                            background_color='#C0C0C0', color='#FFFFFF', height=40))
        self.word_place = toga.MultilineTextInput(readonly=True, style=Pack(font_size=16, background_color='#808080',
                                                             text_align=CENTER, color='#FFFFFF'))
        self.translate_place = toga.MultilineTextInput(placeholder='Translation', style=Pack(font_size=16,
                                                        background_color='#808080', text_align=CENTER, color='#FFFFFF'))
        self.check_button = toga.Button('Check ' + emoji.emojize(":red_question_mark:"), on_press=self.check_answer,
                                        style=Pack(flex=1, background_color='#808080', color='#FFFFFF'))
        self.result_button = toga.Button('Show result ' + emoji.emojize(":bomb:"), on_press=self.show_result,
                                         style=Pack(flex=1, background_color='#808080', color='#FFFFFF'))
        self.word_stat_place = toga.TextInput(readonly=True, style=Pack(font_size=16, text_align=CENTER, color='#FFFFFF'))
        self.next_button = toga.Button('Next word ' + emoji.emojize(":right_arrow:"), on_press=self.next_word, enabled=False,
                                       style=Pack(flex=1, background_color='#808080', color='#FFFFFF'))
        self.stat_button = toga.Button('Stats ' + emoji.emojize(":1st_place_medal:"), on_press=self.show_stat,
                                       style=Pack(flex=1, background_color='#808080', color='#FFFFFF'))
        self.add_button = toga.Button('Add a word ' + emoji.emojize(":scroll:"), on_press=self.show_add,
                                      style=Pack(flex=1, background_color='#808080', color='#FFFFFF'))
        self.box_main.add(self.switch_language)
        self.box_main.add(self.word_place)
        self.box_main.add(self.translate_place)
        self.box_main.add(self.check_button)
        self.box_main.add(self.result_button)
        self.box_main.add(self.word_stat_place)
        self.box_main.add(self.next_button)
        self.box_main.add(self.stat_button)
        self.box_main.add(self.add_button)

        self.label_stat = toga.Label('Statistics', style=Pack(font_size=16, text_align=CENTER, color='#FFFFFF'))
        self.words_total_count = toga.TextInput(value='Words in total: ' + '{0}'.format(self.words_total), readonly=True,
                                                style=Pack(font_size=16, text_align=CENTER, color='#FFFFFF'))
        self.words_session_count = toga.TextInput(value='Words per session: ' + '{0}'.format(self.words_session),
                                                  readonly=True,
                                                  style=Pack(font_size=16, text_align=CENTER, color='#FFFFFF'))
        self.errors_total_count = toga.TextInput(value='Mistakes in total: ' + '{0}'.format(self.errors_total), readonly=True,
                                                 style=Pack(font_size=16, text_align=CENTER, color='#FFFFFF'))
        self.errors_session_count = toga.TextInput(value='Mistakes per session: ' + '0', readonly=True,
                                                   style=Pack(font_size=16, text_align=CENTER, color='#FFFFFF'))
        self.skip_session_count = toga.TextInput(value='Skips per session: ' + '0', readonly=True,
                                                 style=Pack(font_size=16, text_align=CENTER, color='#FFFFFF'))
        self.rating_total_count = toga.TextInput(value='Total rating: ' + '{0}%'.format(self.rating_total), readonly=True,
                                                 style=Pack(font_size=16, text_align=CENTER, color='#FFFFFF'))
        self.rating_session_count = toga.TextInput(value='Session rating: ' + '0%', readonly=True,
                                                   style=Pack(font_size=16, text_align=CENTER, color='#FFFFFF'))
        self.stat_back_button = toga.Button('Back' + emoji.emojize(":left_arrow:"), on_press=self.back_stat,
                                            style=Pack(flex=1, background_color='#000080', color='#FFFFFF'))
        self.box_stat.add(self.label_stat)
        self.box_stat.add(self.words_session_count)
        self.box_stat.add(self.errors_session_count)
        self.box_stat.add(self.skip_session_count)
        self.box_stat.add(self.rating_session_count)
        self.box_stat.add(self.words_total_count)
        self.box_stat.add(self.errors_total_count)
        self.box_stat.add(self.rating_total_count)
        self.box_stat.add(self.stat_back_button)

        self.label_add = toga.Label('Add a new word', style=Pack(font_size=16, text_align=CENTER, color='#FFFFFF'))
        self.eng_word_place = toga.MultilineTextInput(placeholder='Word in English',
                                                      style=Pack(font_size=16, text_align=CENTER, color='#FFFFFF'))
        self.rus_word_place = toga.MultilineTextInput(placeholder='Translate in Russian',
                                                      style=Pack(font_size=16, text_align=CENTER, color='#FFFFFF'))
        self.add_word_button = toga.Button('Add' + emoji.emojize(":up_arrow:"), on_press=self.add_word,
                                           style=Pack(flex=1, background_color='#808080', color='#FFFFFF'))
        self.add_back_button = toga.Button('Back' + emoji.emojize(":left_arrow:"), on_press=self.back_add,
                                           style=Pack(flex=1, background_color='#000080', color='#FFFFFF'))
        self.box_add.add(self.label_add)
        self.box_add.add(self.eng_word_place)
        self.box_add.add(self.rus_word_place)
        self.box_add.add(self.add_word_button)
        self.box_add.add(self.add_back_button)

        self.main_box.add(self.box_main)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.show_word()
        self.main_window.show()

    def show_stat(self, a):
        self.main_box.remove(self.box_main)
        self.main_box.add(self.box_stat)

    def back_stat(self, a):
        self.main_box.remove(self.box_stat)
        self.main_box.add(self.box_main)

    def show_add(self, a):
        self.main_box.remove(self.box_main)
        self.main_box.add(self.box_add)

    def back_add(self, a):
        self.main_box.remove(self.box_add)
        self.main_box.add(self.box_main)

    def show_word(self):
        global ind
        ind = random.randint(0, len(self.key_list) - 1)
        word_stat_file = open(toga.App.app.paths.app / "resources/{0}.txt".format('word_stats'), 'r', encoding='utf-8')
        self.word_stats_data = ast.literal_eval(word_stat_file.read())
        word_stat_file.close()
        self.word_stats_values = list(self.word_stats_data.values())
        self.word_stats_keys = list(self.word_stats_data.keys())
        self.word_stats = self.word_stats_values[ind]
        self.word_stat_place.value = 'This word (O / X / S): ' + '{0} / {0} / {0}'.format(self.word_stats[0], self.word_stats[1], self.word_stats[2])
        if self.switch_language.value is True:
            word = self.key_list[ind]
            self.word_place.value = word
        else:
            word = self.value_list[ind]
            self.word_place.value = word

    def change_mode(self, a):
        if self.switch_language.value is True:
            self.switch_language.text = 'Test: Eng-Rus'
        else:
            self.switch_language.text = 'Test: Rus-Eng'
        self.next_word(1)

    def check_answer(self, a):
        stat_file = open(toga.App.app.paths.app / "resources/{0}.txt".format('total_stats'), 'w', encoding='utf-8')
        answer = self.translate_place.value
        self.answers_session += 1
        self.answers_total += 1
        self.total_stats['Answers total'] = self.answers_total
        word_stat_file = open(toga.App.app.paths.app / "resources/{0}.txt".format('word_stats'), 'w', encoding='utf-8')
        if self.switch_language.value is True:
            true_answer = self.value_list[ind]
        else:
            true_answer = self.key_list[ind]
        if search(answer.lower(), true_answer.lower()) and self.translate_place.value != '':
            self.check_button.text = 'Correct! ' + emoji.emojize(":check_mark:")
            self.check_button.style.background_color = '#98FB98'
            self.word_stats[0] += 1
            self.next_button.enabled = True
            self.result_button.enabled = False
        else:
            self.check_button.text = 'Wrong! ' + emoji.emojize(":cross_mark:")
            self.check_button.style.background_color = '#FF4500'
            self.word_stats[1] += 1
            self.errors_session += 1
            self.errors_session_count.value = 'Mistakes per session: ' + '{0}'.format(self.errors_session)
            self.errors_total += 1
            self.errors_total_count.value = 'Mistakes in total: ' + '{0}'.format(self.errors_total)
            self.total_stats['Errors total'] = self.errors_total
        self.rating_session = round((self.answers_session - self.errors_session) / self.answers_session * 100)
        self.rating_session_count.value = 'Session rating: ' + '{0}%'.format(self.rating_session)
        self.rating_total = round((self.answers_total - self.errors_total) / self.answers_total * 100)
        self.rating_total_count.value = 'Total rating: ' + '{0}%'.format(self.rating_total)
        self.total_stats['Rating total'] = self.rating_total
        stat_file.write(str(self.total_stats))
        stat_file.close()
        self.word_stats_data[self.word_stats_keys[ind]] = self.word_stats
        if self.word_stats[0] - self.word_stats[1] > 10:
            my_file = open(toga.App.app.paths.app / "resources/{0}.txt".format('vocabulary'), 'w',
                                  encoding='utf-8')
            del self.Vocabulary[self.word_stats_keys[ind]]
            del self.word_stats_data[self.word_stats_keys[ind]]
            self.key_list = list(self.Vocabulary.keys())
            self.words_total = len(self.key_list)
            self.words_total_count.value = 'Words in total: ' + '{0}'.format(self.words_total)
            my_file.write(str(self.Vocabulary))
            my_file.close()
        word_stat_file.write(str(self.word_stats_data))
        word_stat_file.close()

    def show_result(self, a):
        word_stat_file = open(toga.App.app.paths.app / "resources/{0}.txt".format('word_stats'), 'w', encoding='utf-8')
        self.word_stats[2] += 1
        if self.switch_language.value is True:
            true_answer = self.value_list[ind]
        else:
            true_answer = self.key_list[ind]
        self.word_stats_data[self.word_stats_keys[ind]] = self.word_stats
        word_stat_file.write(str(self.word_stats_data))
        word_stat_file.close()
        self.translate_place.value = true_answer
        self.skip_session += 1
        self.skip_session_count.value = 'Skips per session: ' + '{0}'.format(self.skip_session)
        self.check_button.text = 'Check ' + emoji.emojize(":red_question_mark:")
        self.next_button.enabled = True
        self.result_button.enabled = False
        self.check_button.enabled = False

    def next_word(self, a):
        self.word_place.value = ''
        self.translate_place.value = ''
        self.check_button.text = 'Check ' + emoji.emojize(":red_question_mark:")
        self.check_button.style.background_color = '#808080'
        self.words_session += 1
        self.words_session_count.value = 'Words per session: ' + '{0}'.format(self.words_session)
        self.show_word()
        self.check_button.enabled = True
        self.result_button.enabled = True
        self.next_button.enabled = False

    def add_word(self, a):
        my_file = open(toga.App.app.paths.app / "resources/{0}.txt".format('vocabulary'), 'w', encoding='utf-8')
        self.Vocabulary[self.eng_word_place.value] = self.rus_word_place.value
        self.key_list = list(self.Vocabulary.keys())
        self.words_total = len(self.key_list)
        self.words_total_count.value = 'Words in total: ' + '{0}'.format(self.words_total)
        my_file.write(str(self.Vocabulary))
        my_file.close()


def main():
    return VocabularyTest()
