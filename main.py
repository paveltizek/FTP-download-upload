import ftplib
import requests
import configparser

class FTPManager:
    def __init__(self):
        # Načtení konfiguračních dat
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.ftp_host = self.config['FTP']['host']
        self.ftp_username = self.config['FTP']['username']
        self.ftp_password = self.config['FTP']['password']
        self.ftp_target_directory = self.config['FTP']['target_directory']
        self.local_download_path = self.config['Local']['local_download_path']
        self.url_to_download = self.config['Local']['url_to_download']
        self.target_filename = self.config['Local']['target_filename']

    def upload_file(self, file_to_upload, target_directory, target_filename):
        try:
            print("Začínám stahovat")
            ftp = ftplib.FTP(self.ftp_host)
            ftp.login(self.ftp_username, self.ftp_password)
            ftp.cwd(target_directory)
            with open(file_to_upload, 'rb') as file:
                ftp.storbinary(f'STOR {target_filename}', file)
            ftp.quit()
            print("Soubor byl úspěšně nahrán.")
        except ftplib.all_errors as e:
            print(f"FTP error: {e}")

    def download_file_from_url(self, url, local_path):
        try:
            print("Začínám nahrávat")
            response = requests.get(url)
            response.raise_for_status()
            with open(local_path, 'wb') as file:
                file.write(response.content)
            print(f"Soubor byl úspěšně stažen a uložen jako {local_path}.")
        except requests.RequestException as e:
            print(f"Chyba při stahování souboru: {e}")

    def main(self):
        # Stáhnout soubor z URL
        self.download_file_from_url(self.url_to_download, self.local_download_path)

        # Nahrát soubor na FTP server
        self.upload_file(self.local_download_path, self.ftp_target_directory, self.target_filename)

# Vytvoření instance třídy FTPManager a spuštění hlavní funkce
if __name__ == '__main__':
    ftp_manager = FTPManager()
    ftp_manager.main()
