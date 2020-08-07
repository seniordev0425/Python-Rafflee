"""
    Admin class for the promotion numbers analytics table
"""

from django.contrib import admin


class PromotionNumbersAdmin(admin.ModelAdmin):
    """
    Admin class for the promotion numbers analytics
    """

    list_display = (
        'promotion',
        'click_views',
        'click_actions',
        'click_participations',
        'number_of_followers',
        'click_views_total',
        'click_actions_total',
        'click_participations_total',
        'product_benefit_by_view',
        'product_benefit_by_action',
        'product_benefit_by_participations',
        'product_benefit_by_total',
        'product_benefit_followers',
        'start_date'
    )

    list_filter = (
        'promotion',
    )

    search_fields = ('promotion',)