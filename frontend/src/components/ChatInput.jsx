/**
 * ChatInput component - Campo di input per messaggi
 * Include bottone invio e bottone WhatsApp.
 */
import { useState } from 'react';
import './ChatInput.css';

export default function ChatInput({ onSend, onWhatsApp, disabled, lastBotMessage }) {
  const [message, setMessage] = useState('');

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = message.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setMessage('');
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  function handleWhatsApp() {
    const text = lastBotMessage || message.trim();
    if (text) {
      onWhatsApp(text);
    }
  }

  return (
    <div className="chat-input-container" id="chat-input-container">
      <form onSubmit={handleSubmit} className="chat-input-form">
        <div className="input-wrapper">
          <input
            id="chat-message-input"
            type="text"
            className="chat-input"
            placeholder="Scrivi un messaggio..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            autoComplete="off"
            autoFocus
          />
          <button
            type="submit"
            id="send-message-btn"
            className="send-btn"
            disabled={!message.trim() || disabled}
            aria-label="Invia messaggio"
          >
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="send-icon">
              <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      </form>
      
      <button
        id="whatsapp-btn"
        className="whatsapp-btn"
        onClick={handleWhatsApp}
        disabled={!lastBotMessage && !message.trim()}
        aria-label="Invia su WhatsApp"
        title="Invia su WhatsApp"
      >
        <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg" className="whatsapp-icon">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
        </svg>
        <span className="whatsapp-label">Invia su WhatsApp</span>
      </button>
    </div>
  );
}
