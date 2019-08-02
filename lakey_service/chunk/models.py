
from django.db import models
from django.core.exceptions import ValidationError

from lily.base.models import (
    array,
    boolean,
    JSONSchemaField,
    null_or,
    number,
    object,
    one_of,
    string,
    ValidatingModel,
)


class Chunk(ValidatingModel):

    created_datetime = models.DateTimeField(auto_now_add=True)

    updated_datetime = models.DateTimeField(auto_now=True)

    catalogue_item = models.ForeignKey(
        'catalogue.CatalogueItem',
        on_delete=models.CASCADE,
        related_name='chunks')

    borders = JSONSchemaField(
        schema=array(
            object(
                column=string(),
                minimum=one_of(number(), string()),
                maximum=one_of(number(), string()),
                distribution=null_or(
                    array(
                        object(
                            value_min=one_of(
                                number(),
                                string(),
                                boolean(),
                            ),
                            value_max=one_of(
                                number(),
                                string(),
                                boolean()
                            ),
                            count=number(),
                            required=['value_min', 'value_max', 'count'])
                    )
                ),
                required=['column', 'minimum', 'maximum', 'distribution'],
            )
        )
    )
    # ??? ask different types

    count = models.IntegerField(default=None)

    def borders_per_column(self, column_name):
        for chunk_border in list(self.borders):
            if chunk_border['column'] == column_name:
                return chunk_border

    def clean(self):
        self.validate_borders_in_context_of_catalogue_item()

    def validate_borders_in_context_of_catalogue_item(self):

        if isinstance(self.borders, list):

            ci_columns = set([col["name"] for col in self.catalogue_item.spec])
            borders_columns = set([
                border["column"]
                for border in self.borders])

            if not borders_columns.issubset(ci_columns):
                raise ValidationError(
                    "borders columns do not match catalogue item")

            if not ci_columns.issubset(borders_columns):
                raise ValidationError(
                    "borders columns do not match catalogue item")

            for border in self.borders:

                border_minimum = border['minimum']
                border_maximum = border['maximum']
                border_column_name = border["column"]

                if border_minimum in [None, '']:
                    raise ValidationError("minimum can not be empty")

                for b_col in self.catalogue_item.spec:
                    if border_column_name == b_col["name"]:

                        if b_col["distribution"]:
                            dist_min_values = [
                                x["value_min"]
                                for x in b_col["distribution"]]
                            catalogue_item_minimum = min(dist_min_values)

                            if border_minimum < catalogue_item_minimum:
                                raise ValidationError(
                                    'borders minimu has to be greater than'
                                    ' catalogue_item minimum')

                if border_maximum in [None, '']:
                    raise ValidationError("maximum can not be empty")

                for b_col in self.catalogue_item.spec:
                    if border_column_name == b_col["name"]:

                        if b_col["distribution"]:
                            dist_min_values = [
                                x["value_max"]
                                for x in b_col["distribution"]]
                            catalogue_item_maximum = max(dist_min_values)

                            if border_maximum > catalogue_item_maximum:
                                raise ValidationError(
                                    'borders maximum has to be greater '
                                    'than catalogue_item maximum')

                if border_minimum >= border_maximum:
                    raise ValidationError(
                        "maximum has to be greater than minimum")

        else:
            raise ValidationError(
                "chunk - borders must be created and type list")
