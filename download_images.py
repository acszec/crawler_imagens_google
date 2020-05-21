import urllib.request
import os
import sys
import progressbar
import hashlib
import time

images_folder_name = 'images'
default_timeout = 0.5


class DownloadImages:
    def start(self, filepath):
        if not os.path.isfile(filepath):
            print("File path {} does not exist. Exiting...".format(filepath))
            sys.exit()

        os.makedirs(images_folder_name, exist_ok=True)

        with open(filepath) as fp:
            urls = [url for url in enumerate(fp)]

        total_images = len(urls)
        err = 0

        with progressbar.ProgressBar(max_value=total_images) as bar:
            for i, url in urls:
                try:
                    res = urllib.request.urlopen(url)
                    file_type = res.info()['Content-Type'].split('/')[1]

                    image_file_path = os.path.join(
                        images_folder_name, self._generate_name(url)) + "." + file_type

                    urllib.request.urlretrieve(url, image_file_path)
                    bar.update(i)
                    time.sleep(default_timeout)
                except Exception:
                    err += 1

        print(f"Error to process {err} from {total_images} files.")

    def _generate_name(self, url):
        hash_object = hashlib.sha256(url.encode('utf-8'))
        return hash_object.hexdigest()


if __name__ == "__main__":
    file_path = sys.argv[1]
    print(f"Starting the download of all the links of file {file_path}")
    DownloadImages().start(file_path)