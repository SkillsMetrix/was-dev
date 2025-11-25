#https://chatgpt.com/c/69246059-5934-832c-9334-f9fc23c5301c
import json
import base64
import traceback

def safe_json_loads(body, is_base64=False):
    if body is None:
        return {}
    try:
        if is_base64:
            body = base64.b64decode(body).decode("utf-8")
        return json.loads(body)
    except Exception:
        # try forgiving parsing (fallback) and return raw string if still fails
        return {"_raw_body": body}

def lambda_handler(event, context):
    try:
        # Helpful debug: log event (CloudWatch)
        print("EVENT:", json.dumps(event))

        http_method = event.get("httpMethod") or event.get("requestContext",{}).get("http",{}).get("method")
        # Support both REST (httpMethod) and HTTP API (requestContext.http.method)

        if http_method == "GET":
            params = event.get("queryStringParameters") or {}
            name = params.get("name", "Guest")
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"method": "GET", "message": f"Hello {name}! This is GET."})
            }

        elif http_method == "POST":
            # handle base64 and non-base64, and both REST and HTTP API shapes
            is_base64 = event.get("isBase64Encoded", False)
            body_content = event.get("body", None)
            # Some HTTP APIs put body in event["body"] too; this handles both.
            body = safe_json_loads(body_content, is_base64=is_base64)

            # handle if body is returned as a dict by safe_json_loads
            if isinstance(body, dict):
                name = body.get("name", "Guest")
                city = body.get("city", "Unknown")
            else:
                # fallback: raw string
                name = "Guest"
                city = "Unknown"

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "method": "POST",
                    "message": f"Hello {name} from {city}! This is POST.",
                    "received": body
                })
            }

        else:
            return {
                "statusCode": 405,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Method Not Allowed", "method": http_method})
            }

    except Exception as e:
        tb = traceback.format_exc()
        print("ERROR:", tb)   # visible in CloudWatch logs
        # Return the stack trace so you can see what went wrong (temporary!)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e), "trace": tb})
        }
