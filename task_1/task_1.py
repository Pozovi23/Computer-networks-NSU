import subprocess
import csv


def write_csv(results):
    with open("sites.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(results)


def ping_server():
    sites = [
        "youtube.com",
        "instagram.com",
        "google.com",
        "mail.ru",
        "nsu.ru",
        "ya.ru",
        "ru.wikipedia.org",
        "geeksforgeeks.org",
        "discord.com",
        "docs.python.org",
    ]
    results = []

    for site in sites:
        output = str(
            subprocess.run(["ping", "-c", "1"] + [site], capture_output=True, text=True)
        )

        if output.find("Destination Protocol Unreachable") == -1:
            index = output.find("time") + len("time=")
            result = ""
            symbol = output[index]

            while symbol != "s":
                result += symbol
                index += 1
                symbol = output[index]
            result += "s"
            results += [[site, result]]
        else:
            results += [[site, "Unreachable"]]

    return results


def main():
    results = ping_server()
    write_csv(results)


main()
