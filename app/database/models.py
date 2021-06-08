from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


playlist_created_by = db.Table('playlist_created_by',
    db.Column('user_id', db.Integer, db.ForeignKey('users.u_id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.p_id'), primary_key=True)
)

playlist_can_be_seen_by = db.Table('playlist_can_be_seen_by',
    db.Column('user_id', db.Integer, db.ForeignKey('users.u_id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.p_id'), primary_key=True)
)

titles_in_playlist = db.Table('title_in_playlist',
    db.Column('title_id', db.Integer, db.ForeignKey('titles.t_id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.p_id'), primary_key=True)
)

class Playlist(db.Model):
    __tablename__ = 'playlist'
    p_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1000))
    is_Public = db.Column(db.Boolean, nullable=False)
    playlist_created = db.relationship('Created', secondary=playlist_created_by, lazy='subquery',
        backref=db.backref('playlist_created', lazy=True))
    playlist_can_be_seen = db.relationship('Can Be Seen', secondary=playlist_can_be_seen_by, lazy='subquery',
        backref=db.backref('users_can_see', lazy=True))
    title_in_playlist = db.relationship('Titles in Playlist', secondary=titles_in_playlist, lazy='subquery',
        backref=db.backref('titles_in_playlist', lazy=True))

    def __repr__(self):
        return '<Playlistname %r>' % self.name

title_has_atmosphere = db.Table('title_has_atmosphere',
    db.Column('atmosphere_id', db.Integer, db.ForeignKey('atmosphere.at_id'), primary_key=True),
    db.Column('title_id', db.Integer, db.ForeignKey('titles.t_id'), primary_key=True)
)

title_has_genre = db.Table('title_has_genre',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.g_id'), primary_key=True),
    db.Column('title_id', db.Integer, db.ForeignKey('titles.t_id'), primary_key=True)
)

title_belongs_to_album = db.Table('title_belongs_to_album',
    db.Column('album_id', db.Integer, db.ForeignKey('album.a_id'), primary_key=True),
    db.Column('title_id', db.Integer, db.ForeignKey('titles.t_id'), primary_key=True)
)

class Title(db.Model):
    __tablename__ = 'titles'
    #Table attributes
    t_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    playtime = db.Column(db.Integer, nullable=False)
    release_date = db.Column(db.DateTime)
    file_path = db.Column(db.String(), nullable=False)
    thumbnail_path = db.Column(db.String())

    #Database relations
    title_atmosphere = db.relationship('Atmosphere', secondary=title_has_atmosphere, lazy='subquery',
        backref=db.backref('Titles', lazy=True))
    title_genre = db.relationship('Genre', secondary=title_has_genre, lazy='subquery',
        backref=db.backref('Titles', lazy=True))
    title_alben = db.relationship('Alben', secondary=title_belongs_to_album, lazy='subquery',
        backref=db.backref('Alben', lazy=True))
    title_in_playlists = db.relationship('Playlists', secondary=titles_in_playlist, lazy='subquery',
        backref=db.backref('Titles', lazy=True))
    sees_playlists = db.relationship('Sees Playlists', secondary=playlist_can_be_seen_by, lazy='subquery',
        backref=db.backref('Playlists', lazy=True))
    created_playlists = db.relationship('Created Playlists', secondary=playlist_created_by, lazy='subquery',
        backref=db.backref('Playlists', lazy=True))

    def __repr__(self):
        return '<Titlename %r>' % self.name

user_likes_title = db.Table('user_likes_title',
    db.Column('user_id', db.Integer, db.ForeignKey('users.u_id'), primary_key=True),
    db.Column('title_id', db.Integer, db.ForeignKey('titles.t_id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    #Table attributes
    u_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    #Datebase relations
    user_likes = db.relationship('Titles in Playlist', secondary=user_likes_title, lazy='subquery',
        backref=db.backref('user_likes', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

class Atmosphere(db.Model):
    __tablename__ = 'atmosphere'

    #Table attributes
    at_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1000))

    #Database relations
    title_with_atmosphere = db.relationship('Tiltes with atmosphere', secondary=title_has_atmosphere, lazy='subquery',
        backref=db.backref('Titles', lazy=True))

    def __repr__(self):
        return '<Atmospherename %r>' % self.name

interpret_plays_genre = db.Table('interpret_plays_genre',
    db.Column('interpret_id', db.Integer, db.ForeignKey('interpret.i_id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.g_id'), primary_key=True)
)

class Genre(db.Model):
    __tablename__ = 'genre'

    #Table relations
    g_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1000))

    #Database relations
    interprets = db.relationship('Genre', secondary=interpret_plays_genre, lazy='subquery',
        backref=db.backref('Interprets', lazy=True))

    def __repr__(self):
        return '<Genre %r>' % self.name

album_belongs_to_interpret = db.Table('album_belongs_to_interpret',
    db.Column('album_id', db.Integer, db.ForeignKey('album.a_id'), primary_key=True),
    db.Column('interpret_id', db.Integer, db.ForeignKey('interpret.i_id'), primary_key=True)
)

class Album(db.Model):
    __tablename__ = 'album'

    #Table attributes
    a_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1000))
    created = db.Column(db.DateTime, nullable=False)

    #Database relations
    title_alben = db.relationship('Titles', secondary=title_belongs_to_album, lazy='subquery',
        backref=db.backref('Titles', lazy=True))

    interprets = db.relationship('Genre', secondary=album_belongs_to_interpret, lazy='subquery',
        backref=db.backref('Interprets', lazy=True))

    def __repr__(self):
        return '<Albumname %r>' % self.name



class Interpret(db.Model):
    __tablename__ = 'interpret'

    #Table attributes
    i_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    born = db.Column(db.DateTime, nullable=False)

    #Database relations
    genre = db.relationship('Genre', secondary=interpret_plays_genre, lazy='subquery',
        backref=db.backref('Interpret', lazy=True))

    def __repr__(self):
        return '<Interpret %r>' % self.name
