
from random import choice

from faker import Faker

from account.models import (
    Account,
    AuthRequest,
)
from catalogue.models import CatalogueItem
from downloader.models import DownloadRequest
from chunk.models import Chunk


faker = Faker()


class EntityFactory:

    def clear(self, with_predefined=True):
        Account.objects.all().delete()
        AuthRequest.objects.all().delete()
        CatalogueItem.objects.all().delete()
        Chunk.objects.all().delete()
        DownloadRequest.objects.all().delete()

    def account(self, email=None, type=None):
        return Account.objects.create(
            email=email or faker.email(),
            type=type or Account.AccountType.RESEARCHER)

    def auth_request(self, account=None):

        r = AuthRequest.objects.create()

        if account:
            r.account = account
            r.save()

        return r

    def catalogue_item(
            self,
            created_by=None,
            updated_by=None,
            maintained_by=None,
            name=None,
            sample=None,
            spec=None,
            executor_type=None):

        return CatalogueItem.objects.create(
            created_by=created_by,
            updated_by=updated_by,
            maintained_by=maintained_by,
            name=name or faker.name(),
            sample=sample or [],
            spec=spec or [
                {
                    'name': 'location',
                    'type': 'STRING',
                    'size': 190234,
                    'is_nullable': False,
                    'is_enum': False,
                    'distribution': None,
                },
                {
                    'name': 'value',
                    'type': 'FLOAT',
                    'size': None,
                    'is_nullable': True,
                    'is_enum': False,
                    'distribution': [
                        {'value_min': 18.0, 'value_max': 20.0, 'count': 9},
                        {'value_min': 22.0, 'value_max': 24.0, 'count': 21},
                        {'value_min': 25.0, 'value_max': 32.0, 'count': 49},
                    ],
                },
            ],
            executor_type=executor_type or choice(['DATABRICKS', 'ATHENA']))

    def download_request(
            self,
            created_by=None,
            spec=None,
            uri=None,
            real_size=None,
            estimated_size=None,
            catalogue_item=None,
            is_cancelled=None,
            executor_job_id=None):

        if is_cancelled is None:
            is_cancelled = False

        return DownloadRequest.objects.create(
            created_by=created_by,
            spec=spec,
            uri=uri,
            real_size=real_size,
            estimated_size=estimated_size,
            catalogue_item=catalogue_item,
            is_cancelled=is_cancelled,
            executor_job_id=executor_job_id)

    def chunk(
            self,
            created_datetime=None,
            updated_datetime=None,
            catalogue_item=None,
            borders=None,
            count=None,):
        
        return Chunk.objects.create(
            created_datetime = created_datetime,
            updated_datetime = updated_datetime,
            catalogue_item = catalogue_item,
            borders = borders or [
                    {
                        'column': 'A',
                        'minimum': 10,
                        'maximum': 15,
                    },
                    {
                        'column': 'B',
                        'minimum': 20,
                        'maximum': 25,
                    },
                ],
            count = faker.random_int(500, 100000),
            )
