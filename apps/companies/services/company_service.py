from ..repositories import CompanyRepository
from ..models import Company

class CompanyService:
    def __init__(self):
        self.repo = CompanyRepository(Company)

    def list_items(self):
        return self.repo.get_all()

    def get_item(self, pk):
        return self.repo.get_by_id(pk)
