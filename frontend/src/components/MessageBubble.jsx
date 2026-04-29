/**
 * MessageBubble component - Bolla di messaggio stile WhatsApp
 * Differenzia visivamente messaggi utente e bot.
 */
import './MessageBubble.css';

export default function MessageBubble({ message }) {
  const { text, sender, timestamp } = message;
  const isBot = sender === 'bot';

  /**
   * Formatta il testo del bot con supporto per markdown basilare.
   * Converte **bold**, emoji e newline.
   */
  function formatBotText(text) {
    if (!text) return '';

    // Converti **testo** in <strong>
    let formatted = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    
    // Converti *testo* in <em>
    formatted = formatted.replace(/(?<!\*)\*([^*]+?)\*(?!\*)/g, '<em>$1</em>');

    // Converti newline in <br>
    formatted = formatted.replace(/\n/g, '<br/>');

    return formatted;
  }

  function formatTime(ts) {
    if (!ts) return '';
    const date = new Date(ts);
    return date.toLocaleTimeString('it-IT', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  }

  return (
    <div 
      className={`message-bubble ${isBot ? 'message-bot animate-slide-in-left' : 'message-user animate-slide-in-right'}`}
      id={`message-${timestamp}`}
    >
      {isBot && (
        <div className="message-avatar">
          <svg viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="28" height="28" rx="8" fill="url(#avatarGrad)" />
            <path d="M14 7V21M7 14H21" stroke="white" strokeWidth="2.5" strokeLinecap="round" />
            <defs>
              <linearGradient id="avatarGrad" x1="0" y1="0" x2="28" y2="28">
                <stop stopColor="#14b8a6" />
                <stop offset="1" stopColor="#0f766e" />
              </linearGradient>
            </defs>
          </svg>
        </div>
      )}
      <div className={`bubble-content ${isBot ? 'bubble-bot' : 'bubble-user'}`}>
        {isBot && <span className="bubble-sender">Farmacia AI</span>}
        <div 
          className="bubble-text"
          dangerouslySetInnerHTML={isBot ? { __html: formatBotText(text) } : undefined}
        >
          {!isBot ? text : undefined}
        </div>
        <span className="bubble-time">{formatTime(timestamp)}</span>
      </div>
    </div>
  );
}
