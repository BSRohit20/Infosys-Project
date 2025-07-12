def handler(request):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": '{"message": "Nexus Hospitality System", "status": "online", "deployment": "vercel"}'
    }
