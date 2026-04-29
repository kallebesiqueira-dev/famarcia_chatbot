"""
Motore AI bilingue (IT/EN) per la generazione di risposte farmaceutiche.
Architettura plug & play: supporta mock (rule-based) e provider reali.

IMPORTANTE: Le risposte sono puramente informative e NON sostituiscono
il parere di un medico o farmacista qualificato.
"""
import logging
import time
from django.conf import settings

logger = logging.getLogger('chatbot')

# ---------------------------------------------------------------------------
# Language Detection — dual-score comparison
# ---------------------------------------------------------------------------
EN_INDICATORS = [
    # greetings & common
    'hello', 'hi', 'hey', 'good morning', 'good evening', 'good afternoon',
    'thanks', 'thank you', 'thx', 'bye', 'goodbye',
    # medical
    'headache', 'fever', 'cough', 'cold', 'allergy', 'allergies', 'stomach',
    'pain', 'sleep', 'insomnia', 'muscle', 'back pain', 'sore', 'nausea',
    'pharmacy', 'medication', 'medicine', 'drug', 'prescription', 'pill',
    # info
    'hours', 'schedule', 'open', 'closed', 'contact', 'services', 'address',
    'phone', 'email', 'location', 'availability', 'available', 'product',
    # common English words (articles, pronouns, verbs, prepositions)
    'the', 'is', 'are', 'was', 'were', 'am',
    'i ', ' i ', "i'm", "i'd", "i've", "i'll",
    'you', 'your', 'my', 'we', 'they', 'our',
    'would', 'could', 'should', 'will', 'shall',
    'like', 'want', 'need', 'help', 'know', 'check', 'find', 'get',
    'do you', 'can you', 'could you', 'would you',
    'what', 'when', 'where', 'how', 'which', 'who', 'why',
    'please', 'about', 'with', 'for', 'from', 'have', 'has',
    'some', 'any', 'this', 'that', 'these', 'those',
]

IT_INDICATORS = [
    # saluti
    'ciao', 'buongiorno', 'buonasera', 'salve', 'grazie', 'arrivederci',
    # medico
    'mal di', 'febbre', 'tosse', 'raffreddore', 'allergia', 'stomaco',
    'dolore', 'dormire', 'insonnia', 'muscoli', 'schiena',
    'farmaco', 'farmaci', 'medicina', 'ricetta', 'pillola',
    # info
    'orari', 'orario', 'aperta', 'chiusa', 'contatti', 'servizi',
    'indirizzo', 'telefono', 'disponibilità', 'disponibile', 'prodotto',
    # common Italian words
    'il ', 'lo ', 'la ', 'le ', 'gli ', 'un ', 'una ',
    'sono', 'sei', 'siamo', 'avete', 'hanno',
    'vorrei', 'posso', 'puoi', 'potrei', 'potete',
    'mi ', 'ti ', 'ci ', 'vi ', 'si ',
    'che ', 'cosa', 'come', 'dove', 'quando', 'quale', 'perché',
    'per ', 'con ', 'del ', 'della', 'delle', 'degli',
    'questo', 'questa', 'quello', 'quella',
    'non ', 'anche', 'molto', 'più',
    'ho ', 'hai ', 'ha ', 'abbiamo',
]


def detect_language(message: str) -> str:
    """Rileva la lingua del messaggio confrontando indicatori EN vs IT."""
    msg = message.lower()
    en_score = sum(1 for kw in EN_INDICATORS if kw in msg)
    it_score = sum(1 for kw in IT_INDICATORS if kw in msg)
    logger.debug(f"Language detection — EN: {en_score}, IT: {it_score}")
    # English wins if it has more indicators, or if tied (since Italian is default)
    if en_score > it_score:
        return 'en'
    return 'it'


