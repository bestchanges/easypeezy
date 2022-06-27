# Requiremtnts for UI

# Main flow

1. User see main page
2. He fills
   1. enter value of amount
   2. selects source currency
   3. selects target currency
   4. presses "Convert"
3. Responce page:
   1. Summary information
      1. input amount
      2. single select source currency
      3. multiple select source platform (banks)
      4. single select source country (optional)
      5. single select target currency
      6. multiple select target platform (banks)
      7. single select target country (optional)
      8. best conversion amount
      9. "Display top-10 from found {len(ways)}"
   2. Expandable list of selected ways. For each way:
      1. Short path like EUR-USDT-RUB
      2. Target amount (summary conversion rate)
   3. Expanded 1st way. List of transfers:
      1. from amount, currency 
      2. to amount, currency
      3. Platform (link)
      4. Commissions (in source currency, % of total amount)