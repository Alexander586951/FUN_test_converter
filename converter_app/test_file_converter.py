import random
import sys
import re

from datetime import date
from pathlib import Path


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
    """
    from https://stackoverflow.com/a/20929881
    :param value: string that could be converted to float
    :return: Boolean
    """
    try:
        float(value)
        return True
    except ValueError:
        return False



def process_file(act_input_file, gift_output_file):
    test_head_data = {}
    test_data = {}

    left_question_pattern = r'L[0-9]?\:'
    right_question_pattern = r'R[0-9]?\:'
    sequence_pattern = r'[0-9]?\:'

    with open(act_input_file, encoding='utf-8') as f_i:
        i_counter = 0
        for line in nonblank_lines(f_i):

            if 'V1:' in line:
                line = line.replace('V1: ', '').replace('V1:', '')
                test_head_data['head_1'] = line.strip()
            elif 'V2:' in line:
                line = line.replace('V2: ', '').replace('V2:', '')
                test_head_data['head_2'] = line.strip()
            elif 'I:' in line:
                i_counter += 1
                test_data[f'{i_counter}'] = {}
                test_data[f'{i_counter}']['head'] = \
                    line.replace('I: ', '').replace('I:', '').strip()
                test_data[f'{i_counter}']['pos_answer'] = []
                test_data[f'{i_counter}']['neg_answer'] = []
                test_data[f'{i_counter}']['left_answer'] = []
                test_data[f'{i_counter}']['right_answer'] = []
            elif 'S:' in line:
                test_data[f'{i_counter}']['body'] = \
                    line.replace('S: ', '').replace('S:', '')\
                        .replace('#', '').strip()

            # обработка вопроса на последовательность
            elif re.match(left_question_pattern, line):
                pattern = re.compile(left_question_pattern)
                left_line = pattern.sub('', line)
                test_data[f'{i_counter}']['left_answer']\
                    .append(left_line.strip())
            elif re.match(right_question_pattern, line):
                pattern = re.compile(right_question_pattern)
                right_line = pattern.sub('', line)
                test_data[f'{i_counter}']['right_answer']\
                    .append(right_line.strip())

            # преобразуем вопрос на последовательность
            # в вопрос на сопоставление
            elif re.match(sequence_pattern, line):
                seq_line = line.split(':')
                test_data[f'{i_counter}']['left_answer']\
                    .append(seq_line[0])
                test_data[f'{i_counter}']['right_answer']\
                    .append(seq_line[1])

            elif '+:' not in line and '-:' not in line:
                test_data[f'{i_counter}']['body'] += ('\n' + line)
            elif '+:' in line:
                test_data[f'{i_counter}']['pos_answer'] \
                    .append(line.replace('+: ', '').replace('+:', '')
                            .strip())
            elif '-:' in line:
                test_data[f'{i_counter}']['neg_answer'] \
                    .append(line.replace('-: ', '').replace('-:', '')
                            .strip())

    # print(test_data)

    with open(gift_output_file, 'w', encoding='utf-8') as o_f:

        o_f.write(f"//H1: {test_head_data['head_1']}\n\n")
        o_f.write(f"//H2: {test_head_data['head_2']}\n")
        o_f.write(' \n')

        for q in test_data:
            # подставляю сюда одни и те же данные,
            # пока мало информации о том, что класть в поле question
            o_f.write(f"// question: {test_data[q]['head']}  "
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

            # обработка вопросов multiple choice
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

            # обработка вопросов fill in answer
            elif neg_answer_count == 0 and l_answer_count == 0:
                o_f.write(f"::{test_data[q]['head']}::")
                if '...' in line or '…' in line:
                    q_body = test_data[q]['body'].replace('...', '…')\
                        .replace('#', '').split("…")
                    o_f.write(f"{q_body[0]} "
                              + "{=" + f"{test_data[q]['pos_answer'][0]}" + "}"
                              + f" {q_body[1]}\n")
                else:
                    o_f.write(f"{test_data[q]['body']} " + "{")
                    for pos_answer in test_data[q]['pos_answer']:
                        if isfloat(pos_answer): # TODO: заменить на корректное выстраивание множественных цифровых ответов
                            print("it's digits!")
                            o_f.write(f"#{pos_answer} ")
                        else:
                            o_f.write(f"={pos_answer} ")
                    o_f.write('}\n')
                o_f.write(' \n')

            # обработка вопросов на сопоставление
            elif neg_answer_count == 0 and l_answer_count > 0:
                left_answers = test_data[q]['left_answer']
                right_answers = test_data[q]['right_answer']

                match_list = list(zip(left_answers,right_answers))

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
        output_file = f'GIFT_{out_path_name[-1].replace(".txt", "")}_{today}.txt'

        process_file(file_name, output_file)
        success_message = f'Файл {output_file} готов\nОн лежит в том же ' \
                          f'каталоге, что и исходный файл\n'
        print(success_message)
    else:
        print('Отсутствует файл для обработки.\n'
              'Перетяните мышкой .txt файл с тестом на bat-файл\n'
              'После обработки сконвертированный файл сохранится рядом с исходным')


if __name__ == "__main__":
    convert()