# ---------------------------------------------------------------------------
# Disclaimer bilingue
# ---------------------------------------------------------------------------
DISCLAIMER = {
    'it': (
        "\n\n⚠️ *Disclaimer: Queste informazioni sono puramente indicative e "
        "non sostituiscono il parere di un medico o farmacista. Consulta sempre "
        "un professionista sanitario prima di assumere qualsiasi farmaco.*"
    ),
    'en': (
        "\n\n⚠️ *Disclaimer: This information is for general guidance only and "
        "does not replace the advice of a doctor or pharmacist. Always consult "
        "a healthcare professional before taking any medication.*"
    ),
}

# ---------------------------------------------------------------------------
# Knowledge Base bilingue
# ---------------------------------------------------------------------------
PHARMACY_KNOWLEDGE = {
    'headache': {
        'keywords_it': ['mal di testa', 'cefalea', 'emicrania', 'testa che fa male', 'dolore alla testa'],
        'keywords_en': ['headache', 'head pain', 'migraine', 'head ache', 'head hurts'],
        'response_it': (
            "💊 Per il **mal di testa**, i farmaci da banco più comuni sono:\n\n"
            "• **Paracetamolo** (Tachipirina) - 500/1000mg\n"
            "• **Ibuprofene** (Moment, Brufen) - 200/400mg\n"
            "• **Aspirina** (Acido acetilsalicilico) - 500mg\n\n"
            "📋 **Consigli:**\n"
            "- Assuma il farmaco a stomaco pieno\n"
            "- Non superi le dosi consigliate\n"
            "- Se il dolore persiste per più di 3 giorni, consulti il medico\n"
            "- Beva molta acqua e riposi in un ambiente tranquillo"
        ),
        'response_en': (
            "💊 For **headaches**, the most common OTC medications are:\n\n"
            "• **Paracetamol** (Acetaminophen) - 500/1000mg\n"
            "• **Ibuprofen** (Advil, Motrin) - 200/400mg\n"
            "• **Aspirin** (Acetylsalicylic acid) - 500mg\n\n"
            "📋 **Advice:**\n"
            "- Take medication with food\n"
            "- Do not exceed recommended doses\n"
            "- If pain persists for more than 3 days, consult a doctor\n"
            "- Drink plenty of water and rest in a quiet environment"
        ),
    },
    'fever': {
        'keywords_it': ['febbre', 'temperatura alta', 'ho la febbre', 'febbricola'],
        'keywords_en': ['fever', 'high temperature', 'i have a fever', 'feverish', 'temperature'],
        'response_it': (
            "🌡️ Per la **febbre**, le consiglio:\n\n"
            "• **Paracetamolo** (Tachipirina) - il più indicato\n"
            "• **Ibuprofene** - antinfiammatorio e antipiretico\n\n"
            "📋 **Consigli importanti:**\n"
            "- Beva molti liquidi per evitare la disidratazione\n"
            "- Riposo adeguato\n"
            "- Se la febbre supera i 39°C o persiste per più di 3 giorni, consulti il medico\n"
            "- Per bambini: dosaggio in base al peso, consulti il pediatra"
        ),
        'response_en': (
            "🌡️ For **fever**, I recommend:\n\n"
            "• **Paracetamol** (Acetaminophen) - most suitable\n"
            "• **Ibuprofen** - anti-inflammatory and antipyretic\n\n"
            "📋 **Important advice:**\n"
            "- Drink plenty of fluids to avoid dehydration\n"
            "- Get adequate rest\n"
            "- If fever exceeds 39°C (102°F) or persists for more than 3 days, see a doctor\n"
            "- For children: dosage by weight, consult a pediatrician"
        ),
    },
    'cough': {
        'keywords_it': ['tosse', 'tossire', 'tosse secca', 'tosse grassa', 'catarro'],
        'keywords_en': ['cough', 'coughing', 'dry cough', 'wet cough', 'phlegm', 'mucus'],
        'response_it': (
            "🫁 Per la **tosse**, distinguiamo:\n\n"
            "**Tosse secca (irritativa):**\n"
            "• Sciroppo sedativo (es. destrometorfano)\n"
            "• Pastiglie emollienti per la gola\n\n"
            "**Tosse grassa (produttiva):**\n"
            "• Sciroppo mucolitico (es. acetilcisteina, ambroxolo)\n"
            "• Bevande calde con miele\n\n"
            "📋 **Consigli:**\n"
            "- Mantenga l'ambiente umidificato\n"
            "- Beva tisane calde con miele e limone\n"
            "- Se la tosse persiste oltre 2 settimane, consulti il medico"
        ),
        'response_en': (
            "🫁 For **cough**, we distinguish:\n\n"
            "**Dry cough (irritative):**\n"
            "• Cough suppressant syrup (e.g. dextromethorphan)\n"
            "• Throat lozenges\n\n"
            "**Wet/productive cough:**\n"
            "• Mucolytic syrup (e.g. acetylcysteine, ambroxol)\n"
            "• Warm drinks with honey\n\n"
            "📋 **Advice:**\n"
            "- Keep the environment humidified\n"
            "- Drink warm herbal teas with honey and lemon\n"
            "- If the cough persists for more than 2 weeks, consult a doctor"
        ),
    },
    'cold': {
        'keywords_it': ['raffreddore', 'naso chiuso', 'congestione', 'starnuti', 'naso che cola'],
        'keywords_en': ['cold', 'stuffy nose', 'congestion', 'sneezing', 'runny nose', 'common cold'],
        'response_it': (
            "🤧 Per il **raffreddore**, le consiglio:\n\n"
            "• **Spray nasale decongestionante** (max 5-7 giorni)\n"
            "• **Lavaggi nasali** con soluzione fisiologica\n"
            "• **Paracetamolo** per eventuali dolori associati\n"
            "• **Vitamina C** per supportare il sistema immunitario\n\n"
            "📋 **Consigli:**\n"
            "- Riposo adeguato\n- Liquidi caldi in abbondanza\n"
            "- Igiene delle mani frequente\n"
            "- Se i sintomi peggiorano, consulti il medico"
        ),
        'response_en': (
            "🤧 For the **common cold**, I recommend:\n\n"
            "• **Nasal decongestant spray** (max 5-7 days)\n"
            "• **Saline nasal rinses**\n"
            "• **Paracetamol** for associated aches\n"
            "• **Vitamin C** to support the immune system\n\n"
            "📋 **Advice:**\n"
            "- Get adequate rest\n- Drink plenty of warm fluids\n"
            "- Wash hands frequently\n"
            "- If symptoms worsen, consult a doctor"
        ),
    },
    'stomach': {
        'keywords_it': ['mal di stomaco', 'stomaco', 'bruciore', 'acidità', 'gastrite', 'digestione'],
        'keywords_en': ['stomach ache', 'stomach pain', 'heartburn', 'acid reflux', 'gastritis', 'indigestion', 'digestion'],
        'response_it': (
            "🫄 Per i **disturbi gastrici**, le consiglio:\n\n"
            "• **Antiacidi** (es. Maalox, Gaviscon) per sollievo rapido\n"
            "• **Gastroprotettori** da banco per bruciore persistente\n"
            "• **Fermenti lattici** per riequilibrare la flora intestinale\n\n"
            "📋 **Consigli:**\n"
            "- Eviti cibi piccanti, fritti e alcolici\n"
            "- Mangi porzioni piccole e frequenti\n"
            "- Non si sdrai subito dopo mangiato\n"
            "- Se il disturbo persiste, consulti il medico"
        ),
        'response_en': (
            "🫄 For **gastric issues**, I recommend:\n\n"
            "• **Antacids** (e.g. Maalox, Gaviscon) for quick relief\n"
            "• **OTC gastroprotectants** for persistent heartburn\n"
            "• **Probiotics** to restore gut flora balance\n\n"
            "📋 **Advice:**\n"
            "- Avoid spicy, fried foods and alcohol\n"
            "- Eat small, frequent meals\n"
            "- Don't lie down right after eating\n"
            "- If symptoms persist, consult a doctor"
        ),
    },
    'allergy': {
        'keywords_it': ['allergia', 'allergico', 'occhi rossi', 'prurito', 'polline'],
        'keywords_en': ['allergy', 'allergic', 'red eyes', 'itchy', 'pollen', 'hay fever', 'allergies'],
        'response_it': (
            "🌼 Per le **allergie**, le consiglio:\n\n"
            "• **Antistaminici** da banco (cetirizina, loratadina)\n"
            "• **Spray nasale** antistaminico\n"
            "• **Collirio** antistaminico per gli occhi\n\n"
            "📋 **Consigli:**\n"
            "- Eviti l'esposizione all'allergene quando possibile\n"
            "- Lavi frequentemente i vestiti dopo attività all'aperto\n"
            "- Tenga le finestre chiuse nelle ore di picco dei pollini\n"
            "- Per allergie gravi, consulti un allergologo"
        ),
        'response_en': (
            "🌼 For **allergies**, I recommend:\n\n"
            "• **OTC antihistamines** (cetirizine, loratadine)\n"
            "• **Antihistamine nasal spray**\n"
            "• **Antihistamine eye drops**\n\n"
            "📋 **Advice:**\n"
            "- Avoid allergen exposure when possible\n"
            "- Wash clothes frequently after outdoor activities\n"
            "- Keep windows closed during peak pollen hours\n"
            "- For severe allergies, consult an allergist"
        ),
    },
    'muscle_pain': {
        'keywords_it': ['dolore muscolare', 'muscoli', 'contrattura', 'strappo', 'dolori muscolari', 'mal di schiena'],
        'keywords_en': ['muscle pain', 'muscles', 'muscle ache', 'back pain', 'sore muscles', 'muscle strain', 'body ache'],
        'response_it': (
            "💪 Per i **dolori muscolari**, le consiglio:\n\n"
            "• **Gel antinfiammatorio** (diclofenac, ketoprofene)\n"
            "• **Ibuprofene** per via orale se il dolore è intenso\n"
            "• **Cerotti riscaldanti** per contratture\n\n"
            "📋 **Consigli:**\n"
            "- Applichi ghiaccio nelle prime 48 ore (se trauma)\n"
            "- Dopo 48 ore, il calore può aiutare\n"
            "- Stretching leggero quando il dolore diminuisce\n"
            "- Se il dolore è molto intenso, consulti il medico"
        ),
        'response_en': (
            "💪 For **muscle pain**, I recommend:\n\n"
            "• **Anti-inflammatory gel** (diclofenac, ketoprofen)\n"
            "• **Ibuprofen** orally if pain is severe\n"
            "• **Heat patches** for muscle tension\n\n"
            "📋 **Advice:**\n"
            "- Apply ice in the first 48 hours (if trauma)\n"
            "- After 48 hours, heat can help\n"
            "- Light stretching as pain decreases\n"
            "- If pain is very intense, consult a doctor"
        ),
    },
    'insomnia': {
        'keywords_it': ['insonnia', 'dormire', 'non riesco a dormire', 'sonno', 'non dormo'],
        'keywords_en': ['insomnia', 'sleep', "can't sleep", 'sleeping', 'sleepless', 'trouble sleeping'],
        'response_it': (
            "😴 Per l'**insonnia**, le consiglio:\n\n"
            "• **Melatonina** - integratore naturale\n"
            "• **Tisane rilassanti** (camomilla, valeriana, passiflora)\n"
            "• **Integratori** a base di valeriana e magnesio\n\n"
            "📋 **Consigli per l'igiene del sonno:**\n"
            "- Mantenga orari regolari\n- Eviti schermi 1 ora prima di dormire\n"
            "- Camera fresca e buia\n- No caffeina dopo le 14:00\n"
            "- Se il problema persiste, consulti il medico"
        ),
        'response_en': (
            "😴 For **insomnia**, I recommend:\n\n"
            "• **Melatonin** - natural supplement\n"
            "• **Relaxing teas** (chamomile, valerian, passionflower)\n"
            "• **Supplements** with valerian and magnesium\n\n"
            "📋 **Sleep hygiene tips:**\n"
            "- Keep a regular schedule\n- Avoid screens 1 hour before bed\n"
            "- Cool and dark bedroom\n- No caffeine after 2 PM\n"
            "- If the problem persists, consult a doctor"
        ),
    },
}

