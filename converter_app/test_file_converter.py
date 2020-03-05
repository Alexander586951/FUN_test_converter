import random
import sys
from datetime import date

import re

LEFT_QUESTION_PATTERN = r'L[0-9]?\:'
RIGHT_QUESTION_PATTERN = r'R[0-9]?\:'
SEQUENCE_PATTERN = r'[0-9]?\:'


def nonblank_lines(f):
    """
    from https://stackoverflow.com/questions/4842057/easiest-way-to-ignore-blank-lines-when-reading-a-file-in-python
    skips empty lines during reading text file
    :param f: - file
    :return:
    """
    for l in f:
        line = l.rstrip()
        if line:
            yield line


def randomize_list(source_list):
    random.shuffle(source_list)
    return source_list


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def process_title_line(line: str, pattern: str):
    """
    Обработка
        - титульных закомментированных строк
        - строк названия вопроса
    :param line: строка из исходного файла
    :param pattern: служебная комбинация символов
    :return: обработанная строка
    """
    res_line = line.replace(f'{pattern} ', '').replace(f'{pattern}', '').strip()
    return res_line


def process_question_body(line: str, pattern: str):
    """
    Обработка строки формулировки вопроса
    :param line: строка из исходного файла
    :param pattern: служебная комбинация символов
    :return: обработанная строка
    """
    if '<p>' in line and '</p>' in line:
        line = '[html]' + line
    res_line = line.replace(f'{pattern} ', '') \
        .replace(f'{pattern}', '').replace('#', '').strip()
    return res_line


def process_pairing_answers(line: str, pattern: str):
    """
    Обработка ответов в вопросе на сопоставление
    :param line: строка из исходного файла
    :param pattern: служебная комбинация символов
    :return: обработанная строка
    """
    pattern = re.compile(pattern)
    res_line = pattern.sub('', line)
    return res_line.strip()


def process_positive_answer(line: str, pattern: str, target_list: list):
    """
    Обработка строк правильных ответов:
        - очистка от старой служебной разметки;
        - проверка на формат регулярных выражений, и очистка;
        - запись в соответствующий list
    :param line: строка из исходного файла
    :param pattern: служебная комбинация символов
    :param target_list: список, содержащий правильные ответы
    """
    if "^\S" in line and "\S*$" in line:
        line = line.replace("+:^\S*(", "").replace(")\S*$)", "") \
            .replace("\S*$  ","").split('|')
        for text in line:
            target_list.append(text)
    else:
        target_list.append(line.replace(f'{pattern} ', '')
                           .replace(f'{pattern}', '').strip())


def process_negative_answer(line: str, pattern: str, target_list: list):
    """
    Обработка строк неправильных ответов:
    :param line: строка из исходного файла
    :param pattern: служебная комбинация символов
    :param target_list: список, содержащий правильные ответы
    """
    res_line = line.replace(f'{pattern} ', '').replace(f'{pattern}', '').strip()
    target_list.append(res_line)



