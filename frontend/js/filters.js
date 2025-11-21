// Gestion des filtres
const filters = {
    // Application des périodes rapides
    applyQuickPeriod: function() {
        const period = document.getElementById('filter-period').value;
        const startDateInput = document.getElementById('filter-start-date');
        const endDateInput = document.getElementById('filter-end-date');
        const today = new Date();

        switch(period) {
            case 'today':
                startDateInput.value = today.toISOString().split('T')[0];
                endDateInput.value = today.toISOString().split('T')[0];
                break;
            case 'yesterday':
                const yesterday = new Date(today);
                yesterday.setDate(yesterday.getDate() - 1);
                startDateInput.value = yesterday.toISOString().split('T')[0];
                endDateInput.value = yesterday.toISOString().split('T')[0];
                break;
            case 'week':
                const startOfWeek = new Date(today);
                startOfWeek.setDate(today.getDate() - today.getDay());
                startDateInput.value = startOfWeek.toISOString().split('T')[0];
                endDateInput.value = today.toISOString().split('T')[0];
                break;
            case 'month':
                const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
                const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);
                startDateInput.value = this.formatDate(startOfMonth);
                endDateInput.value = this.formatDate(endOfMonth);
                break;
            case 'year':
                const startOfYear = new Date(today.getFullYear(), 0, 1);
                const endOfYear = new Date(today.getFullYear(), 11, 31);
                startDateInput.value = this.formatDate(startOfYear);
                endDateInput.value = this.formatDate(endOfYear);
                break;
            case 'last7days':
                const sevenDaysAgo = new Date(today);
                sevenDaysAgo.setDate(today.getDate() - 7);
                startDateInput.value = this.formatDate(sevenDaysAgo);
                endDateInput.value = this.formatDate(today);
                break;
            case 'last30days':
                const thirtyDaysAgo = new Date(today);
                thirtyDaysAgo.setDate(today.getDate() - 30);
                startDateInput.value = this.formatDate(thirtyDaysAgo);
                endDateInput.value = this.formatDate(today);
                break;
        }

        if (period) {
            dashboard.loadIndicators();
        }
    },

    // Mise à jour des filtres de date
    updateDateFilters: function() {
        document.getElementById('filter-period').value = '';
        dashboard.loadIndicators();
    },

    // Réinitialisation de tous les filtres
    resetFilters: function() {
        document.getElementById('filter-type').value = '';
        document.getElementById('filter-zone').value = '';
        document.getElementById('filter-limit').value = '25';
        document.getElementById('filter-period').value = '';
        this.initializeDefaultDates();
        dashboard.loadIndicators();
        App.showMessage('Filtres réinitialisés', 'success');
    },

    // Initialisation des dates par défaut (début du mois → fin du mois)
    initializeDefaultDates: function() {
        const today = new Date();
        const startDateInput = document.getElementById('filter-start-date');
        const endDateInput = document.getElementById('filter-end-date');

        // Date de début : 1er du mois
        const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);

        // Date de fin : dernier jour du mois
        const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);

        startDateInput.value = this.formatDate(startOfMonth);
        endDateInput.value = this.formatDate(endOfMonth);

        console.log('📅 Dates initialisées:', startDateInput.value, '→', endDateInput.value);
    },

    // Formatage de date en YYYY-MM-DD
    formatDate: function(date) {
        return date.toISOString().split('T')[0];
    }
};

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    filters.initializeDefaultDates();
});