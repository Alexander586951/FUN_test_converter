import random
import sys
from datetime import date


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


def process_file(act_input_file, gift_output_file):
    test_head_data = {}
    test_data = {}

    with open(act_input_file, encoding='utf-8') as f_i:
        i_counter = 0
        for line in nonblank_lines(f_i):

            if 'V1:' in line:
                line = line.replace('V1: ', '')
                test_head_data['head_1'] = line.strip()
            elif 'V2:' in line:
                line = line.replace('V2: ', '')
                test_head_data['head_2'] = line.strip()
            elif 'I:' in line:
                i_counter += 1
                test_data[f'{i_counter}'] = {}
                test_data[f'{i_counter}']['head'] = \
                    line.replace('I: ', '').strip()
                test_data[f'{i_counter}']['pos_answer'] = []
                test_data[f'{i_counter}']['neg_answer'] = []
            elif 'S:' in line:
                test_data[f'{i_counter}']['body'] = \
                    line.replace('S: ', '').strip()
            elif '+:' not in line and '-:' not in line:
                test_data[f'{i_counter}']['body'] += ('\n' + line)
            elif '+:' in line:
                test_data[f'{i_counter}']['pos_answer'] \
                    .append(line.replace('+: ', '').strip())
            elif '-:' in line:
                test_data[f'{i_counter}']['neg_answer'] \
                    .append(line.replace('-: ', '').strip())

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
            elif neg_answer_count == 0:
                o_f.write(f"::{test_data[q]['head']}::")
                q_body = test_data[q]['body'].split("…")
                o_f.write(f"{q_body[0]} "
                          + "{=" + f"{test_data[q]['pos_answer'][0]}" + "}"
                          + f" {q_body[1]}\n")
                o_f.write(' \n')


def convert():
    if len(sys.argv) > 1:

        file_name = sys.argv[-1]
        print('Входной файл: ', file_name, '\n')

        out_path_name = file_name.split('\\')

        today = date.today()
        output_file = f'GIFT_{out_path_name[-1].replace(".txt", "")}_{today}.txt'

        process_file(file_name, output_file)
        success_message = f'Файл {output_file} готов\nОн лежит в том же каталоге, что и исходный файл\n'
        print(success_message)
    else:
        print('Отсутствует файл для обработки.\n'
              'Перетяните мышкой .txt файл с тестом на bat-файл\n'
              'После обработки сконвертированный файл сохранится рядом с исходным')


if __name__ == "__main__":
    convert()
