from typing import Dict

from app.models import Exchange


class CompanyInformation:
    def __init__(self, data: Dict):
        self.exchange = data["General"]["Exchange"]
        self.sector = data["General"]["Sector"]
        self.industry = data["General"]["Industry"]

    def get_exchange(self):
        exchange = self.exchange
        return Exchange.objects.get(name=exchange)

    def get_sector(self):
        return self.sector

    def get_industry(self):
        return self.industry
