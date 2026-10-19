import streamlit as st
import random
import datetime
import hashlib
import urllib.request
import urllib.parse
import json
import io
import math
from PIL import Image, ImageDraw, ImageOps
from google import genai

# ==========================================
# 0. PAGE CONFIG & API KEY SETUP
# ==========================================
st.set_page_config(page_title="The Karmic Path", layout="wide")

# Direct key for local testing (Change to st.secrets["GEMINI_API_KEY"] before GitHub upload)
# Fetches the key securely from the Streamlit Cloud environment
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
st.markdown("""
<style>
div[data-testid="stImage"] img {
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
div[data-testid="stImage"] img:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 28px rgba(212, 175, 55, 0.35);
}
.card-desc-box {
    background-color: rgba(255, 255, 255, 0.04);
    border-left: 3px solid #D4AF37;
    padding: 14px;
    border-radius: 8px;
    font-size: 0.95rem;
    line-height: 1.6;
    text-align: justify;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. BULLETPROOF KRISHNA CARD RENDERER
# ==========================================
HEADERS = {"User-Agent": "KarmicPathOracleApp/1.0 (https://streamlit.io)"}

def fetch_wikimedia_artwork(wiki_titles, commons_query):
    """Fetches real Krishna artwork bytes from Wikipedia/Wikimedia APIs."""
    for title in wiki_titles:
        try:
            encoded_title = urllib.parse.quote(title)
            api_url = (
                "https://en.wikipedia.org/w/api.php?action=query"
                f"&titles={encoded_title}&prop=pageimages&format=json"
                "&pithumbsize=600&redirects=1"
            )
            req = urllib.request.Request(api_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                pages = data.get("query", {}).get("pages", {})
                for page in pages.values():
                    thumb_url = page.get("thumbnail", {}).get("source")
                    if thumb_url:
                        img_req = urllib.request.Request(thumb_url, headers=HEADERS)
                        with urllib.request.urlopen(img_req, timeout=6) as img_resp:
                            return Image.open(io.BytesIO(img_resp.read())).convert("RGB")
        except Exception:
            continue

    try:
        encoded_q = urllib.parse.quote(f"filetype:bitmap {commons_query}")
        commons_api = (
            "https://commons.wikimedia.org/w/api.php?action=query"
            f"&generator=search&gsrsearch={encoded_q}&gsrnamespace=6&gsrlimit=5"
            "&prop=imageinfo&iiprop=url&iiurlwidth=600&format=json"
        )
        req = urllib.request.Request(commons_api, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for page in pages.values():
                info = page.get("imageinfo", [{}])[0]
                img_url = info.get("thumburl") or info.get("url")
                if img_url:
                    img_req = urllib.request.Request(img_url, headers=HEADERS)
                    with urllib.request.urlopen(img_req, timeout=6) as img_resp:
                        return Image.open(io.BytesIO(img_resp.read())).convert("RGB")
    except Exception:
        pass

    return None

@st.cache_data(show_spinner=False)
def build_card_image(name, wiki_titles, commons_query):
    """Frames every Krishna painting into a unified 450x620 Vedic Golden Deck Card."""
    width, height = 450, 620
    canvas = Image.new("RGB", (width, height), (15, 20, 38))
    draw = ImageDraw.Draw(canvas)

    art = fetch_wikimedia_artwork(wiki_titles, commons_query)
    if art:
        fitted_art = ImageOps.fit(art, (406, 576), method=Image.Resampling.LANCZOS)
        canvas.paste(fitted_art, (22, 22))
    else:
        cx, cy = width // 2, height // 2
        for r in range(200, 20, -15):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(212, 175, 55), width=2)
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            x2 = cx + int(190 * math.cos(rad))
            y2 = cy + int(190 * math.sin(rad))
            draw.line([cx, cy, x2, y2], fill=(180, 140, 40), width=1)

    draw.rectangle([8, 8, width - 9, height - 9], outline=(212, 175, 55), width=4)
    draw.rectangle([18, 18, width - 19, height - 19], outline=(245, 215, 110), width=2)
    return canvas

# ==========================================
# 2. KRISHNA KARMIC DECK & 200-WORD LORE
# ==========================================
class KarmicCard:
    def __init__(self, name, theme, wiki_titles, commons_query, description):
        self.name = name
        self.theme = theme
        self.wiki_titles = wiki_titles
        self.commons_query = commons_query
        self.description = " ".join(description.split())

class KrishnaDeck:
    def __init__(self):
        self.cards = []
        self.build_deck()

    def build_deck(self):
        self.cards = [
            KarmicCard(
                name="The Flute Player (Muralidhara)",
                theme="Harmony, Divine Calling & Inner Peace",
                wiki_titles=["Krishna", "Svayam_Bhagavan"],
                commons_query="Krishna playing flute painting",
                description="""
                The Flute Player represents the sacred call of the soul toward inner stillness,
                creative flow, and effortless alignment. In the spiritual tradition of Vrindavan,
                Krishna's bamboo flute is completely hollow—symbolizing a mind emptied of ego,
                stubbornness, and anxious resistance so that cosmic breath can pass through it as
                pure melody. When this archetype appears in your Karmic Signature, it reveals that
                your deepest strength does not come from forcing outcomes or fighting against the
                current of life, but from tuning yourself to a higher internal frequency. You
                possess a natural magnetism that draws people, opportunities, and healing energy
                toward you whenever you act from a place of authenticity and peace. However, the
                lesson of the flute asks you to release mental clutter and control. Whenever you
                feel overwhelmed by external noise or worldly expectations, this card reminds you
                to step back into silence, listen to your intuition, and trust the unseen rhythm
                guiding your path. Your soul is meant to bring harmony to chaotic spaces, turning
                life's raw experiences into wisdom, grace, and emotional resonance.
                """
            ),
            KarmicCard(
                name="The Divine Charioteer (Parthasarathy)",
                theme="Guidance, Duty & Righteous Action",
                wiki_titles=["Bhagavad_Gita", "Kurukshetra_War"],
                commons_query="Krishna Arjuna chariot Kurukshetra painting",
                description="""
                The Divine Charioteer captures the iconic moment on the battlefield of Kurukshetra
                where Krishna takes the reins of Arjuna's chariot, steering him through doubt,
                moral paralysis, and emotional turmoil. In your Karmic Signature, this archetype
                signifies mastery over the mind, unwavering courage, and the call to fulfill your
                highest Dharma without attachment to fear or applause. In Vedic philosophy, the
                chariot represents the physical body, the wild horses represent the restless
                senses, the reins are the disciplined mind, and the Charioteer is awakened higher
                intelligence. Drawing this card indicates that you are built to navigate complex
                life crossroads and carry significant responsibilities with integrity. You are not
                meant to shrink back when life demands tough decisions. Instead, this archetype
                teaches Nishkama Karma—performing your duty with total excellence and devotion
                while surrendering anxiety over the final result. Whether in your studies, career,
                or personal battles, trust that you have the inner clarity to hold the reins
                steady, cut through illusion, and move forward with fearless purpose.
                """
            ),
            KarmicCard(
                name="The Butter Thief (Makhan Chor)",
                theme="Joy, Playfulness & Innocent Mischief",
                wiki_titles=["Bala_Krishna", "Yashoda"],
                commons_query="Bal Krishna butter painting",
                description="""
                The Butter Thief celebrates the radiant, untamed spirit of young Bala Krishna, who
                playfully breaks into the clay pots of Vrindavan to steal fresh white butter. In
                spiritual symbolism, churned butter represents the purest essence of devotion and
                joy distilled from the mind, and Krishna steals it to remind humanity that the
                divine prefers a soft, loving, and spontaneous heart over rigid rules and cold
                perfectionism. When this card anchors your Karmic Signature, it is a powerful
                reminder not to let heavy ambitions, harsh self-criticism, or worldly cynicism
                harden your spirit. You carry a spark of creative rebellion and childlike wonder
                that can break through stale routines and outdated limitations. Life is not meant
                to be treated solely as a grim test of endurance; it is also Lila—a sacred, joyful
                play. This archetype encourages you to reconnect with curiosity, laughter, and
                creative experimentation. By approaching your goals with lightness rather than
                crushing pressure, you unlock unexpected breakthroughs and keep your emotional
                energy vibrant, resilient, and deeply alive.
                """
            ),
            KarmicCard(
                name="The Eternal Lovers (Radha Madhava)",
                theme="Devotion, Soul Connection & Wholeheartedness",
                wiki_titles=["Radha_Krishna", "Gita_Govinda"],
                commons_query="Radha Krishna miniature painting",
                description="""
                The Eternal Lovers embodies the supreme synthesis of consciousness and energy,
                where the individual soul and the universal spirit mirror one another in complete
                devotion. Beyond conventional romance, Radha and Krishna represent the power of
                Bhakti—giving your whole heart to what you love, what you create, and what you
                believe in without holding back out of fear. In your Karmic Signature, this card
                reveals a soul wired for deep emotional truth, artistic sensitivity, and profound
                empathy. You cannot thrive in superficial environments or half-hearted commitments;
                your spirit craves meaning, beauty, and genuine connection in every endeavor you
                touch. This archetype teaches that vulnerability is not a weakness, but the secret
                doorway to spiritual and creative power. When you pour pure intention into your
                craft, your vision, and your personal growth, the universe responds with abundance.
                Guard your energy from cynicism, honor your emotional depth as a sacred gift, and
                allow your passion to remain the guiding compass that shapes your destiny.
                """
            ),
            KarmicCard(
                name="The Universal Form (Vishvarupa)",
                theme="Cosmic Perspective, Infinity & Awe",
                wiki_titles=["Vishvarupa", "Bhagavata_Purana"],
                commons_query="Vishvarupa Krishna cosmic form painting",
                description="""
                The Universal Form reflects the awe-inspiring revelation of Vishvarupa, where
                Krishna unveils the entire cosmos—past, present, and future, creation and
                dissolution, stars and atoms—contained within a single infinite body. When this
                monumental card appears in your Karmic Signature, it calls you to step out of
                narrow, limiting self-doubt and view your life through a vast cosmic lens. Often,
                we trap ourselves in small anxieties, temporary setbacks, or the fear that our
                work does not matter. Vishvarupa shatters that illusion, reminding you that the
                same intelligence that moves galaxies is flowing through your own mind and
                ambitions. You are meant to think boldly, embrace big transitions, and recognize
                the interconnectedness of every experience you have lived through. Even the
                endings and disruptions in your life are never failures; they are necessary
                transformations clearing space for a grander chapter. Stand in awe of your own
                potential, expand your vision beyond immediate obstacles, and trust the vast
                architecture of your unfolding destiny.
                """
            ),
            KarmicCard(
                name="The Mountain Lifter (Govardhana Giridhari)",
                theme="Protection, Faith & Overcoming Burdens",
                wiki_titles=["Govardhan_Puja", "Govardhan_Hill"],
                commons_query="Krishna lifting Govardhan hill painting",
                description="""
                The Mountain Lifter portrays Krishna effortlessly raising Govardhan Hill on his
                little finger for seven days to shelter the people of Braj from the torrential
                storms of Indra's wrath. In your Karmic Signature, this archetype is the ultimate
                symbol of unshakeable resilience, divine shelter, and quiet inner power during
                turbulent times. When storms of uncertainty, external pressure, or doubt gather
                around you, this card reveals that your foundation is far stronger than the chaos
                outside. Notice that Krishna lifts the massive mountain not with strained muscles,
                but on a single pinky finger—teaching that when your mind is anchored in spiritual
                confidence and clear purpose, even the heaviest responsibilities become light to
                carry. You have a natural capacity to endure pressure, build self-reliance, and
                become a pillar of strength for yourself and those around you. Do not fear intense
                challenges or changing environments; they are only revealing how unbreakable your
                inner resolve truly is.
                """
            ),
            KarmicCard(
                name="The Peacemaker (Shanti Duta)",
                theme="Diplomacy, Balance & Calm Strategy",
                wiki_titles=["Vasudeva_Krishna", "Udyoga_Parva"],
                commons_query="Krishna ambassador court painting",
                description="""
                The Peacemaker represents Krishna in his royal diplomatic mission to the court of
                Hastinapura, where he spoke with unshakeable poise, razor-sharp wisdom, and
                fearless composure before kings and rivals alike. In your Karmic Signature, this
                archetype highlights strategic intelligence, emotional maturity, and the power of
                clear communication. It signifies a soul that knows how to walk into high-stakes
                situations, read the room with precision, and seek fair, constructive solutions
                without ever compromising personal dignity. The Peacemaker is never weak or
                passive; Krishna offered peace first, yet stood completely prepared for action
                when justice demanded it. Drawing this card shows that your path involves bridging
                contrasting worlds—blending logic with intuition, ambition with ethics, and
                firmness with grace. When facing conflict or uncertainty, your greatest asset is
                your calm, discerning mind. Speak your truth clearly, negotiate your worth with
                confidence, and never allow anyone else's chaos to pull you out of your center.
                """
            ),
            KarmicCard(
                name="The Serpent Conqueror (Kaliya Mardana)",
                theme="Fearlessness, Transmutation & Rising Above",
                wiki_titles=["Kaliya", "Yamuna_in_Hinduism"],
                commons_query="Krishna Kaliya serpent painting",
                description="""
                The Serpent Conqueror depicts young Krishna diving fearlessly into the poisoned
                waters of the Yamuna River and dancing victoriously upon the many hoods of the
                venomous serpent Kaliya. In esoteric philosophy, the multi-headed serpent
                represents toxic fears, self-sabotaging thoughts, and old emotional wounds that
                poison our inner peace. Notice that Krishna does not destroy Kaliya; instead, he
                dances upon the serpent's heads until the venom is subdued and the waters are pure
                again. In your Karmic Signature, this is a card of profound alchemy and
                psychological mastery. It reveals that you have withstood difficult emotional
                tests or self-doubt and possess the power to turn your deepest fears into your
                greatest stepping stones. Every hood of anxiety or setback you conquer only
                elevates your stature. Rather than running from intimidating challenges, face them
                with rhythm, poise, and courage—knowing you are meant to rise above the poison and
                reclaim your power.
                """
            ),
            KarmicCard(
                name="The Cosmic Dancer (Raseshwara)",
                theme="Rhythm of Life, Celebration & Creative Flow",
                wiki_titles=["Rasa_lila", "Vrindavan"],
                commons_query="Rasa lila Krishna painting",
                description="""
                The Cosmic Dancer illuminates the sacred night of the Rasa Lila, where Krishna
                dances in a great circle beneath the autumn full moon, multiplying his presence so
                that every soul experiences the divine standing right beside them. In your Karmic
                Signature, this archetype symbolizes dynamic balance, creative abundance, and the
                ability to stay centered while life spins in motion around you. Just as the hub of
                a wheel remains still while the outer rim turns rapidly, The Cosmic Dancer teaches
                you how to engage fully with your studies, projects, and ambitions without losing
                your inner equilibrium. You are meant to bring artistry, originality, and spirited
                energy into the world. When life feels overly mechanical or stressful, this card
                invites you to shift your perspective from struggle to choreography—learning when
                to step forward, when to pivot, and when to celebrate how far you have already
                come. Trust the sacred timing of your journey.
                """
            )
        ]

# ==========================================
# 3. BULLETPROOF DYNAMIC AI CALLER
# ==========================================
def get_ai_reading(prompt):
    try:
        available_models = client.models.list()
        valid_models = []
        for m in available_models:
            name = m.name.replace("models/", "")
            if "gemini" in name.lower() and "vision" not in name.lower() and "embedding" not in name.lower():
                valid_models.append(name)

        valid_models.sort(reverse=True)

        if not valid_models:
            return "Error: Your API key does not have access to any Gemini text models."

        last_error = None
        for model_name in valid_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                last_error = e
                continue

        return f"The Oracle's servers are currently busy. Please try again. Last error: {last_error}"
    except Exception as e:
        return f"System failed to fetch model list from Google: {e}"

# ==========================================
# 4. STREAMLIT VISUAL INTERFACE
# ==========================================
st.title("🦚 The Karmic Path")
st.write("Discover the cosmic themes written into your life. Enter your birth details to reveal your permanent Karmic Signature.")
st.divider()

# --- SIDEBAR: BIRTH DETAILS ---
st.sidebar.header("Your Birth Details")
dob_date = st.sidebar.date_input(
    "Date of Birth:",
    value=datetime.date(2000, 1, 1),
    min_value=datetime.date(1900, 1, 1)
)
dob_time = st.sidebar.time_input(
    "Time of Birth (Optional):",
    value=datetime.time(12, 0)
)
birth_place = st.sidebar.text_input(
    "Place of Birth:",
    placeholder="e.g., Kolhapur, India"
)

user_seed_string = f"{dob_date}-{dob_time}-{birth_place.strip().lower()}"
seed_hash = int(hashlib.sha256(user_seed_string.encode("utf-8")).hexdigest(), 16)

st.sidebar.divider()
calculate_btn = st.sidebar.button("✨ Reveal My Karmic Path", use_container_width=True)

# --- MAIN INTERACTIVE AREA ---
if calculate_btn:
    if not birth_place.strip():
        st.warning("Please enter your Place of Birth to calculate your Karmic Path.")
    else:
        random.seed(seed_hash)

        deck = KrishnaDeck()
        drawn_cards = random.sample(deck.cards, 3)

        positions = [
            "Past Karma (Roots)",
            "Present Dharma (Action)",
            "Future Moksha (Evolution)"
        ]

        st.subheader("Your Karmic Signature")
        cols = st.columns(3)
        card_data_for_ai = []

        for i, card in enumerate(drawn_cards):
            with cols[i]:
                st.markdown(f"**{positions[i]}**")
                with st.spinner(f"Summoning {card.name}..."):
                    card_img = build_card_image(card.name, card.wiki_titles, card.commons_query)
                    st.image(card_img, use_container_width=True)
                st.markdown(f"### {card.name}")
                st.caption(f"Theme: {card.theme}")
                st.markdown(
                    f'<div class="card-desc-box">{card.description}</div>',
                    unsafe_allow_html=True
                )

                card_data_for_ai.append(
                    f"{positions[i]}: '{card.name}' (Theme: {card.theme})"
                )

        st.divider()

        st.subheader("✨ Your Personalized Karmic Synthesis")
        with st.spinner("Decoding your karmic blueprint across time..."):
            prompt = f"""
            The user was born on {dob_date} at {dob_time} in {birth_place}.
            Based on these birth coordinates, they have drawn the following three Krishna Archetype cards:
            1. {card_data_for_ai[0]}
            2. {card_data_for_ai[1]}
            3. {card_data_for_ai[2]}

            Provide a deeply insightful spiritual reading structured into three clear sections—one for each card.
            CRITICAL INSTRUCTIONS:
            - Dedicate roughly 200 words to EACH of the three cards (around 600 words total).
            - Section 1 (Past Karma): Explain how their roots in {birth_place} and the first archetype shaped their inner foundation.
            - Section 2 (Present Dharma): Explain what practical actions and strengths the second archetype calls them to embody now.
            - Section 3 (Future Moksha): Explain how the third archetype guides their long-term spiritual and personal evolution.
            - Write in a warm, empowering, and accessible tone.
            """

            reading = get_ai_reading(prompt)
            st.write(reading)

        random.seed()
else:
    st.info("Enter your birth details in the sidebar and click 'Reveal My Karmic Path' to draw your cards.")