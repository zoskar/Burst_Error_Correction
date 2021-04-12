# Generator

import random

# dlugosc ciagu bitow, musi byc wielokrotnoscia 4
PARAM = 64


def generator(file):
    f = open(file, 'w')
    for i in range(PARAM):
        f.write(str(random.randint(0, 1)))
    f.close()


# Encoder


def hamming_encoder(file, filev2):
    with open(file, "r") as f:
        data = f.readline()

    # w tej części robimy z wczytanych danych listę i dzielimy ją na czterobitowe wyrazy

    words = []
    word_start = -4
    word_end = 0
    data = [int(b) for b in data]

    for i in range(0, int(PARAM / 4)):
        word_start += 4
        word_end += 4
        word = data[word_start:word_end]
        words.append(word)
    # ------------------------------------------------------------------------------------

    # następnie kodujemy w każdym z wyrazów bity parzystości; powstają słowa siedmiobitowe

    for word in words:
        if (word[0] + word[1] + word[3]) % 2 == 0:
            word.append(0)
        else:
            word.append(1)

        if (word[0] + word[2] + word[3]) % 2 == 0:
            word.append(0)
        else:
            word.append(1)

        if (word[0] + word[1] + word[2]) % 2 == 0:
            word.insert(3, 0)
        else:
            word.insert(3, 1)

    # ------------------------------------------------------------------------------------

    # ostatecznie zamieniamy listę na ciąg bitów (najpierw najstarsze bity danych z kolejnych słów, potem kolejne
    # itd. bitów parzystości nie wyrzucamy na koniec,
    # tylko są na ,,swoich miejscach''

    coded_signal = []

    for n in range(0, 7):
        for word in words:
            coded_signal.append(word[n])

    with open(filev2, "w") as f:
        for bit in coded_signal:
            bit = str(bit)
            f.write(bit)


def noise_generator(filev2):
    f = open(filev2, 'r')
    signal_txt = f.read()
    f.close()
    signal_str = list(signal_txt)
    noise_length = random.randint(1, 4)
    noise_start = random.randint(0, int(PARAM / 4 * 7)) - noise_length

    # ("Długość błędu:", noise_length)
    for i in range(noise_length):

        if signal_str[noise_start + i] == '1':
            signal_str[noise_start + i] = '0'
            # print('1->0')

        elif signal_str[noise_start + i] == '0':
            signal_str[noise_start + i] = '1'
            # print('0->1')

    f = open(filev2, 'w')

    for i in signal_str:
        f.write(i)

    f.close()

    # ------------------------------------------------------------------------------------


def hamming_decoder(filev2, filev3):
    with open(filev2, "r") as f:
        data = f.readline()

    # w tej części robimy z wczytanych danych listę i dzielimy ją na siedmiobitowe wyrazy

    words = []

    for j in range(int(PARAM / 4)):
        word = []
        for i in range(0, int(PARAM / 4 * 7), int(PARAM / 4)):  # liczba bitów
            word.append(int(data[i + j]))
        words.append(word)

    for word in words:
        p4 = (word[0] + word[1] + word[2] + word[3]) % 2
        p2 = (word[0] + word[1] + word[4] + word[5]) % 2
        p1 = (word[0] + word[2] + word[4] + word[6]) % 2
        wrong_bit = 4 * p4 + 2 * p2 + 1 * p1

        if wrong_bit == 3:
            if word[4] == 0:
                word[4] = 1
            else:
                word[4] = 0

        if wrong_bit == 5:
            if word[2] == 0:
                word[2] = 1
            else:
                word[2] = 0

        if wrong_bit == 6:
            if word[1] == 0:
                word[1] = 1
            else:
                word[1] = 0

        if wrong_bit == 7:
            if word[0] == 0:
                word[0] = 1
            else:
                word[0] = 0

        del word[6]
        del word[5]
        del word[3]

    coded_signal = []

    for word in words:
        for bit in word:
            coded_signal.append(bit)

    with open(filev3, "w") as f:
        for bit in coded_signal:
            f.write(str(bit))


def compare(file, filev2):
    i = 0
    f = open(file, 'r')
    data_a = f.readline()
    f.close()

    g = open(filev2, 'r')
    data_b = g.readline()
    g.close()

    if len(data_a) is not len(data_b):
        print("Różne Długości plików")
        return
    for index, data in enumerate(data_a):
        if data != data_b[index]:
            i += 1
            print(f"Error in {index} column")
    print("Ilość błędów: ", i)


if __name__ == '__main__':
    generator("signal.txt")
    hamming_encoder("signal.txt", "coded_signal.txt")
    hamming_decoder("coded_signal.txt", "decoded_signal.txt")
    compare("decoded_signal.txt", "signal.txt")
