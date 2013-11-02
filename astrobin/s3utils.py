# Django
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Third party
from storages.backends.s3boto import S3BotoStorage
from pipeline.storage import PipelineMixin


class CachedS3BotoStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(location=kwargs.pop('location'))
        self.local_storage = FileSystemStorage(location = settings.IMAGE_CACHE_DIRECTORY)

    def _save(self, name, content):
        name = super(CachedS3BotoStorage, self)._save(name, content)
        self.local_storage._save(name, content)
        return name

ImageStorage = lambda: CachedS3BotoStorage(location='images')


class S3PipelineStorage(PipelineMixin, S3BotoStorage):
    pass
StaticRootS3BotoStorage = lambda: S3PipelineStorage(location='www/static')

