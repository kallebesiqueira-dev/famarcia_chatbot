/**
 * Header component - Barra superiore con selettore lingua (SVG flags)
 */
import { useState, useRef, useEffect } from 'react';
import './Header.css';

/* ── Inline SVG flags (no emoji, works on all OS) ── */
function FlagIT({ size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 640 480" className="flag-svg">
      <rect width="640" height="480" fill="#fff"/>
      <rect width="213.3" height="480" fill="#009246"/>
      <rect x="426.7" width="213.3" height="480" fill="#ce2b37"/>
    </svg>
  );
}

function FlagGB({ size = 20 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 640 480" className="flag-svg">
      <path fill="#012169" d="M0 0h640v480H0z"/>
      <path fill="#FFF" d="m75 0 244 181L562 0h78v62L400 241l240 178v61h-80L320 301 81 480H0v-60l239-178L0 64V0h75z"/>
      <path fill="#C8102E" d="m424 281 216 159v40L369 281h55zm-184 20 6 35L54 480H0l240-179zM640 0v3L391 191l2-44L590 0h50zM0 0l239 176h-60L0 42V0z"/>
      <path fill="#FFF" d="M241 0v480h160V0H241zM0 160v160h640V160H0z"/>
      <path fill="#C8102E" d="M0 193v96h640v-96H0zM273 0v480h96V0h-96z"/>
    </svg>
  );
}

const LANGUAGES = [
  { code: 'it', label: 'Italiano', short: 'IT', Flag: FlagIT },
  { code: 'en', label: 'English', short: 'EN', Flag: FlagGB },
];

export default function Header({ language = 'it', onLanguageChange }) {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  const current = LANGUAGES.find(l => l.code === language) || LANGUAGES[0];

  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  function selectLanguage(code) {
    onLanguageChange(code);
    setDropdownOpen(false);
  }

  return (
    <header className="app-header" id="app-header">
      <div className="header-content">
        <div className="header-brand">
          <div className="header-logo">
            <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" className="logo-icon">
              <rect x="2" y="2" width="36" height="36" rx="10" fill="url(#logoGradient)" />
              <path d="M20 10V30M10 20H30" stroke="white" strokeWidth="3.5" strokeLinecap="round" />
              <defs>
                <linearGradient id="logoGradient" x1="2" y1="2" x2="38" y2="38" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#14b8a6" />
                  <stop offset="1" stopColor="#0f766e" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div className="header-text">
            <h1 className="header-title">Farmacia AI Assistant</h1>
            <p className="header-subtitle">
              {language === 'en' ? 'Your virtual pharmacy assistant' : 'Il tuo assistente farmaceutico virtuale'}
            </p>
          </div>
        </div>

        <div className="header-actions">
          <div className="header-status">
            <span className="status-dot"></span>
            <span className="status-text">Online</span>
          </div>

          {/* Language selector */}
          <div className="lang-selector" id="lang-selector" ref={dropdownRef}>
            <button
              className="lang-selector-btn"
              onClick={() => setDropdownOpen(!dropdownOpen)}
              aria-label="Seleziona lingua"
              aria-expanded={dropdownOpen}
            >
              <current.Flag size={18} />
              <span className="lang-code">{current.short}</span>
              <svg className={`lang-chevron ${dropdownOpen ? 'lang-chevron-open' : ''}`} viewBox="0 0 16 16" fill="none">
                <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>

            {dropdownOpen && (
              <div className="lang-dropdown">
                {LANGUAGES.map(lang => (
                  <button
                    key={lang.code}
                    className={`lang-option ${lang.code === language ? 'lang-option-active' : ''}`}
                    onClick={() => selectLanguage(lang.code)}
                  >
                    <lang.Flag size={20} />
                    <span className="lang-option-label">{lang.label}</span>
                    {lang.code === language && (
                      <svg className="lang-check" viewBox="0 0 16 16" fill="none">
                        <path d="M3 8L7 12L13 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    )}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
