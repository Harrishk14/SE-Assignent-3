import json
import pandas as pd
import re
from playwright.sync_api import sync_playwright, TimeoutError

# Read Contacts.xlsx
df = pd.read_excel("Contacts.xlsx")

# Report containers
report_data = []
excel_rows = []

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        user_data_dir="./whatsapp_profile",
        headless=False
    )

    page = context.pages[0] if context.pages else context.new_page()

    page.goto("https://web.whatsapp.com")

    page.wait_for_load_state("networkidle")

    print("WhatsApp loaded successfully")

    # Close popup if available
    close_btn = page.get_by_role("button", name="Close")

    if close_btn.count() > 0:
        close_btn.click()

    for _, row in df.iterrows():

        name = str(row["Name"]).strip()
        message = str(row["Message"]).strip()

        print(f"\nSearching contact: {name}")

        try:

            # Search contact
            search_box = page.get_by_role("textbox").first

            search_box.wait_for(timeout=10000)

            search_box.click()
            search_box.fill("")
            search_box.fill(name)

            contact = page.get_by_text(
                name,
                exact=True
            ).first

            contact.wait_for(timeout=10000)

            contact.click()

            print(f"Opened chat: {name}")

            page.wait_for_timeout(3000)

            message_containers = page.locator(
                '[data-testid^="conv-msg-"]'
            )

            count = message_containers.count()

            print(f"{name} Message Count: {count}")

            incoming_messages = []

            time_pattern = r'^\d{1,2}:\d{2}\s?(am|pm)$'

            for i in range(count):

                container = message_containers.nth(i)

                try:

                    html = container.inner_html()

                    # Skip messages sent by you
                    if 'aria-label="You:' in html:
                        continue

                    text = container.inner_text().strip()

                    print("\n====================")
                    print(f"Message Index: {i}")
                    print(repr(text))
                    print("====================")

                    # Normal text message
                    if text and not re.match(
                        time_pattern,
                        text.lower()
                    ):
                        incoming_messages.append(text)

                    # Timestamp-only message
                    elif re.match(
                        time_pattern,
                        text.lower()
                    ):

                        debug_file = (
                            f"possible_media_{name}_{i}.html"
                            .replace(" ", "_")
                        )

                        with open(
                            debug_file,
                            "w",
                            encoding="utf-8"
                        ) as f:

                            f.write(
                                container.evaluate(
                                    "e => e.outerHTML"
                                )
                            )

                        print(
                            f"Possible media detected. "
                            f"Saved to {debug_file}"
                        )

                        incoming_messages.append(
                            "[MEDIA MESSAGE]"
                        )

                    else:

                        debug_file = (
                            f"unknown_{name}_{i}.html"
                            .replace(" ", "_")
                        )

                        with open(
                            debug_file,
                            "w",
                            encoding="utf-8"
                        ) as f:

                            f.write(
                                container.evaluate(
                                    "e => e.outerHTML"
                                )
                            )

                        print(
                            f"Unknown message detected. "
                            f"Saved to {debug_file}"
                        )

                        incoming_messages.append(
                            "[UNKNOWN MESSAGE TYPE]"
                        )

                except Exception as e:

                    print(
                        f"Error reading message "
                        f"{i}: {e}"
                    )

            print(
                f"\nIncoming Messages Count: "
                f"{len(incoming_messages)}"
            )

            last_three = incoming_messages[-3:]

            print(
                f"\nLast 3 incoming messages "
                f"from {name}"
            )

            for msg in last_three:

                print("----------------")
                print(msg)

            # JSON report entry
            report_data.append({
                "name": name,
                "message_sent": message,
                "last_3_messages": last_three
            })

            # Excel report entry
            excel_rows.append({
                "Name": name,
                "Message Sent": message,
                "Last Message 1":
                    last_three[0]
                    if len(last_three) > 0
                    else "",
                "Last Message 2":
                    last_three[1]
                    if len(last_three) > 1
                    else "",
                "Last Message 3":
                    last_three[2]
                    if len(last_three) > 2
                    else ""
            })

            '''
            Uncomment if you want to send messages

            message_box = page.locator(
                '[data-testid="conversation-compose-box-input"]'
            )

            message_box.wait_for(
                timeout=10000
            )

            message_box.click()

            message_box.press_sequentially(
                message
            )

            message_box.press("Enter")

            print(
                f"Message sent to: {name}"
            )
            '''

            page.wait_for_timeout(2000)

        except TimeoutError:

            print(
                f"Contact not found: {name}"
            )

        except Exception as e:

            print(
                f"Error while processing "
                f"{name}: {e}"
            )

    # Save JSON reportcls
    with open(
        "whatsapp_report.json",
        "w",
        encoding="utf-8"
    ) as json_file:

        json.dump(
            report_data,
            json_file,
            indent=4,
            ensure_ascii=False
        )

    # Save Excel report
    report_df = pd.DataFrame(
        excel_rows
    )

    report_df.to_excel(
        "whatsapp_report.xlsx",
        index=False
    )

    print(
        "\nReports generated successfully"
    )

    print(
        "1. whatsapp_report.json"
    )

    print(
        "2. whatsapp_report.xlsx"
    )

    context.close()