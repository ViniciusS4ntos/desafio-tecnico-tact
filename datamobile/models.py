from django.db import models

class CensoCelular(models.Model):

    id = models.BigIntegerField(
        primary_key=True
    )
    grupo_idade = models.CharField()
    brasil = models.BigIntegerField()
    norte = models.BigIntegerField()
    nordeste = models.BigIntegerField()
    sudeste = models.BigIntegerField()
    sul = models.BigIntegerField()
    centro_oeste = models.BigIntegerField()

    class Meta:
        db_table = "posse_celular_2005"
        managed = False

    def __str__(self):
        return self.grupo_idade