# ---------------------------------------------------------------------------
# Risposte informazioni farmacia bilingue
# ---------------------------------------------------------------------------
PHARMACY_INFO = {
    'hours': {
        'keywords_it': ['orari', 'orario', 'aperta', 'chiusa', 'apertura', 'chiusura', 'quando apre'],
        'keywords_en': ['hours', 'schedule', 'open', 'closed', 'opening', 'closing', 'when open', 'opening hours'],
        'response_it': (
            "🕐 **Orari della Farmacia:**\n\n"
            "📅 **Lunedì - Venerdì:** 8:30 - 19:30\n"
            "📅 **Sabato:** 8:30 - 13:00\n"
            "📅 **Domenica:** Chiuso\n\n"
            "🚨 **Servizio notturno:** Disponibile a rotazione.\n"
            "📍 Siamo in Via Roma 42, Centro città"
        ),
        'response_en': (
            "🕐 **Pharmacy Hours:**\n\n"
            "📅 **Monday - Friday:** 8:30 AM - 7:30 PM\n"
            "📅 **Saturday:** 8:30 AM - 1:00 PM\n"
            "📅 **Sunday:** Closed\n\n"
            "🚨 **Night service:** Available on rotation.\n"
            "📍 Located at Via Roma 42, City Center"
        ),
    },
    'contacts': {
        'keywords_it': ['contatti', 'telefono', 'email', 'indirizzo', 'dove siete', 'numero'],
        'keywords_en': ['contact', 'phone', 'email', 'address', 'where are you', 'number', 'location'],
        'response_it': (
            "📞 **Contatti della Farmacia:**\n\n"
            "📍 **Indirizzo:** Via Roma 42, 00100 Roma\n"
            "📞 **Telefono:** +39 06 1234567\n"
            "📧 **Email:** info@farmacia-esempio.it\n\n"
            "💬 Può anche contattarci su WhatsApp!"
        ),
        'response_en': (
            "📞 **Pharmacy Contact Info:**\n\n"
            "📍 **Address:** Via Roma 42, 00100 Rome, Italy\n"
            "📞 **Phone:** +39 06 1234567\n"
            "📧 **Email:** info@farmacia-esempio.it\n\n"
            "💬 You can also reach us on WhatsApp!"
        ),
    },
    'services': {
        'keywords_it': ['servizi', 'cosa fate', 'offrite', 'prenotazione', 'tamponi', 'vaccini'],
        'keywords_en': ['services', 'what do you offer', 'booking', 'vaccination', 'tests', 'what services'],
        'response_it': (
            "🏥 **I nostri servizi:**\n\n"
            "• 💊 Dispensazione farmaci con e senza ricetta\n"
            "• 🩺 Misurazione pressione arteriosa\n"
            "• 🩸 Analisi del sangue rapide\n"
            "• 💉 Vaccinazioni (su prenotazione)\n"
            "• 📋 Prenotazione visite CUP\n"
            "• 🧴 Consulenza dermocosmesi\n"
            "• 🌿 Fitoterapia e omeopatia\n\n"
            "Per prenotazioni, ci contatti via telefono o WhatsApp."
        ),
        'response_en': (
            "🏥 **Our services:**\n\n"
            "• 💊 Prescription and OTC medication dispensing\n"
            "• 🩺 Blood pressure measurement\n"
            "• 🩸 Rapid blood tests\n"
            "• 💉 Vaccinations (by appointment)\n"
            "• 📋 Specialist visit booking\n"
            "• 🧴 Skincare consulting\n"
            "• 🌿 Herbal and homeopathic remedies\n\n"
            "For appointments, contact us by phone or WhatsApp."
        ),
    },
}

