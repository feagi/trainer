import csv
import argparse
import random


def convert_iris_dataset(input_file, train_output, test_output):
    class_mapping = {
        "Iris-setosa": 0,
        "Iris-versicolor": 1,
        "Iris-virginica": 2  # Assuming the third class might be present in a full dataset
    }

    data_by_class = {0: [], 1: [], 2: []}

    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                class_label = class_mapping[row[-1]]  # Convert class name to integer
                features = list(map(float, row[:-1]))  # Convert features to floats
                data_by_class[class_label].append([class_label] + features)  # Reorder

    train_data = []
    test_data = []

    for class_label, data in data_by_class.items():
        random.shuffle(data)
        split_idx = int(len(data) * 2 / 3)  # 2/3 for training, 1/3 for testing
        train_data.extend(data[:split_idx])
        test_data.extend(data[split_idx:])

    with open(train_output, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(train_data)

    with open(test_output, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(test_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Iris dataset format and split into training and test sets.")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("train_output", help="Path to the output training CSV file")
    parser.add_argument("test_output", help="Path to the output test CSV file")
    args = parser.parse_args()

    convert_iris_dataset(args.input_file, args.train_output, args.test_output)

