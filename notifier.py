"""Twilio SMS notifier."""
from config import TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM, TWILIO_TO, MAX_SMS_LISTINGS


def _format_listing(l):
    miles = l.get("miles")
    miles_str = f"{miles:,}mi" if miles else "mi:?"
    title = l["title"][:70]
    return f"• {l['source']}: {title} [{miles_str}]\n{l['url']}"


def send(new_listings):
    if not new_listings:
        print("No new listings, skipping SMS")
        return False
    if not (TWILIO_SID and TWILIO_TOKEN and TWILIO_FROM and TWILIO_TO):
        print("Twilio creds missing — dumping to stdout instead:")
        for l in new_listings[:MAX_SMS_LISTINGS]:
            print(_format_listing(l))
        return False

    from twilio.rest import Client  # imported lazily so local dry-runs don't need it

    client = Client(TWILIO_SID, TWILIO_TOKEN)
    chunk = new_listings[:MAX_SMS_LISTINGS]
    header = f"🏁 {len(new_listings)} new R8 listing(s):"
    body = header + "\n\n" + "\n\n".join(_format_listing(l) for l in chunk)
    if len(new_listings) > MAX_SMS_LISTINGS:
        body += f"\n\n(+{len(new_listings) - MAX_SMS_LISTINGS} more not shown)"

    # SMS has a 1600 char practical ceiling; trim if needed
    if len(body) > 1500:
        body = body[:1497] + "..."

    msg = client.messages.create(body=body, from_=TWILIO_FROM, to=TWILIO_TO)
    print(f"Sent SMS {msg.sid}")
    return True
