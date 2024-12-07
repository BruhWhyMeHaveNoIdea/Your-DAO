def gpt_converter(questions):
    d = []
    for i in questions:
        d.append({"role": i[0], "content": i[1]})
    return d
