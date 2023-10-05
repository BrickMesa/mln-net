from django.db import models

class DarkflameDBManager(models.Manager):
    def get_queryset(self):
        query = super().get_queryset()

        if hasattr(self.model, 'database'):
            query = query.using(self.model.database)

        return query
    
class DarkflameDBModel(models.Model):
    database = "darkflame"
    objects = DarkflameDBManager()
    
    class Meta:
        abstract = True

