from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from cottages.models import Cottage


@registry.register_document
class CottageDocument(Document):
    name = fields.TextField(
        attr='name',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    town = fields.ObjectField(
        attr='town',
        properties={
            'id': fields.TextField(),
            'name': fields.TextField(
                attr='name',
                fields={
                    'raw': fields.KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            )
        }
    )

    class Index:
        name = "cottage"

    class Django:
        model = Cottage
        fields = ["id",]
