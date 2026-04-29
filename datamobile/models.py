from django.db import models

# Create your models here.

class CensoCelular(models.Model):

    grupo_idade = models.CharField(
        max_length=100,
        primary_key=True
    )

    brasil = models.BigIntegerField()
    norte = models.BigIntegerField()
    nordeste = models.BigIntegerField()
    sudeste = models.BigIntegerField()
    sul = models.BigIntegerField()
    centro_oeste = models.BigIntegerField()

    class Meta:
        db_table = "censo_celular"
        managed = False

    def __str__(self):
        return self.grupo_idade
