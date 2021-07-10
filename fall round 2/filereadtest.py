'''with open('test.txt', 'w') as f:
    f.write("Hello\nThis is a test\nto see if\n a file ends\n with newline")
    f.close()
with open('test.txt','r+') as f:
    lines = f.readlines()
    last = lines[-1]
    if last[-1] == "\n":
        print("Yes")
    else:
        print("False")
        print(lines)
        f.seek(0,0)
        del lines[-1]
        for line in lines:
            f.write(line)
        f.write(last + "\n")
        f.seek(0,0)
        print(f.readlines())
    f.close()'''
with open('Book1.csv','r+') as f:
    lines = f.readlines()
    print(lines)
    last = lines[-1]
    if last[-1] == "\n":
        print("Yes")
    else:
        print("False")
        f.write("\n")
        f.seek(0)
        print(f.readlines())


