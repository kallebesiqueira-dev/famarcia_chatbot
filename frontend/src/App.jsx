/**
 * App component - Root dell'applicazione Farmacia AI Assistant
 * 
 * Gestisce lo stato globale della chat:
 * - Lista messaggi
 * - Stato di typing del bot
 * - Comunicazione con backend API
 * - Integrazione WhatsApp
 */
import { useState, useCallback } from 'react';
import Header from './components/Header';
import ChatBox from './components/ChatBox';
import QuickActions from './components/QuickActions';
import ChatInput from './components/ChatInput';
import { sendChatMessage, generateWhatsAppLinkLocal } from './services/api';
import './App.css';

// Genera un session ID unico per questa sessione browser
const SESSION_ID = `session_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`;

// Delay simulazione typing (ms)
const TYPING_DELAY_MIN = 800;
const TYPING_DELAY_MAX = 2000;

export default function App() {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [lastBotMessage, setLastBotMessage] = useState('');
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState('it');

  /**
   * Calcola delay typing in base alla lunghezza della risposta.
   */
  function getTypingDelay(responseLength) {
    const base = Math.min(
      TYPING_DELAY_MAX,
      TYPING_DELAY_MIN + (responseLength * 2)
    );
    return base + Math.random() * 500;
  }

  /**
   * Invia un messaggio e gestisce la risposta del bot.
   */
  const handleSendMessage = useCallback(async (text) => {
    if (!text.trim() || isLoading) return;

    setError(null);

    // Aggiungi messaggio utente
    const userMessage = {
      text,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMessage]);

    // Mostra typing
    setIsTyping(true);
    setIsLoading(true);

    try {
      // Chiama API backend
      const data = await sendChatMessage(text, SESSION_ID);
      const responseText = data?.response || data?.message || 'Risposta non disponibile.';

      // Simula delay typing realistico
      const delay = getTypingDelay(responseText.length);
      await new Promise(resolve => setTimeout(resolve, delay));

      // Aggiungi risposta bot
      const botMessage = {
        text: responseText,
        sender: 'bot',
        timestamp: data?.timestamp || new Date().toISOString(),
      };

      setMessages(prev => [...prev, botMessage]);
      setLastBotMessage(responseText);

    } catch (err) {
      console.error('Errore chat:', err);

      // Fallback: risposta locale se il backend non è disponibile
      const fallbackResponse = getFallbackResponse(text);
      
      const delay = getTypingDelay(fallbackResponse.length);
      await new Promise(resolve => setTimeout(resolve, delay));

      const botMessage = {
        text: fallbackResponse,
        sender: 'bot',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, botMessage]);
      setLastBotMessage(fallbackResponse);

      // Mostra errore solo se non è un fallback
      if (!fallbackResponse.includes('Benvenuto') && !fallbackResponse.includes('Welcome')) {
        setError(language === 'en' 
          ? 'Backend unreachable. Responses in offline mode.'
          : 'Backend non raggiungibile. Risposte in modalità offline.');
      }
    } finally {
      setIsTyping(false);
      setIsLoading(false);
    }
  }, [isLoading]);

  /**
   * Risposta di fallback lato client quando il backend non è disponibile.
   */
  function getFallbackResponse(message) {
    const msg = message.toLowerCase();
    // Auto-detect: se contiene keyword EN, rispondi in EN
    const enWords = ['hello','hi','hey','headache','fever','cough','cold','hours','thanks','help','open','services'];
    const isEn = enWords.some(kw => msg.includes(kw));

    if (['ciao','buongiorno','buonasera','salve','hello','hi','hey'].some(kw => msg.includes(kw))) {
      return isEn
        ? "👋 **Hello!** Welcome to Pharmacy AI.\n\nI'm running in offline mode, but I can still help with basic info.\n\nTry asking about:\n• Pharmacy hours\n• Common medications\n• Our services"
        : "👋 **Buongiorno!** Benvenuto nella Farmacia AI.\n\nSto funzionando in modalità offline, ma posso aiutarla con informazioni di base.\n\nProvi a chiedere:\n• Orari della farmacia\n• Farmaci comuni\n• I nostri servizi";
    }

    if (['orari','orario','aperta','hours','schedule','open'].some(kw => msg.includes(kw))) {
      return isEn
        ? "🕐 **Pharmacy Hours:**\n\n📅 **Mon-Fri:** 8:30 AM - 7:30 PM\n📅 **Saturday:** 8:30 AM - 1:00 PM\n📅 **Sunday:** Closed\n\n📍 Via Roma 42, City Center"
        : "🕐 **Orari della Farmacia:**\n\n📅 **Lun-Ven:** 8:30 - 19:30\n📅 **Sabato:** 8:30 - 13:00\n📅 **Domenica:** Chiuso\n\n📍 Via Roma 42, Centro città";
    }

    if (['mal di testa','cefalea','headache','migraine'].some(kw => msg.includes(kw))) {
      return isEn
        ? "💊 For **headaches**, common OTC meds:\n\n• **Paracetamol** - 500/1000mg\n• **Ibuprofen** - 200/400mg\n\n⚠️ *Do not exceed recommended doses. Consult a doctor if persistent.*"
        : "💊 Per il **mal di testa**:\n\n• **Paracetamolo** (Tachipirina) - 500/1000mg\n• **Ibuprofene** (Moment) - 200/400mg\n\n⚠️ *Non superi le dosi consigliate. Consulti un medico per casi persistenti.*";
    }

    if (['tosse','catarro','cough','phlegm'].some(kw => msg.includes(kw))) {
      return isEn
        ? "🫁 For **cough**:\n\n• **Dry cough:** suppressant syrup\n• **Wet cough:** mucolytic syrup\n• Warm honey drinks\n\n⚠️ *See a doctor if cough persists over 2 weeks.*"
        : "🫁 Per la **tosse**:\n\n• **Tosse secca:** sciroppo sedativo\n• **Tosse grassa:** sciroppo mucolitico\n• Tisane calde con miele\n\n⚠️ *Consulti un medico se persiste oltre 2 settimane.*";
    }

    if (['febbre','temperatura','fever','temperature'].some(kw => msg.includes(kw))) {
      return isEn
        ? "🌡️ For **fever**:\n\n• **Paracetamol** - most suitable\n• Drink plenty of fluids\n• Rest well\n\n⚠️ *See a doctor if fever exceeds 39°C or lasts more than 3 days.*"
        : "🌡️ Per la **febbre**:\n\n• **Paracetamolo** (Tachipirina)\n• Beva molti liquidi\n• Riposo adeguato\n\n⚠️ *Se supera 39°C o persiste per 3+ giorni, consulti il medico.*";
    }

    if (['grazie','thanks','thank you'].some(kw => msg.includes(kw))) {
      return isEn
        ? "😊 **Thank you!** Happy to help.\n\nDon't hesitate to ask more. Have a great day! 🌟"
        : "😊 **Grazie a Lei!** È stato un piacere.\n\nNon esiti a chiedere. Buona giornata! 🌟";
    }

    return isEn
      ? "🤔 Sorry, I'm running in offline mode.\n\nI can help with:\n• **Common symptoms** (headache, fever, cough)\n• **Pharmacy hours**\n\nPlease verify the backend server is running."
      : "🤔 Sto funzionando in modalità offline.\n\nPosso aiutarla con:\n• **Sintomi comuni** (mal di testa, febbre, tosse)\n• **Orari farmacia**\n\nVerifichi che il server backend sia attivo.";
  }

  /**
   * Gestisce l'invio su WhatsApp.
   */
  function handleWhatsApp(messageText) {
    const cleanText = messageText
      .replace(/\*\*/g, '')
      .replace(/\*/g, '')
      .replace(/•/g, '-')
      .substring(0, 500);

    const url = generateWhatsAppLinkLocal(
      `Farmacia AI Assistant:\n\n${cleanText}`
    );
    window.open(url, '_blank', 'noopener,noreferrer');
  }

  /**
   * Gestisce i pulsanti rapidi.
   */
  function handleQuickAction(message) {
    handleSendMessage(message);
  }

  return (
    <div className="app-container" id="app-container">
      <Header language={language} onLanguageChange={setLanguage} />
      
      {/* Banner errore */}
      {error && (
        <div className="error-banner animate-fade-in-up" id="error-banner">
          <span className="error-icon">⚡</span>
          <span className="error-text">{error}</span>
          <button 
            className="error-dismiss" 
            onClick={() => setError(null)}
            aria-label="Chiudi errore"
          >
            ✕
          </button>
        </div>
      )}

      <ChatBox messages={messages} isTyping={isTyping} language={language} />
      <QuickActions onAction={handleQuickAction} disabled={isLoading} language={language} />
      <ChatInput 
        onSend={handleSendMessage} 
        onWhatsApp={handleWhatsApp}
        disabled={isLoading}
        lastBotMessage={lastBotMessage}
      />
    </div>
  );
}
