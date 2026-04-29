/**
 * QuickActions component - Pulsanti rapidi bilingue (IT/EN)
 */
import './QuickActions.css';

const QUICK_ACTIONS = {
  it: [
    { id: 'consiglio-farmaco', label: '💊 Consiglio farmaco', message: 'Vorrei un consiglio su un farmaco per il mal di testa', color: 'primary' },
    { id: 'orari-farmacia', label: '🕐 Orari farmacia', message: 'Quali sono gli orari di apertura della farmacia?', color: 'info' },
    { id: 'disponibilita', label: '📦 Disponibilità', message: 'Vorrei sapere se avete disponibile un prodotto', color: 'success' },
    { id: 'servizi', label: '🏥 Servizi', message: 'Quali servizi offrite in farmacia?', color: 'secondary' },
  ],
  en: [
    { id: 'medication-advice', label: '💊 Medication advice', message: 'I need advice for a headache medication', color: 'primary' },
    { id: 'pharmacy-hours', label: '🕐 Pharmacy hours', message: 'What are the pharmacy opening hours?', color: 'info' },
    { id: 'availability', label: '📦 Availability', message: 'I would like to check product availability', color: 'success' },
    { id: 'services', label: '🏥 Services', message: 'What services do you offer?', color: 'secondary' },
  ],
};

export default function QuickActions({ onAction, disabled, language }) {
  const actions = QUICK_ACTIONS[language] || QUICK_ACTIONS.it;

  return (
    <div className="quick-actions" id="quick-actions-panel">
      <p className="quick-actions-label">
        {language === 'en' ? 'Quick actions' : 'Azioni rapide'}
      </p>
      <div className="quick-actions-grid">
        {actions.map((action) => (
          <button
            key={action.id}
            id={`quick-action-${action.id}`}
            className={`quick-action-btn quick-action-${action.color}`}
            onClick={() => onAction(action.message)}
            disabled={disabled}
            aria-label={action.label}
          >
            {action.label}
          </button>
        ))}
      </div>
    </div>
  );
}
