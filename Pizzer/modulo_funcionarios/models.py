# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Funcionario(models.Model):  # Futuramente a classe funcionario herdara da classe pessoa
    cpf = models.CharField(max_length=20)
	
    def get_absolute_url(self):
        return '/pizzer/'