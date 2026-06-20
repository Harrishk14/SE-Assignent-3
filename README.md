# Daily Report Bot

## Purpose

Daily Report Bot is a Python-based automation script that uses PyAutoGUI to generate a simple daily report by collecting content from the Times Now News website and storing it in Microsoft Excel.

The bot automates repetitive manual tasks such as:

* Launching Google Chrome
* Opening the Times Now News website
* Copying website content
* Creating a report in Microsoft Excel
* Recording the current date and time
* Adding comments to the report
* Saving the report automatically with the current date

This project demonstrates desktop GUI automation using Python and showcases how routine reporting activities can be automated without manual intervention.

## Features

* Automated browser interaction
* Automated Excel report generation
* Timestamp-based report creation
* Automatic file saving
* Simple and lightweight implementation using PyAutoGUI

## Use Case

This bot can be used as a learning project for:

* Python Automation
* GUI Automation
* Report Generation
* PyAutoGUI Practice
* Desktop Productivity Automation

## Author

Harrish Kumar G M




# WhatsApp Automated Messaging and Reporting Bot

## Overview

This automation script uses Playwright to interact with WhatsApp Web, send predefined messages to contacts listed in an Excel file, retrieve recent incoming messages from each chat, and generate summary reports in both JSON and Excel formats.

The script is designed for bulk messaging and chat monitoring workflows where message delivery and recent responses need to be tracked automatically.

---

## Features

* Reads contact names and messages from an Excel file.
* Opens WhatsApp Web using a persistent browser profile.
* Searches and opens individual chats automatically.
* Sends custom messages to each contact.
* Extracts incoming chat messages.
* Identifies special message types:

  * Text Messages
  * Stickers
  * Images
* Captures the last three incoming messages from each contact.
* Generates reports in:

  * JSON format
  * Excel format
* Handles missing contacts and unexpected errors gracefully.

---

## Input File

### Contacts.xlsx

The script expects an Excel file named `Contacts.xlsx` with the following structure:

| Name       | Message      |
| ---------- | ------------ |
| John Doe   | Hello John   |
| Jane Smith | Good Morning |

### Columns

* **Name** → WhatsApp contact name.
* **Message** → Message to be sent.

---

## Workflow

1. Launch WhatsApp Web using a persistent browser profile.
2. Load contacts from `Contacts.xlsx`.
3. Search for each contact.
4. Open the chat.
5. Send the configured message.
6. Read all available incoming messages.
7. Extract the latest three incoming messages.
8. Store results in memory.
9. Generate JSON and Excel reports.
10. Close the browser context.

---

## Message Detection

The script categorizes incoming messages as:

| Type            | Output                   |
| --------------- | ------------------------ |
| Text Message    | Actual message text      |
| Sticker         | `[STICKER]`              |
| Image           | `[IMAGE]`                |
| Unknown Content | `[UNKNOWN MESSAGE TYPE]` |

Outgoing messages sent by the automation are ignored while generating reports.

---

## Output Files

Reports are generated using the current date.

### JSON Report

```text
whatsapp_report_YYYY-MM-DD.json
```

Example:

```json
[
    {
        "name": "John Doe",
        "message_sent": "Hello",
        "last_3_incoming_messages": [
            "Hi",
            "How are you?",
            "[STICKER]"
        ]
    }
]
```

### Excel Report

```text
whatsapp_report_YYYY-MM-DD.xlsx
```

Example:

| Name     | Message Sent | Incoming Message 1 | Incoming Message 2 | Incoming Message 3 |
| -------- | ------------ | ------------------ | ------------------ | ------------------ |
| John Doe | Hello        | Hi                 | How are you?       | [STICKER]          |

---

## Error Handling

The script handles:

* Contact not found scenarios.
* Message extraction failures.
* WhatsApp loading delays.
* Unexpected runtime exceptions.

Processing continues even if an individual contact fails.

---

## Use Cases

* Customer follow-up campaigns.
* Bulk WhatsApp communication.
* Response tracking.
* Contact engagement monitoring.
* Automated chat reporting.

---

## Generated Reports

After successful execution:

```text
Reports generated successfully

1. whatsapp_report_YYYY-MM-DD.json
2. whatsapp_report_YYYY-MM-DD.xlsx
```

These reports provide a summary of messages sent and the latest responses received from each contact.

