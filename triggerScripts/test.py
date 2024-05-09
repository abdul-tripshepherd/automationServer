import json

# JSON data
json_data = """
{
    "headers": [
        {
            "name": "Content-Type",
            "value": "application/json"
        },
        {
            "name": "User-Agent",
            "value": "hasura-graphql-engine/v2.14.0"
        }
    ],
    "payload": {
        "created_at": "2024-05-09T08:03:05.402964Z",
        "delivery_info": {
            "current_retry": 0,
            "max_retries": 0
        },
        "event": {
            "data": {
                "new": {
                    "author": null,
                    "canonical": "wwwwww",
                    "category": null,
                    "content": null,
                    "created_at": "2024-05-09T08:03:05.409+00:00",
                    "created_by": null,
                    "header": null,
                    "id": 580,
                    "meta_description": "Discover why May is the perfect time to explore Fort Lauderdale's sunny shores, lively music scene, and exciting events. From beach bliss to cultural gems, find out all you need to know for an unforgettable trip with Tripshepherd.",
                    "page_title": null,
                    "publication_date": null,
                    "published_at": null,
                    "slug": null,
                    "snippet": null,
                    "subheader": null,
                    "updated_at": "2024-05-09T08:03:05.409+00:00",
                    "updated_by": null
                },
                "old": null
            },
            "op": "INSERT",
            "session_variables": null,
            "trace_context": null
        },
        "id": "28a9b42c-2695-492a-9012-46ef83478e63",
        "table": {
            "name": "blogs",
            "schema": "strapi"
        },
        "trigger": {
            "name": "automated_testing_new_blog"
        }
    },
    "version": "2"
}
"""

# Parse JSON string into a Python dictionary
data_dict = json.loads(json_data)

# Access the value of 'canonical' under 'event > data'
canonical_value = data_dict['payload']['event']['data']['new']['canonical']

print("Canonical Value:", canonical_value)
