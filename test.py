def imageProcess(p):
    #num = 0
    pictures = p
    if (len(pictures) % 4) == 0:
        maxPage = (len(pictures) // 4)
    else:
        maxPage = (len(pictures) // 4) + 1

    if (len(pictures) % 4) != 0:
        for addPicture in range(4 - (len(pictures) % 4)):
            pictures.append("null.jpg")

    return pictures, maxPage