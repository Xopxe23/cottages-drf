from .service import yandex_suggest, search_cottages
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["GET"])
def get_suggestion(request: Request):
    search_string = request.query_params.get("text")
    if not search_string:
        return Response({"error": "No search string provided"}, status=400)

    yandex_results = yandex_suggest(search_string)

    cottages_results = search_cottages(search_string)

    return Response({
        "data": {
            "regions": yandex_results.get("regions", []),
            "objects": cottages_results
        }
    })
