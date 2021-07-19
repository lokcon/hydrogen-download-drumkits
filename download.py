import os
import requests
import re
import time
import io
import sys
import tarfile
import xml.etree.ElementTree

HYDROGEN_PATH = os.path.expanduser("~/.hydrogen/")
HYDROGEN_CONFIG = "hydrogen.conf"
HYDROGEN_DRUMKIT_PATH = "data/drumkits"

def main():
    server_urls = read_server_urls_from_config()
    for server_url in server_urls:
        print(server_url)

        drumkit_list_xml = fetch_http(server_url)
        if drumkit_list_xml is None:
            print("    - Invalid response from server. Not doing anything")
            continue

        drumkit_list = read_drumkit_list(drumkit_list_xml)
        for drumkit in drumkit_list:
            name, author, url = drumkit
            print("")
            print("    - {} | {}".format(name, author))
            print("      {}".format(url))

            drumkit_name = parse_drumkit_name(url)
            if drumkit_name is None:
                print("      Unable to parse drumkit name in the format of '{name}.h2drumkit' from the url. This drumkit will not be skipped.")
            else:
                drumkit_path = drumkit_dir_path(drumkit_name)
                if os.path.isdir(drumkit_path):
                    print ("      Drumkit already exists. Skipping.")
                    continue

            try:
                h2drumkit_file = fetch_http_bytes(url)
            except Exception as e:
                print("      Failed to download h2drumkit file: '{}'. Skipping.".format(e))
                continue

            try:
                tar = tarfile.open(fileobj=h2drumkit_file, mode="r:*")
                tar.extractall(path=os.path.join(HYDROGEN_PATH, HYDROGEN_DRUMKIT_PATH))
            except Exception as e:
                print("      Error occured while decompressing file: '{}'. Skipping.".format(e))
                continue

            print("")

        print("")


def drumkit_dir_path(drumkit_name):
    return os.path.join(HYDROGEN_PATH, HYDROGEN_DRUMKIT_PATH, drumkit_name)


def parse_drumkit_name(url):
    match = re.search(r"^.*\/(.*?)\.h2drumkit$", url)
    if match is None:
        return None

    return match.group(1)


def fetch_http(url):
    response = requests.get(url, allow_redirects=True)
    if response.status_code != 200:
        return None

    return response.text


def fetch_http_bytes(url):
    f = io.BytesIO()

    start = time.time()
    response = requests.get(url, stream=True)
    total_length = response.headers.get('content-length')

    downloaded = 0
    if total_length is None:
        f.write(response.content)
    else:
        total_length = int(total_length)
        for chunk in response.iter_content(1024):
            f.write(chunk)

            downloaded  += len(chunk)
            done = int(20 * downloaded / total_length)

            sys.stdout.write("\r      [{}{}] {:.2f} MB / {:.2f} MB, {:.2f}s, {:.2f} Mbps".format(
                '=' * done,
                ' ' * (20 - done),
                downloaded / 1000000,
                total_length / 1000000,
                time.time() - start,
                downloaded // (time.time() - start) / 1000000)
            )

    f.seek(0)
    return f


def read_drumkit_list(drumkit_xml):
    drumkit_list_tree = xml.etree.ElementTree.fromstring(drumkit_xml)
    assert drumkit_list_tree.tag == "drumkit_list" 

    drumkits = drumkit_list_tree.iter("drumkit")
    for drumkit in drumkits:
        name, = drumkit.iter("name")
        author, = drumkit.iter("author")
        url, = drumkit.iter("url")
        yield (name.text, author.text, url.text)


def read_server_urls_from_config():
    config_path = os.path.join(HYDROGEN_PATH, HYDROGEN_CONFIG)
    with open(config_path, "r") as f:
        config = f.read()

    config_tree = xml.etree.ElementTree.fromstring(config)
    assert config_tree.tag == "hydrogen_preferences"

    server_list, = config_tree.iter("serverList")
    servers = [server for server in server_list.iter("server")]
    server_urls = [server.text for server in servers]

    return server_urls


if __name__ == "__main__":
    main()
