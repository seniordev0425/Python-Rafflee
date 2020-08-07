"""Rafflee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from account.views import authentication, registration, informations, accounts
from promotion.views import list_promotions, promotion_creation, categories
from favorite.views import favorite, homepage
from coupon.views import participate_coupon
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token
from social_network.views import social_wall
from company.views import company, bills
from analytics.views import analytics
from tools import twilio

from report.views import report_creation
from analytics.tasks import creation_product_benefit_analytics, check_social_followers, renew_token

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', authentication.login, name='login'),
    path('login/facebook/', authentication.login_facebook, name='login_facebook'),
    path('login/google/', authentication.login_google, name='login_google'),
    path('twitter/connect/<int:step>/', authentication.url_connect_twitter),
    path('twitch/connect/<str:version>/', authentication.url_connect_twitch),
    path('snapchat/connect/<int:step>/', authentication.url_connect_snapchat),
    path('instagram/connect/', authentication.url_connect_instagram),
    path('facebook/connect/', authentication.url_connect_facebook),
    path('facebook/connect/instagram_business/', authentication.url_connect_instagram_business),
    path('facebook/connect/instagram_business/validation/', authentication.url_connect_instagram_business_validation),
    path('logout/', authentication.logout, name='logout'),
    # path('login/professional/', authentication.login_professional, name='login_professional'),

    path('account/password/reset/email/', accounts.send_reset_password, name='send_email_reset_password'),
    path('account/password/reset/', accounts.reset_password, name='reset_password'),
    path('account/password/update/', accounts.update_password, name='update_password'),

    #TWILIO VERIFICATION
    path('account/number/send-sms/', twilio.send_confirmation_number_sms, name='send_confirmation_sms'),
    path('account/number/verification/', twilio.verification_code_sms, name='verification_sms'),

    path('account/wall/', social_wall.my_social_wall),
    path('account/wall/settings/', promotion_creation.settings_wall),
    path('company/wall/<int:id>/', social_wall.company_social_wall),

    path('account/register/', registration.register_particular, name='register'),

    path('account/profile/activate/<int:pk>/<str:token>/', registration.activate),
    path('account/profile/deactivate/', registration.deactivate_profile_endpoint),
    path('account/email/delete/<int:pk>/<str:token>/', registration.delete_profile_email_endpoint),

    path('account/result/<int:id>/', participate_coupon.get_result_by_promotion, name='result_giveaway'),

    path('account/follow/<int:id>/', promotion_creation.subscription_company_page),
    path('account/unfollow/<int:id>/', promotion_creation.unfollow_company_page),


    path('account/profile/update/', informations.update_information, name='user_profile_update'),
    path('account/profile/', informations.retrieve_informations, name='user_profile'),
    path('account/profile/username/', informations.check_username_exist, name='check_username'),

    path('company/register/', registration.register_professional, name='register_professional'),
    path('company/contact-form/', company.registration_contact, name='register_contact'),

    path('company/profile/update/', company.update_company_information, name='company_profile_update'),
    path('company/<int:id>/', company.get_company, name='get_company'),
    path('company/profile/', company.retrieve_company_informations, name='company_profile'),
    path('company/campaign/', company.retrieve_company_campaign, name='company_campaign'),
    path('company/campaign/<int:id>/', company.get_promotion),
    path('company/bills/', bills.get_bills),
    path('company/bill/<int:id>/', bills.get_bill_with_pdf),

    path('analytics/followers/<str:time>/', analytics.followers),
    path('analytics/click/<int:id>/<str:time>/', analytics.clicks),
    path('analytics/gender/<str:id>/', analytics.gender),
    path('analytics/map/<str:id>/<str:type>/', analytics.map),
    path('analytics/age/<str:id>/<str:type>/', analytics.range_age),

    path('categories/', categories.get_categories, name='get_categories'),

    # Promotions routes
    path('campaign/close/', list_promotions.close_promotion),

    path('campaign/all-campaigns/informations/', list_promotions.campaign_id),
    path('campaign/all-campaigns/', list_promotions.homepage_promotion),
    path('campaign/<int:id>/', list_promotions.get_promotion),
    path('campaign/user/inventory/', list_promotions.prizes_inventory),
    path('campaign/user/in-progress/', list_promotions.get_my_promotions_in_progress),
    path('campaign/user/historical/', list_promotions.get_history_promotion),
    path('campaign/prizes/details/<int:id>/<str:name>/', list_promotions.get_prizes_details),

    path('campaign/participate/', participate_coupon.participate),

    path('campaign/participate/twitter/tweet/', participate_coupon.twitter_tweet),
    path('campaign/participate/twitter/tweet/validation/', participate_coupon.twitter_tweet_validation),
    path('campaign/participate/twitter/retweet/', participate_coupon.twitter_retweet),
    path('campaign/participate/twitter/retweet/validation/', participate_coupon.twitter_retweet_validation),
    path('campaign/participate/twitter/follow/', participate_coupon.twitter_follow),
    path('campaign/participate/twitter/follow/validation/', participate_coupon.twitter_follow_validation),
    path('campaign/participate/twitter/like/', participate_coupon.twitter_like),
    path('campaign/participate/twitter/like/validation/', participate_coupon.twitter_like_validation),
    path('campaign/participate/twitch/follow/', participate_coupon.twitch_follow),
    path('campaign/participate/twitch/follow/validation/', participate_coupon.twitch_follow_validation),
    path('campaign/participate/instagram/publication/', participate_coupon.instagram_publication),
    path('campaign/participate/instagram/profile/', participate_coupon.instagram_profile),
    path('campaign/participate/facebook/url/', participate_coupon.facebook_url),
    path('campaign/participate/facebook/page/', participate_coupon.facebook_page),
    path('campaign/participate/facebook/post/', participate_coupon.facebook_post),

    path('campaign/participate/url_video/', participate_coupon.url_video),
    path('campaign/participate/url_website/', participate_coupon.url_website),
    path('campaign/participate/poll/', participate_coupon.poll),

    path('campaign/participate/subscription/<int:id>/', promotion_creation.subscription),
    path('campaign/create/', promotion_creation.create_promotion),
    path('campaign/live/<int:pk>/', promotion_creation.live_draw),
    path('campaign/live/pick/<int:pk>/', promotion_creation.live_draw_by_giveaway),
    path('campaign/live/all/<int:pk>/', promotion_creation.live_draw_all_by_giveaway),
    path('campaign/live/finish/<int:pk>/', promotion_creation.live_draw_all_finish),
    path('campaign/live/get-winnings/<int:pk>/', promotion_creation.get_winnings),
    path('campaign/participants/<int:pk>/', promotion_creation.get_all_participants),

    path('favorites/campaign/', favorite.list_favorites_campaign),
    path('favorites/company/', favorite.list_favorites_company),
    path('favorites/update/campaign/', favorite.update_favorite),
    path('favorites/remove/newsletter/', favorite.remove_newsletter),
    path('favorites/remove/follow/', favorite.remove_follow),

    path('homepage/new/', homepage.new),
    path('homepage/end-soon/', homepage.end_soon),
    path('homepage/hot/', homepage.hot),
    path('homepage/highlights/', homepage.highlights),

    #    path('token/', obtain_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('token/verify/', verify_jwt_token),

    path('twitter/users/search/', promotion_creation.twitter_search_users),
    path('facebook/page/search/', promotion_creation.facebook_search_page),
    path('facebook/publication/search/', promotion_creation.facebook_search_publication),


    path('test/', creation_product_benefit_analytics),

    path('beta/report/', report_creation.creation_report_test),

    # Youtube routes
#    path('social-network/youtube/list-video/', list_all_video),
]
