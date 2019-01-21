def main():

    with open('feedback.txt', 'r') as f:
        data = f.read()
    data = data.split('\t')
    data = [w.split('\n') for w in data]
    print(data)


if __name__ == "__main__":
    main()