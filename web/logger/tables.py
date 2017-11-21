from django.utils.html import format_html
from logger.models import User
import django_tables2 as tables

class UserTable(tables.Table):

    def render_card_id(self, value):
        return format_html('<a href="{}">{}</a>', value, value)

    class Meta:
        model = User

class DayTable(tables.Table):
    user = tables.Column()
    absence = tables.Column()

    # def order_user(self, queryset, is_descending):
    #     queryset = queryset.annotate(
    #         name='user.first_name'
    #     ).order_by(('-' if is_descending else '') + 'name')
    #     return (queryset, True)

    def render_user(self, value):
        return format_html('<a href="{}">{}</a>', 
                    "/logger/user/"+str(value.card_id),
                    value.first_name.capitalize()+" "+value.last_name.capitalize())

    def order_user(self, queryset, is_descending):
        queryset = queryset.order_by(('-' if is_descending else '') + 'first_name')
        return (queryset, True)