# ---------------------------------------------------------------------------
# Saluti, ringraziamenti, fallback bilingue
# ---------------------------------------------------------------------------
GREETING_KW_IT = ['ciao', 'buongiorno', 'buonasera', 'salve']
GREETING_KW_EN = ['hello', 'hey', 'hi', 'good morning', 'good evening', 'good afternoon']
THANKS_KW_IT = ['grazie', 'ti ringrazio']
THANKS_KW_EN = ['thanks', 'thank you', 'thx']

GREETING_RESPONSE = {
    'it': (
        "👋 **Buongiorno!** Benvenuto nella Farmacia AI.\n\n"
        "Sono il suo assistente virtuale. Posso aiutarla con:\n\n"
        "• 💊 Consigli su farmaci da banco\n"
        "• 🕐 Orari e informazioni sulla farmacia\n"
        "• 📦 Disponibilità prodotti\n"
        "• 📞 Contatti e servizi\n\n"
        "Come posso aiutarla oggi?"
    ),
    'en': (
        "👋 **Hello!** Welcome to Pharmacy AI.\n\n"
        "I'm your virtual assistant. I can help you with:\n\n"
        "• 💊 OTC medication advice\n"
        "• 🕐 Pharmacy hours and info\n"
        "• 📦 Product availability\n"
        "• 📞 Contact and services\n\n"
        "How can I help you today?"
    ),
}

