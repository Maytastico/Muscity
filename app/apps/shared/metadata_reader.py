from config import Config
import eyed3
from flask import Flask
import os

class MusicFile():
    def __extract_album_cover(self):
        """extracts the pricture data of the audio file and writes it
        into data dir.
        """
        ext = ""
        for imageinfo in self.audio_file.tag.images:
            extension = {
                "image/jpeg" : ".jpg",
                "image/png" : ".png"
            }
            ext = extension.get(imageinfo.mime_type)
            path = os.path.join(Config.TITLE_COVER_DIR, self.file_link) + ext
            if not os.path.exists(path):
                f = open(path, 'x')
                f.close()
                with open(path, "wb") as f:
                    f.write(imageinfo.image_data)
                    f.close()
        
    def __get_metadata(self):
        """Gets the data from the eyed3 tag object and writes the data into
        the attributes. This is to later access the data inside the Music database
        model and write it into the database.
        """
        self.title = self.audio_file.tag.title
        self.artist = self.audio_file.tag.artist
        self.album = self.audio_file.tag.title
        self.album_artist = self.audio_file.tag.album_artist
        self.time = self.audio_file.info.time_secs

    def __init__(self, file_link):
        """Helps to organize the files inside the music folder. It gets the metadata of the file
        and extracts the thumbnail of the title

        Args:
            file_link (string): Contains the audio file name
        """

        super().__init__()
        self.audio_file = eyed3.load(os.path.join(Config.FILE_DIR, file_link))
        self.file_link = file_link
        self.__get_metadata()
        self.__extract_album_cover()
        
    def __repr__(self) -> str:
        return self.title + " / " + self.artist + self.album + " / " + str(self.time) + " / "




class AudioDirHandler:
    def getFiles(path:str):
        """Lists all files inside a specified path

        Args:
            path (str): This should contain a path to a folder

        Returns:
            list: returns a list with all files inside the dir
        """
        dir_content = os.listdir(path)

        files = []

        for file in dir_content:
            if os.path.isfile(os.path.join(path, file)):
                files.append(file)

        return files

    def getFilesbyType(path:str, extension:str):
        """Searches a File with in a specific path with an specific extension

        Args:
            path (string): The destination of the files
            extension (string): The specific keyword of the filename that you want inside the list

        Returns:
            list: Retuns a list of the file names that have the pattern inside
        """
        dir_content = os.listdir(path)

        files = []

        for file in dir_content:
            if os.path.isfile(os.path.join(path, file)):
                if extension in file:
                    files.append(file)

        return files


    def scan_dir(self):
        """Scans trough the music dir and adds their metadata into
        the database
        """
        files = AudioDirHandler.getFilesbyType(Config.FILE_DIR, ".mp3")
        with self.app.app_context():
            from database.handler import db, AudioFile
            for file in files:         
                if AudioFile.query.filter_by(file_name=file).first() == None:
                    audio = AudioFile(file)
                    db.session.add(audio)
                    db.session.commit()

    def housekeep(self):
        """Checks whether the audio files still exist inside the filesystem and deletes
        their thumbnails and flags them inside the database that they do not exist on the filesystem.
        """
        with self.app.app_context():
            from database.handler import db, AudioFile
            title_covers = AudioDirHandler.getFiles(Config.TITLE_COVER_DIR)
            music_files = AudioDirHandler.getFilesbyType(Config.FILE_DIR, ".mp3")
            database_data = AudioFile.query.all()
            
            #Goes through the thumbnails an looks whether the is a audio file with the same name
            for title_cover in title_covers:
                is_matching = False
                for audio in music_files:
                    if audio in title_cover:
                        is_matching = True
                        break
                if is_matching == False:
                    os.remove(os.path.join(Config.TITLE_COVER_DIR, title_cover))
                    is_matching = False

            #Searches through the data of the database and checks whether the
            #entries inside the database still exist on the fillsystem
            for audiofile in database_data:
                is_matching = False
                for musicfile in music_files:
                    if musicfile == audiofile.file_name:
                        is_matching=True
                        break
                if is_matching == False:
                    audiofile.present_on_filesystem = False
                    db.session.commit()
                    is_matching = False

    def __init__(self, app:Flask) -> None:
        """Manages the metadata and the audio files

        Args:
            app (Flask): Needs an Flask object to have a reference to the database
        """
        self.app = app
        self.scan_dir()
        self.housekeep()

