/**
 * Servizio API per comunicare con il backend Django.
 * Gestisce tutte le chiamate HTTP con error handling centralizzato.
 */

const API_BASE_URL = '/api';

/**
 * Helper per le richieste fetch con gestione errori.
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const mergedOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, mergedOptions);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `Errore HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Impossibile connettersi al server. Verificare che il backend sia attivo.');
    }
    throw error;
  }
}

/**
 * Invia un messaggio al chatbot e riceve la risposta AI.
 * @param {string} message - Il messaggio dell'utente
 * @param {string} sessionId - ID sessione opzionale
 * @returns {Promise<{response: string, timestamp: string, provider: string}>}
 */
export async function sendChatMessage(message, sessionId = null) {
  const body = { message };
  if (sessionId) body.session_id = sessionId;

  return apiRequest('/chat/', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

/**
 * Recupera la lista dei prodotti dalla farmacia.
 * @param {Object} filters - Filtri opzionali (available, category, search)
 * @returns {Promise<{count: number, results: Array}>}
 */
export async function getProducts(filters = {}) {
  const params = new URLSearchParams();
  
  if (filters.available !== undefined) params.append('available', filters.available);
  if (filters.category) params.append('category', filters.category);
  if (filters.search) params.append('search', filters.search);

  const queryString = params.toString();
  const endpoint = `/products/${queryString ? `?${queryString}` : ''}`;

  return apiRequest(endpoint);
}

/**
 * Genera un link WhatsApp con messaggio pre-compilato.
 * @param {string} message - Il messaggio da inviare
 * @param {string} phoneNumber - Numero di telefono opzionale
 * @returns {Promise<{whatsapp_url: string, message: string, phone_number: string}>}
 */
export async function generateWhatsAppLink(message, phoneNumber = null) {
  const body = { message };
  if (phoneNumber) body.phone_number = phoneNumber;

  return apiRequest('/whatsapp/', {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

/**
 * Genera un link WhatsApp lato client (fallback se il backend non è disponibile).
 * @param {string} message - Il messaggio da inviare
 * @param {string} phoneNumber - Numero di telefono
 * @returns {string} URL WhatsApp
 */
export function generateWhatsAppLinkLocal(message, phoneNumber = '393331234567') {
  const encodedMessage = encodeURIComponent(message);
  return `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
}
