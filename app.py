import streamlit as st
import requests

st.set_page_config(page_title="Splinterlands BCX Comparator")
st.title("🧮 Splinterlands Missing BCX Comparator")

username = st.text_input("Enter your Splinterlands username:")
card_id = st.text_input("Enter Card ID:")

if st.button("Compare") and username and card_id:
    with st.spinner("Fetching data..."):
        try:
            player_url = f"https://api.splinterlands.io/players/details?name={username}"
            card_url = f"https://api.splinterlands.io/cards/find?ids[]={card_id}"

            player_res = requests.get(player_url)
            card_res = requests.get(card_url)

            player_data = player_res.json()
            card_data = card_res.json()

            cards_owned = [c for c in player_data.get("cards", []) if str(c.get("card_detail_id")) == card_id]
            regular_cards = [c for c in cards_owned if not c.get("gold", False)]
            gold_cards = [c for c in cards_owned if c.get("gold", False)]

            def total_bcx(cards):
                return sum(c.get("xp", 0) for c in cards)

            reg_bcx = total_bcx(regular_cards)
            gold_bcx = total_bcx(gold_cards)

            card_info = card_data[0]

            max_reg = next((x["xp"] for x in card_info["xp"] if x["level"] == card_info["max_level"] and not x["gold"]), 0)
            max_gold = next((x["xp"] for x in card_info["xp"] if x["level"] == card_info["max_level"] and x["gold"]), 0)

            cp_per_bcx = card_info.get("dec", 0)

            reg_missing = max(0, max_reg - reg_bcx)
            gold_missing = max(0, max_gold - gold_bcx)

            reg_cp = reg_missing * cp_per_bcx
            gold_cp = gold_missing * cp_per_bcx * 1.5  # Estimate multiplier

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Regular Foil")
                st.metric("Owned BCX", reg_bcx)
                st.metric("Max BCX", max_reg)
                st.metric("Missing BCX", reg_missing)
                st.metric("Missing CP", reg_cp)

            with col2:
                st.subheader("Gold Foil")
                st.metric("Owned BCX", gold_bcx)
                st.metric("Max BCX", max_gold)
                st.metric("Missing BCX", gold_missing)
                st.metric("Missing CP", gold_cp)

        except Exception as e:
            st.error(f"Error: {e}")
