from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from cottages.models import Cottage
from towns.models import Town


@registry.register_document
class CottageDocument(Document):
    name = fields.TextField(
        attr='name',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    town_name = fields.TextField(
        attr='town.name',
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    class Index:
        name = "cottage"

    class Django:
        model = Cottage
        fields = ["id",]


@registry.register_document
class TownDocument(Document):
    name = fields.TextField(
        attr='name',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )

    class Index:
        name = "town"

    class Django:
        model = Town
        fields = ["id",]
