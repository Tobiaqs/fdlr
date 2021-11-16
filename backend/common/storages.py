from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from urllib.parse import quote
import uuid
import re


class MinioStorage(S3Boto3Storage):
    def url(self, name, parameters=None, expire=None, http_method=None):
        url = super().url(name, parameters=parameters, expire=expire, http_method=http_method)
        if settings.MINIO_EXTERNAL_URL:
            return url.replace(settings.AWS_S3_ENDPOINT_URL, settings.MINIO_EXTERNAL_URL)
        return url

    '''
    Override generated filename by prefixing it with a UUID as a "virtual" folder.
    This avoids conflicting files.
    '''

    def generate_filename(self, filename):
        return super().generate_filename(str(uuid.uuid4()) + '/' + filename)


class MinioStorageAttachment(MinioStorage):
    def get_object_parameters(self, name):
        params = super().get_object_parameters(name)

        # Take part after the last /
        original_name = name.split('/')[-1]

        # Removes all /, \ and " from the name, so that it can safely be used in headers and on many filesystems.
        original_name = re.sub(r'[\/\\\"]', '', original_name)

        params['ContentDisposition'] = f'attachment; filename="{quote(original_name)}"'
        return params


class MinioStorageInline(MinioStorage):
    def get_object_parameters(self, name):
        params = super().get_object_parameters(name)
        params['ContentDisposition'] = 'inline'
        return params