THANKS_RESPONSE = {
    'it': (
        "😊 **Grazie a Lei!** È stato un piacere aiutarla.\n\n"
        "Se ha altre domande, non esiti a chiedere. "
        "Le ricordo che può contattarci anche su WhatsApp.\n\n"
        "Le auguro una buona giornata! 🌟"
    ),
    'en': (
        "😊 **Thank you!** It was a pleasure helping you.\n\n"
        "If you have more questions, don't hesitate to ask. "
        "Remember you can also reach us on WhatsApp.\n\n"
        "Have a great day! 🌟"
    ),
}

DEFAULT_RESPONSE = {
    'it': (
        "🤔 Mi dispiace, non ho trovato informazioni sulla sua richiesta.\n\n"
        "Posso aiutarla con:\n"
        "• **Sintomi comuni** (mal di testa, febbre, tosse...)\n"
        "• **Informazioni farmacia** (orari, contatti, servizi)\n"
        "• **Disponibilità prodotti**\n\n"
        "Provi a riformulare la domanda o utilizzi i pulsanti rapidi."
    ),
    'en': (
        "🤔 Sorry, I couldn't find specific information for your request.\n\n"
        "I can help you with:\n"
        "• **Common symptoms** (headache, fever, cough...)\n"
        "• **Pharmacy info** (hours, contact, services)\n"
        "• **Product availability**\n\n"
        "Try rephrasing your question or use the quick action buttons."
    ),
}


