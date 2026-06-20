import json
import pandas as pd
import re
from playwright.sync_api import sync_playwright, TimeoutError
from datetime import datetime

df = pd.read_excel("Contacts.xlsx")

report_data = []
excel_rows = []

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(user_data_dir="./whatsapp_profile", headless=False)

    page = context.pages[0] if context.pages else context.new_page()

    page.goto("https://web.whatsapp.com")
    page.wait_for_load_state("networkidle")

    print("WhatsApp loaded successfully")

    close_btn = page.get_by_role("button", name="Close")

    if close_btn.count() > 0:
        close_btn.click()

    for _, row in df.iterrows():

        name = str(row["Name"]).strip()
        message = str(row["Message"]).strip()

        print(f"\nSearching contact: {name}")

        try:

            search_box = page.get_by_role("textbox").first

            search_box.wait_for(timeout=10000)
            search_box.click()
            search_box.fill("")
            search_box.fill(name)

            contact = page.get_by_text(name, exact=True).first

            contact.wait_for(timeout=10000)
            contact.click()

            print(f"Opened chat: {name}")

            page.wait_for_timeout(3000)

            message_box = page.locator('[data-testid="conversation-compose-box-input"]').first
            message_box.wait_for(timeout=10000)
            message_box.click()

            message_box.press_sequentially(message)
            message_box.press("Enter")

            page.wait_for_timeout(5000)

            print(f"Message sent to: {name}")

            message_containers = page.locator('[data-testid^="conv-msg-"]')

            count = message_containers.count()

            print(f"{name} Message Count: {count}")

            incoming_messages = []

            for i in range(count):

                container = message_containers.nth(i)

                try:

                    html = container.inner_html()
                    text = container.inner_text().strip()

                    text = re.sub(r'\n\d{1,2}:\d{2}\s?(am|pm)$','',text,flags=re.IGNORECASE).strip()

                    if 'aria-label="You:' in html:
                        continue

                    if container.locator('[data-testid="sticker-container"]').count() > 0:
                        incoming_messages.append("[STICKER]")

                    elif container.locator('[data-testid="image-thumb"]').count() > 0:
                        incoming_messages.append("[IMAGE]")

                    elif text and not re.match(r'^\d{1,2}:\d{2}\s?(am|pm)$', text.lower()):
                        incoming_messages.append(text)

                    else:
                        incoming_messages.append("[UNKNOWN MESSAGE TYPE]")

                except Exception as e:
                    print(f"Error reading message {i}: {e}")

            print(f"\nIncoming Messages Count: {len(incoming_messages)}")

            last_three = incoming_messages[-3:]

            print(f"\nLast 3 incoming messages from {name}")

            for msg in last_three:
                print("----------------")
                print(msg)

            report_data.append({
                "name": name,
                "message_sent": message,
                "last_3_incoming_messages": last_three
            })

            excel_rows.append({
                "Name": name,
                "Message Sent": message,
                "Incoming Message 1": last_three[0] if len(last_three) > 0 else "",
                "Incoming Message 2": last_three[1] if len(last_three) > 1 else "",
                "Incoming Message 3": last_three[2] if len(last_three) > 2 else ""
            })

            page.wait_for_timeout(2000)

        except TimeoutError:
            print(f"Contact not found: {name}")

        except Exception as e:
            print(f"Error while processing {name}: {e}")

    date_now = datetime.now().strftime("%Y-%m-%d")
    
    with open(f"whatsapp_report_{date_now}.json", "w", encoding="utf-8") as json_file:
        json.dump(report_data, json_file, indent=4, ensure_ascii=False)

    pd.DataFrame(excel_rows).to_excel(f"whatsapp_report_{date_now}.xlsx", index=False)

    print("\nReports generated successfully")
    print(f"1. whatsapp_report_{date_now}.json")
    print(f"2. whatsapp_report_{date_now}.xlsx")

    context.close()