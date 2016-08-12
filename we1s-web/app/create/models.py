from mongokit import Document


class PublicationManifest(Document):
    structure = {
        'name': unicode,
        'email': unicode,
    }
    use_dot_notation = True

    def __repr__(self):
        return '<User %r>' % self.name
