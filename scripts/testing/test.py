

if __name__ == "__main__":
    f = open('../../resources/txt_files/QnA_formated.txt')

    unedited_input = f.read()

    context_list = unedited_input.split("[delimiter]")
    context_list.pop(len(context_list) - 1)

    f.close()