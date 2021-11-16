from django.db import models


class BigCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 1048576
        super().__init__(*args, **kwargs)
