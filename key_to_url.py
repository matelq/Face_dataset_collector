from pytube import Search


def convert(key, pages):
    s = Search(key)
    for i in range(int(pages) - 1):
        s.results
        s.get_next_results()

    print('{}, DONE!'.format(key))
    return s.results


def keys_to_urls():

    class KeyInfo:
        def __init__(self, key, pages):
            self.key = key
            self.pages = pages

    keyword_csv_file = 'key_words.csv'

    with open(keyword_csv_file, 'r') as f:
        lines = f.readlines()
        lines = [x.split(',') for x in lines]
        keyword_infos = [KeyInfo(x[0], x[1]) for x in lines]

    urls_from_keys_csv = open('urls_from_keys.csv', 'w')
    for KeyInfo in keyword_infos:
        ktu_list = convert(KeyInfo.key, KeyInfo.pages)
        for ktu in ktu_list:
            urls_from_keys_csv.write(ktu.watch_url + ', ' + KeyInfo.key + '\n')
    urls_from_keys_csv.close()









