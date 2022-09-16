"""Hotel models"""
from sql_alchemy import banco


class SiteModel(banco.Model):
    # mapeamento para o SQLAlquemy
    __tablename__ = "sites"

    # mapeamento para o SQLAlquemy
    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')

    def __init__(self, site_id, url):
        self.site_id = site_id
        self.url = url

    def json(self):
        """Return data in JSON format"""
        return {
            "site_id": self.site_id,
            "url": self.url,
        }

    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return None

    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_site(self):
        banco.session.delete(self)
        banco.session.commit()
