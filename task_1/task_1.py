import csv
import subprocess


def write_csv(results):
    with open("./sites.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(results)


def parse_response(response):
    index = response.find("time") + len("time=")
    symbol = response[index]
    result = ""

    while symbol != "s":
        result += symbol
        index += 1
        symbol = response[index]
    result += "s"

    return result

def response_from_server(site):
    output = str(
        subprocess.run(["ping", "-c", "1"] + [site], capture_output=True, text=True)
    )
    result = ""

    if (
        output.find("Destination Protocol Unreachable") == -1
        and output.find("100% packet loss") == -1
        and output.find("time") != -1
    ):
        result = parse_response(output)
    else:
        result = "Unreachable or something went wrong"

    return result


def ping_servers():
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
        time = response_from_server(site)
        results += [[site, time]]

    return results


def main():
    results = ping_servers()
    write_csv(results)


main()
