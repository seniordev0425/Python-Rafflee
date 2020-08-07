"""
    YOUTUBE API
"""

import os

from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rafflee import settings

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

YOUTUBE_CREDENTIALS = os.path.abspath(settings.YOUTUBE_JSON)

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


@api_view(['GET'])
def list_all_video(request):
    """
    API endpoint for listing all the last video on the information channel
    Args:
        request:
    Returns: HttpResponse
    """
    id = request.GET['id']
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = YOUTUBE_CREDENTIALS

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=id
    )
    response = request.execute()