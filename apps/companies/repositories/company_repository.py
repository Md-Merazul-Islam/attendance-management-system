class CompanyRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, pk):
        return self.model.objects.filter(pk=pk).first()
