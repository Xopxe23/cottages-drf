import os
import requests
from cottages.models import Cottage


def yandex_suggest(search_string: str):
    key = str(os.getenv("YANDEX_SUGGEST"))
    response = requests.get(f'https://suggest-maps.yandex.ru/v1/suggest?apikey={key}&text={search_string}&types=geo')
    data = response.json()

    results = data.get('results', [])
    formatted_results = []

    for city_object in results:
        title_text = city_object.get('title', {}).get('text', '')
        subtitle_text = city_object.get('subtitle', {}).get('text', '')

        if title_text.lower().startswith(search_string.lower()):
            if subtitle_text:
                formatted_results.append({
                    "title": title_text,
                    "subtitle": subtitle_text
                })
            else:
                formatted_results.append({
                    "title": title_text
                })

    return {
        "regions": [f"{result['title']} - {result.get('subtitle', '')}" for result in formatted_results],
        "objects": formatted_results
    }


def search_cottages(search_string: str):
    cottages = Cottage.objects.filter(name__istartswith=search_string)

    result = []
    for cottage in cottages:
        name = cottage.name.lower() if cottage.name else ''
        if name.startswith(search_string.lower()):
            first_image = cottage.images.first()
            first_image_url = first_image.image.url if first_image else None

            result.append({
                "id": str(cottage.id),
                "name": cottage.name,
                "first_image": first_image_url
            })

    return result
