import re
import pandas as pd

# Raw chat data
chat_data = """
[2/7/23, 07:06:17] Aayaraa 🤝 Casagrand: ‎Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.
[2/7/23, 07:06:17] Babu  Anna : ‎Babu  Anna  created this group
[10/27/23, 21:32:01] Babu  Anna : ‎Babu  Anna  Added You to a Group in the Community: Aayaraa foods- Dairy
[10/27/23, 21:32:01] Aayaraa 🤝 Casagrand: ‎‎Disappearing messages were turned on. ‎New messages will disappear from this chat ‎7 days after they're sent, except when kept.
[10/29/23, 10:12:11] ~ Sudharshanan Periyaswamy😎: ‎Babu  Anna  added ~ Sudharshanan Periyaswamy😎
[11/16/23, 21:12:11] ~ sowkarthikaa k: ‎Babu  Anna  added ~ sowkarthikaa k
[11/19/23, 01:23:48] ~ MinnieSaju: ‎Babu  Anna  added ~ MinnieSaju
[12/14/23, 22:54:56] ~ Prabha: ‎~ Sreeja Vijayanathan added ~ Prabha
[7/5/24, 09:15:30] ~ Aayaraa Foods: ‎Waiting for this message. This may take a while.
[10/26/24, 21:41:27] ‪+91 81487 93891‬: ‎~ Prabha added ‪+91 81487 93891‬
[12/25/24, 20:18:25] Babu  Anna : Hi, Greetings from Aayaraa!  
A fresh batch of home-style paneer and curd from fresh wholesome milk, crafted and ready to deliver on *Friday 27/12/24*. Do let us know your requirements here. Thank you for your continued support.
[12/25/24, 20:21:44] ~ MinnieSaju: Curd..1/2 l...3 boxes
V22
[12/26/24, 04:42:56] ~ Uma Vijay: Curd-1 litre - 5
Paneer -1
V105
[12/26/24, 06:27:50] ~ Shanthi: Curd -1/2l - 2
V86
[12/26/24, 20:58:25] Babu  Anna : We should be delivering between 11.30 to 12.00
[12/26/24, 21:04:00] ~ Sujatha Ramesh: I missed to order. Can u deliver curd - 1/2 ltr - 1 pack for villa 23
[12/26/24, 21:05:10] ~ Dhivya Ayyappan: If possible, for villa 32 also.. 1/2 ltr curd 1 pack...

"""

# Step 1: Combine multi-line messages
combined_messages = []
current_message = ""

# Regex to identify the start of a new message
timestamp_pattern = r"^\[\d{2}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2}\]"

for line in chat_data.splitlines():
    if re.match(timestamp_pattern, line):  # New message detected
        if current_message:
            combined_messages.append(current_message.strip())
        current_message = line  # Start a new message
    else:
        current_message += " " + line  # Append to the current message

# Add the last message if present
if current_message:
    combined_messages.append(current_message.strip())


# Step 2: Extract data from combined messages
data = []
date_pattern=r"(\d{2}/\d{2}/\d{2})"
name_pattern = r"~\s?([\w\s]+):"
product_pattern = r"(curd|paneer)"
weight_pattern = r"(\d+(?:/\d+)?\s?(?:l|litres?|L))"
quantity_pattern = r"-?\s?(\d+\s+)(?!.*\bl|litres?|L\b)"
address_pattern = r"\b(villa\s*\d+|V\d+|v\d+)\b"

for message in combined_messages:
 
    date_match=re.search(date_pattern,message)
    message=re.sub(timestamp_pattern,"_",message)
   

    name_match = re.search(name_pattern, message)
    product_match = re.findall(product_pattern, message, re.IGNORECASE)
    weight_match = re.findall(weight_pattern, message, re.IGNORECASE)
    quantity_match = re.findall(quantity_pattern, message)
    address_match = re.search(address_pattern, message, re.IGNORECASE)
    
    if name_match and product_match:
      for i, Product in enumerate(product_match):
          date = date_match.group(1).strip()
          name = name_match.group(1).strip()
          
          # Check if weight_match[i] exists and is not None
          try:
            # Attempt to process weight_match[i]
            weight = weight_match[i].lower().replace("litres", "").replace("l", "").replace("litre","").replace("ltr","")
            
            
          except IndexError:
            # If index is out of bounds, assign 1 as default value
            weight = "-"
          
          try:
             quantity=quantity_match[i]
          except IndexError:
             quantity="1"
          address = address_match[0] if address_match else None

          data.append({
              "Date": date,
              "Name": name,
              "Product": Product,
              "Weight": weight,
              "Quantity": quantity,
              "Address": address
          })

# Step 3: Create DataFrame and Export
df = pd.DataFrame(data)
df.to_excel("whatsapp_orders_combined.xlsx", index=False)

print(df)

