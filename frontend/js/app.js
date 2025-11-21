// Configuration globale de l'application
const App = {
    API_BASE: "http://localhost:8000",
    token: localStorage.getItem('ecotrack_token'),
    currentUser: null,

    // Initialisation de l'application
    init: function() {
        console.log('🚀 Initialisation de EcoTrack...');
        this.initializeDates();

        if (this.token) {
            dashboard.showDashboard();
        }
    },

    // Initialisation des dates par défaut
    initializeDates: function() {
        const today = new Date().toISOString().split('T')[0];
        const oneWeekAgo = new Date();
        oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
        const oneWeekAgoStr = oneWeekAgo.toISOString().split('T')[0];

        // Définir les dates par défaut pour les filtres
        document.getElementById('filter-start-date').value = oneWeekAgoStr;
        document.getElementById('filter-end-date').value = today;

        // Dates pour les stats (année en cours)
        const currentYear = new Date().getFullYear();
        document.getElementById('stats-start-date').value = `${currentYear}-01-01`;
        document.getElementById('stats-end-date').value = `${currentYear}-12-31`;
    },

    // Gestion des messages
    showMessage: function(text, type) {
        const messageDiv = document.getElementById('message');
        messageDiv.innerHTML = `<div class="${type}">${text}</div>`;
        setTimeout(() => messageDiv.innerHTML = '', 5000);
    },

    // Utilitaire pour formater les dates
    formatDate: function(dateString) {
        return new Date(dateString).toLocaleDateString('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    // Utilitaire pour les requêtes API
    apiRequest: async function(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            }
        };

        const mergedOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, mergedOptions);
            return response;
        } catch (error) {
            console.error('❌ Erreur réseau:', error);
            throw error;
        }
    }
};

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    App.init();
});