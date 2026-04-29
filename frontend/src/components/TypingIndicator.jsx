/**
 * TypingIndicator component - Indicatore di digitazione del bot
 * Tre puntini animati stile WhatsApp.
 */
import './TypingIndicator.css';

export default function TypingIndicator() {
  return (
    <div className="typing-indicator-wrapper animate-fade-in-up" id="typing-indicator">
      <div className="typing-avatar">
        <svg viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="28" height="28" rx="8" fill="url(#typingGrad)" />
          <path d="M14 7V21M7 14H21" stroke="white" strokeWidth="2.5" strokeLinecap="round" />
          <defs>
            <linearGradient id="typingGrad" x1="0" y1="0" x2="28" y2="28">
              <stop stopColor="#14b8a6" />
              <stop offset="1" stopColor="#0f766e" />
            </linearGradient>
          </defs>
        </svg>
      </div>
      <div className="typing-bubble">
        <div className="typing-dots">
          <span className="typing-dot" style={{ animationDelay: '0s' }}></span>
          <span className="typing-dot" style={{ animationDelay: '0.2s' }}></span>
          <span className="typing-dot" style={{ animationDelay: '0.4s' }}></span>
        </div>
      </div>
    </div>
  );
}
