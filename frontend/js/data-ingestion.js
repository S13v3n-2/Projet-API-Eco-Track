// Gestion de l'ingestion des données externes
const dataIngestion = {
    // Lance l'ingestion des données externes
    fetchExternalData: async function() {
        const button = document.getElementById('fetch-external-data');
        const buttonText = button.querySelector('.btn-text');
        const buttonLoading = button.querySelector('.btn-loading');
        const resultDiv = document.getElementById('ingestion-result');
        
        // Désactiver le bouton et afficher le loading
        button.disabled = true;
        buttonText.style.display = 'none';
        buttonLoading.style.display = 'inline';
        resultDiv.innerHTML = '⏳ Connexion aux APIs externes...';
        resultDiv.style.color = '#856404';
        
        try {
            // CORRECTION : Utiliser App.API_BASE pour l'URL complète
            const response = await fetch(`${App.API_BASE}/indicators/ingest/external-data`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${App.token}`
                }
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Erreur HTTP: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                resultDiv.innerHTML = `✅ ${data.message}`;
                resultDiv.style.color = '#155724';
                
                // Afficher les détails
                const details = data.details;
                resultDiv.innerHTML += `<br><small>
                    🌤️ Météo: ${details.weather_data} | 
                    🌫️ Qualité air: ${details.air_quality_data} | 
                    ⚡ Énergie: ${details.energy_data} | 
                    📊 Total: ${details.total}
                </small>`;
                
                // Recharger les indicateurs après un délai
                setTimeout(() => {
                    dashboard.loadIndicators();
                }, 2000);
                
                App.showMessage('Données externes récupérées avec succès!', 'success');
            } else {
                throw new Error(data.detail || 'Erreur inconnue');
            }
            
        } catch (error) {
            console.error('Erreur ingestion données:', error);
            resultDiv.innerHTML = `❌ Erreur: ${error.message}`;
            resultDiv.style.color = '#721c24';
            App.showMessage('Erreur lors de la récupération des données: ' + error.message, 'error');
        } finally {
            // Réactiver le bouton
            button.disabled = false;
            buttonText.style.display = 'inline';
            buttonLoading.style.display = 'none';
            
            // Effacer le message après 10 secondes
            setTimeout(() => {
                resultDiv.innerHTML = '';
            }, 10000);
        }
    },
    
    // Initialisation
    init: function() {
        const button = document.getElementById('fetch-external-data');
        if (button) {
            button.addEventListener('click', this.fetchExternalData);
        }
    }
};

// Initialiser au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    dataIngestion.init();
});