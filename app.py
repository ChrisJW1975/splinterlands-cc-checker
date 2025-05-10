import streamlit as st
import requests

st.set_page_config(page_title="Splinterlands BCX Comparator")
st.title("🧮 Splinterlands Missing BCX Comparator")

username = st.text_input("Enter your Splinterlands username:")

if st.button("Compare") and username:
    with st.spinner("Fetching data..."):
        try:
            # Fetch player details and owned cards
            player_url = f"https://api.splinterlands.io/players/details?name={username}"
            player_res = requests.get(player_url)
            player_data = player_res.json()

            if 'cards' not in player_data:
                st.error("No cards found for this user.")
                st.stop()

            cards_owned = player_data.get("cards", [])

            # Filter for Rebellion cards
            rebellion_cards = [
                card for card in cards_owned if "Rebellion" in card.get("card_detail", {}).get("set", "")
            ]

            if not rebellion_cards:
                st.warning("No Rebellion cards found for this user.")
                st.stop()

            def total_bcx(cards):
                return sum(c.get("xp", 0) for c in cards)

            # Display details for each Rebellion card
            for card in rebellion_cards:
                card_info = card.get("card_detail", {})
                card_name = card_info.get("name", "Unknown")
                card_id = card_info.get("id", "Unknown")
                max_level = card_info.get("max_level", 0)
                max_bcx = max(card_info.get("xp", []), key=lambda x: x.get("level", 0))

                # BCX for the card
                owned_bcx = total_bcx([card])
                max_bcx_value = max_bcx.get("xp", 0)
                missing_bcx = max(0, max_bcx_value - owned_bcx)
                cp_per_bcx = card_info.get("dec", 0)

                missing_cp = missing_bcx * cp_per_bcx

                # Display results
                st.subheader(f"{card_name} (Rebellion)")
                st.metric("Owned BCX", owned_bcx)
                st.metric("Max BCX", max_bcx_value)
                st.metric("Missing BCX", missing_bcx)
                st.metric("Missing CP", missing_cp)

        except Exception as e:
            st.error(f"Error: {e}")
