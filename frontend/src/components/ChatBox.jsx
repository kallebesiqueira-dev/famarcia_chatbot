/**
 * ChatBox component - Container principale della chat
 * Gestisce l'area dei messaggi con auto-scroll.
 */
import { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import './ChatBox.css';

const WELCOME = {
  it: {
    title: 'Benvenuto in Farmacia AI',
    text: 'Sono il tuo assistente farmaceutico virtuale.',
    sub: 'Chiedimi informazioni su farmaci, orari o servizi della farmacia.',
    f1: 'Consigli farmaci', f2: 'Orari e info', f3: 'Disponibilità',
  },
  en: {
    title: 'Welcome to Pharmacy AI',
    text: "I'm your virtual pharmacy assistant.",
    sub: 'Ask me about medications, hours, or pharmacy services.',
    f1: 'Medication advice', f2: 'Hours & info', f3: 'Availability',
  },
};

export default function ChatBox({ messages, isTyping, language = 'it' }) {
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);
  const w = WELCOME[language] || WELCOME.it;

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isTyping]);

  return (
    <div className="chatbox" id="chatbox" ref={chatContainerRef}>
      {messages.length === 0 && (
        <div className="chatbox-welcome animate-fade-in-up">
          <div className="welcome-icon">
            <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="40" cy="40" r="38" fill="url(#welcomeGrad)" opacity="0.1"/>
              <circle cx="40" cy="40" r="28" fill="url(#welcomeGrad)" opacity="0.15"/>
              <rect x="26" y="26" width="28" height="28" rx="8" fill="url(#welcomeGrad)" />
              <path d="M40 33V47M33 40H47" stroke="white" strokeWidth="3" strokeLinecap="round" />
              <defs>
                <linearGradient id="welcomeGrad" x1="12" y1="12" x2="68" y2="68">
                  <stop stopColor="#14b8a6" />
                  <stop offset="1" stopColor="#0f766e" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h2 className="welcome-title">{w.title}</h2>
          <p className="welcome-text">
            {w.text}<br/>{w.sub}
          </p>
          <div className="welcome-features">
            <div className="welcome-feature">
              <span className="feature-icon">💊</span>
              <span className="feature-text">{w.f1}</span>
            </div>
            <div className="welcome-feature">
              <span className="feature-icon">🕐</span>
              <span className="feature-text">{w.f2}</span>
            </div>
            <div className="welcome-feature">
              <span className="feature-icon">📦</span>
              <span className="feature-text">{w.f3}</span>
            </div>
          </div>
        </div>
      )}

      <div className="chatbox-messages">
        {messages.map((msg, index) => (
          <MessageBubble key={index} message={msg} />
        ))}
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}