# ---------------------------------------------------------------------------
# Motore di risposta principale
# ---------------------------------------------------------------------------
class PharmacyAIEngine:
    """
    Motore AI bilingue (IT/EN) per risposte farmaceutiche.

    Supporta:
    - 'mock': risposte rule-based (default)
    - 'openai': integrazione OpenAI (futura)
    """

    def __init__(self):
        self.provider = getattr(settings, 'AI_PROVIDER', 'mock')
        logger.info(f"AI Engine inizializzato con provider: {self.provider}")

    def generate_response(self, message: str) -> dict:
        start_time = time.time()

        if self.provider == 'openai':
            response = self._openai_response(message)
        else:
            response = self._mock_response(message)

        elapsed_ms = int((time.time() - start_time) * 1000)
        return {
            'response': response,
            'provider': self.provider,
            'response_time_ms': elapsed_ms,
        }

    def _mock_response(self, message: str) -> str:
        msg = message.lower().strip()
        lang = detect_language(msg)
        logger.debug(f"Messaggio: '{msg}' | Lingua: {lang}")

        # Saluti — check both languages
        all_greet = GREETING_KW_EN + GREETING_KW_IT
        if any(kw in msg for kw in all_greet):
            return GREETING_RESPONSE[lang]

        # Ringraziamenti — check both languages
        all_thanks = THANKS_KW_EN + THANKS_KW_IT
        if any(kw in msg for kw in all_thanks):
            return THANKS_RESPONSE[lang]

        # Cerca nelle risposte mediche — check BOTH keyword sets
        for cat, data in PHARMACY_KNOWLEDGE.items():
            all_kws = data['keywords_it'] + data['keywords_en']
            if any(kw in msg for kw in all_kws):
                logger.info(f"Match: {cat} ({lang})")
                return data[f'response_{lang}'] + DISCLAIMER[lang]

        # Cerca nelle info farmacia — check BOTH keyword sets
        for cat, data in PHARMACY_INFO.items():
            all_kws = data['keywords_it'] + data['keywords_en']
            if any(kw in msg for kw in all_kws):
                logger.info(f"Match info: {cat} ({lang})")
                return data[f'response_{lang}']

        logger.info("Nessun match, risposta di default")
        return DEFAULT_RESPONSE[lang]

    def _openai_response(self, message: str) -> str:
        """Genera risposta tramite OpenAI API con contesto farmaceutico."""
        try:
            from openai import OpenAI

            api_key = getattr(settings, 'OPENAI_API_KEY', '')
            if not api_key:
                logger.warning("OPENAI_API_KEY non configurata. Fallback a mock.")
                return self._mock_response(message)

            client = OpenAI(api_key=api_key)
            lang = detect_language(message)

            system_prompt = (
                "You are a professional, friendly AI pharmacy assistant for an Italian pharmacy. "
                "You provide helpful information about OTC medications, common symptoms, pharmacy services, and general health advice. "
                "IMPORTANT RULES:\n"
                "1. NEVER diagnose conditions or prescribe prescription medications.\n"
                "2. Always recommend consulting a doctor or pharmacist for serious or persistent symptoms.\n"
                "3. Use emojis to make responses friendly (💊🌡️🫁 etc.).\n"
                "4. Format responses with markdown bold (**text**) and bullet points (•).\n"
                "5. Always end medical advice with a disclaimer.\n"
                "6. Keep responses concise but informative (max 300 words).\n"
                f"7. Respond in {'English' if lang == 'en' else 'Italian'}.\n"
                "8. The pharmacy is located at Via Roma 42, Rome. Hours: Mon-Fri 8:30-19:30, Sat 8:30-13:00, Sun closed.\n"
                "9. Phone: +39 06 1234567, Email: info@farmacia-esempio.it\n"
            )

            response = client.chat.completions.create(
                model=getattr(settings, 'AI_MODEL', 'gpt-4'),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
                max_tokens=int(getattr(settings, 'AI_MAX_TOKENS', 500)),
                temperature=0.7,
            )

            result = response.choices[0].message.content.strip()
            logger.info(f"OpenAI response OK — tokens used: {response.usage.total_tokens}")
            return result

        except ImportError:
            logger.error("Pacchetto 'openai' non installato. pip install openai")
            return self._mock_response(message)
        except Exception as e:
            logger.error(f"Errore OpenAI: {e}")
            return self._mock_response(message)


# Istanza singleton
ai_engine = PharmacyAIEngine()


def generate_pharmacy_response(message: str) -> dict:
    """Funzione di convenienza per generare risposte."""
    return ai_engine.generate_response(message)
