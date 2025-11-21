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
                startDateInput.value = startOfMonth.toISOString().split('T')[0];
                endDateInput.value = today.toISOString().split('T')[0];
                break;
            case 'year':
                const startOfYear = new Date(today.getFullYear(), 0, 1);
                startDateInput.value = startOfYear.toISOString().split('T')[0];
                endDateInput.value = today.toISOString().split('T')[0];
                break;
            case 'last7days':
                const sevenDaysAgo = new Date(today);
                sevenDaysAgo.setDate(today.getDate() - 7);
                startDateInput.value = sevenDaysAgo.toISOString().split('T')[0];
                endDateInput.value = today.toISOString().split('T')[0];
                break;
            case 'last30days':
                const thirtyDaysAgo = new Date(today);
                thirtyDaysAgo.setDate(today.getDate() - 30);
                startDateInput.value = thirtyDaysAgo.toISOString().split('T')[0];
                endDateInput.value = today.toISOString().split('T')[0];
                break;
        }

        if (period) {
            dashboard.loadIndicators();
        }
    },

    // Mise à jour des filtres de date
    updateDateFilters: function() {
        // Réinitialiser la sélection de période rapide si les dates sont modifiées manuellement
        document.getElementById('filter-period').value = '';
        dashboard.loadIndicators();
    },

    // Réinitialisation de tous les filtres
    resetFilters: function() {
        document.getElementById('filter-type').value = '';
        document.getElementById('filter-zone').value = '';
        document.getElementById('filter-limit').value = '25';
        document.getElementById('filter-period').value = '';
        App.initializeDates();
        dashboard.loadIndicators();
        App.showMessage('Filtres réinitialisés', 'success');
    }
};