def process_file(act_input_file, gift_output_file):
    test_head_data = {}
    test_data = {}

    # LEFT_QUESTION_PATTERN = r'L[0-9]?\:'
    # RIGHT_QUESTION_PATTERN = r'R[0-9]?\:'
    # SEQUENCE_PATTERN = r'[0-9]?\:'

    with open(act_input_file, encoding='utf-8') as f_i:
        i_counter = 0
        for line in nonblank_lines(f_i):

            if 'V1:' in line:
                test_head_data['head_1'] = process_title_line(line, 'V1:')
            elif 'V2:' in line:
                test_head_data['head_2'] = process_title_line(line, 'V2:')
            elif 'I:' in line:
                i_counter += 1
                test_data[f'{i_counter}'] = {}
                test_data[f'{i_counter}']['head'] = process_title_line(
                    line, 'I:'
                )

                test_data[f'{i_counter}']['pos_answer'] = []
                test_data[f'{i_counter}']['neg_answer'] = []
                test_data[f'{i_counter}']['left_answer'] = []
                test_data[f'{i_counter}']['right_answer'] = []
            elif 'S:' in line:
                test_data[f'{i_counter}']['body'] = process_question_body(
                    line, 'S:'
                )

            # считываем ответы L1, L2,... R1, R2...
            elif re.match(LEFT_QUESTION_PATTERN, line):
                test_data[f'{i_counter}']['left_answer'].append(
                    process_pairing_answers(line, LEFT_QUESTION_PATTERN)
                )
            elif re.match(RIGHT_QUESTION_PATTERN, line):
                test_data[f'{i_counter}']['right_answer'].append(
                    process_pairing_answers(line, RIGHT_QUESTION_PATTERN)
                )

            # преобразуем вопрос на последовательность
            # в вопрос на сопоставление
            elif re.match(SEQUENCE_PATTERN, line):
                seq_line = line.split(':')
                test_data[f'{i_counter}']['left_answer'] \
                    .append(seq_line[0])
                test_data[f'{i_counter}']['right_answer'] \
                    .append(seq_line[1])

            # если вопрос из нескольких строк,
            # подшиваем строки без служебной разметки к телу вопроса
            elif '+:' not in line and '-:' not in line:
                test_data[f'{i_counter}']['body'] += ('\n' + line)

            elif '+:' in line:
                process_positive_answer(line, '+:',
                                        test_data[f'{i_counter}']['pos_answer'])
            elif '-:' in line:
                process_negative_answer(line, '-:',
                                        test_data[f'{i_counter}']['neg_answer'])


    with open(gift_output_file, 'w', encoding='utf-8') as o_f:

        o_f.write(f"//H1: {test_head_data['head_1']}\n\n")
        o_f.write(f"//H2: {test_head_data['head_2']}\n")
        o_f.write(' \n')

        for q in test_data:
            # подставляю сюда одни и те же данные,
            # пока мало информации о том, что класть в поле question
            o_f.write(f"// question: Вопрос №{q}  "
                      f"name: {test_data[q]['head']}\n")

            neg_answer_count = len(test_data[q]['neg_answer'])
            l_answer_count = len(test_data[q]['left_answer'])
            r_answer_count = len(test_data[q]['right_answer'])

            # GIFT не поддерживает вопросы на сопоставление с неравными
            # списками вариантов. Искусственно выравниваем их.
            while len(test_data[q]['right_answer']) < len(test_data[q]['left_answer']):
                test_data[q]['right_answer'].append(' ')
            while len(test_data[q]['left_answer']) < len(test_data[q]['right_answer']):
                test_data[q]['left_answer'].append(' ')

            # запись вопроса multiple choice
            if neg_answer_count >= 1:
                o_f.write(f"::{test_data[q]['head']}::{test_data[q]['body']} ")
                o_f.write("{\n")

                answers = []
                for pos_answer in test_data[q]['pos_answer']:
                    pos_answer = '=' + pos_answer
                    answers.append(pos_answer)
                for neg_answer in test_data[q]['neg_answer']:
                    neg_answer = '~' + neg_answer
                    answers.append(neg_answer)

                for answer in randomize_list(answers):
                    o_f.write(f"\t{answer} \n")

                o_f.write("}\n")
                o_f.write(" \n")

            # запись вопросов fill in answer/short answer
            elif neg_answer_count == 0 and l_answer_count == 0:
                o_f.write(f"::{test_data[q]['head']}::")
                if '...' in line or '…' in line:
                    q_body = test_data[q]['body'].replace('...', '…') \
                        .replace('#', '').split("…")
                    o_f.write(f"{q_body[0]} "
                              + "{=" + f"{test_data[q]['pos_answer'][0]}" + "}"
                              + f" {q_body[1]}\n")
                else:
                    o_f.write(f"{test_data[q]['body']} " + "{")
                    for pos_answer in test_data[q]['pos_answer']:
                        if isfloat(pos_answer): # TODO: заменить на корректное выстраивание множественных цифровых ответов
                            o_f.write(f"#{pos_answer} ")
                        else:
                            o_f.write(f"={pos_answer} ")
                    o_f.write('}\n')
                o_f.write(' \n')

            # запись вопроса на сопоставление
            elif neg_answer_count == 0 and l_answer_count > 0:
                match_list = list(zip(
                    test_data[q]['left_answer '] ,test_data[q]['right_answer']
                ))
                o_f.write(f"::{test_data[q]['head']}::{test_data[q]['body']} ")
                o_f.write("{\n")
                for pair in match_list:
                    o_f.write(f"\t={pair[0]}\t-> {pair[1]} \n")
                o_f.write('}\n')
                o_f.write(' \n')


def convert():
    if len(sys.argv) > 1:

        file_name = sys.argv[-1]
        print('Входной файл: ', file_name, '\n')

        out_path_name = file_name.split('\\')

        today = date.today()
        output_file = f'GIFT_{out_path_name[-1].replace(".txt", "")}' \
                      f'_{today}.txt'

        process_file(file_name, output_file)
        success_message = f'Файл {output_file} готов\nОн лежит в том же ' \
                          f'каталоге, что и исходный файл\n'
        print(success_message)
    else:
        print('Отсутствует файл для обработки.\n'
              'Перетяните мышкой .txt файл с тестом на bat-файл\n'
              'После обработки сконвертированный файл сохранится '
              'рядом с исходным')


if __name__ == "__main__":
    convert()


    # from pathlib import Path
    #
    # test_files = Path('./fixtures').glob('*.txt')
    # for file in test_files:
    #     input_file = str(file)
    #     output_file = input_file.replace('.txt', '_GIFT.txt')
    #     process_file(file, output_file)
