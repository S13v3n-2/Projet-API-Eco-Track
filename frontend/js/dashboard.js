// Gestion du tableau de bord
const dashboard = {
    // Affichage du tableau de bord - CORRIGÉE
    showDashboard: function() {
        document.getElementById('login-section').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
        document.getElementById('user-header').style.display = 'block';
        document.getElementById('user-info').style.display = 'block';

        const email = document.getElementById('email').value || 'admin@ecotrack.com';

        // AFFICHAGE AMÉLIORÉ avec rôle
        let userInfoHtml = `<strong>👤 Connecté en tant que:</strong> ${email}`;
        if (App.currentUser) {
            userInfoHtml += ` | <strong>Rôle:</strong> ${App.currentUser.role}`;
            if (App.currentUser.role === 'admin') {
                userInfoHtml += ' 👑';
            }
        }

        document.getElementById('user-info').innerHTML = userInfoHtml;

        // AFFICHER L'ONGLET ADMIN SI UTILISATEUR EST ADMIN
        const adminTab = document.getElementById('admin-tab');
        if (App.currentUser && App.currentUser.role === 'admin') {
            adminTab.style.display = 'block';
            console.log("🔓 Onglet admin activé");
        } else {
            adminTab.style.display = 'none';
            console.log("🔒 Onglet admin caché - utilisateur non admin");
        }

        this.loadZones();
        this.loadIndicators();
    },

    // NOUVELLE FONCTION : Navigation par onglets
    showTab: function(tabName) {
        console.log("🔍 Changement d'onglet:", tabName);

        // Cacher tous les contenus d'onglets
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.style.display = 'none';
        });

        // Désactiver tous les boutons d'onglets
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // Afficher l'onglet sélectionné
        const targetTab = document.getElementById(`tab-${tabName}`);
        if (targetTab) {
            targetTab.style.display = 'block';
            event.target.classList.add('active');

            // Charger les données si nécessaire
            if (tabName === 'admin') {
                console.log("🔄 Chargement des utilisateurs...");
                admin.loadUsers();
            } else if (tabName === 'stats') {
                this.loadAirStats();
            }
        }
    },

    // Chargement des zones
    loadZones: async function() {
        try {
            const response = await App.apiRequest(`${App.API_BASE}/zones/`);

            if (response.ok) {
                const zones = await response.json();
                const zoneSelect = document.getElementById('filter-zone');
                zoneSelect.innerHTML = '<option value="">Toutes les zones</option>';

                zones.forEach(zone => {
                    const option = document.createElement('option');
                    option.value = zone.id;
                    option.textContent = `${zone.name} (${zone.postal_code})`;
                    zoneSelect.appendChild(option);
                });
            } else if (response.status === 401) {
                auth.logout();
                App.showMessage('Session expirée - Veuillez vous reconnecter', 'error');
            }
        } catch (error) {
            console.error('Error loading zones:', error);
            App.showMessage('Erreur lors du chargement des zones', 'error');
        }
    },

// Chargement des indicateurs - CORRIGÉ
loadIndicators: async function() {
    const typeFilter = document.getElementById('filter-type').value;
    const zoneFilter = document.getElementById('filter-zone').value;
    const limit = document.getElementById('filter-limit').value;
    const startDate = document.getElementById('filter-start-date').value;
    const endDate = document.getElementById('filter-end-date').value;

    document.getElementById('indicators-loading').style.display = 'block';
    document.getElementById('indicators-list').innerHTML = '';

    try {
        // Construction de l'URL avec tous les paramètres
        let url = `${App.API_BASE}/indicators/?limit=${limit}`;

        // CORRECTION : Ne pas envoyer le paramètre type si c'est "Tous les types"
        if (typeFilter && typeFilter !== "") {
            url += `&type=${encodeURIComponent(typeFilter)}`;
        }

        if (zoneFilter && zoneFilter !== "") {
            url += `&zone_id=${encodeURIComponent(zoneFilter)}`;
        }

        // CORRECTION : Toujours envoyer les dates, même si vides
        if (startDate) {
            url += `&start_date=${encodeURIComponent(startDate)}`;
        }
        if (endDate) {
            url += `&end_date=${encodeURIComponent(endDate)}`;
        }

        console.log("🔍 Requête API:", url); // Debug

        const response = await App.apiRequest(url);

        if (response.ok) {
            const indicators = await response.json();
            console.log(`✅ ${indicators.length} indicateurs chargés`); // Debug
            this.displayIndicators(indicators);
        } else if (response.status === 401) {
            auth.logout();
            App.showMessage('Session expirée - Veuillez vous reconnecter', 'error');
        } else {
            console.error('Erreur API:', response.status, response.statusText);
            App.showMessage('Erreur API: ' + response.status, 'error');
        }
    } catch (error) {
        console.error('Error loading indicators:', error);
        App.showMessage('Erreur lors du chargement des indicateurs: ' + error.message, 'error');
    } finally {
        document.getElementById('indicators-loading').style.display = 'none';
    }
},

    // Affichage des indicateurs
    displayIndicators: function(indicators) {
        const list = document.getElementById('indicators-list');

        if (indicators.length === 0) {
            list.innerHTML = '<div class="loading">Aucun indicateur trouvé pour la période sélectionnée</div>';
            return;
        }

        list.innerHTML = indicators.map(ind => {
            const date = App.formatDate(ind.timestamp);
            const quality = this.getQualityBadge(ind.type, ind.value);

            return `
                <div class="indicator-card">
                    <div class="indicator-type">${this.getIndicatorLabel(ind.type)}</div>
                    <div class="indicator-value">${ind.value} ${ind.unit}</div>
                    <div class="indicator-meta">
                        📍 Zone: ${ind.zone_id} | 📅 ${date}
                        ${quality}
                    </div>
                </div>
            `;
        }).join('');
    },

    // Chargement des statistiques
    loadAirStats: async function() {
        const startDate = document.getElementById('stats-start-date').value;
        const endDate = document.getElementById('stats-end-date').value;

        document.getElementById('stats-loading').style.display = 'block';
        document.getElementById('air-stats').innerHTML = '';

        try {
            const response = await App.apiRequest(
                `${App.API_BASE}/stats/air/averages?start_date=${startDate}&end_date=${endDate}`
            );

            if (response.ok) {
                const stats = await response.json();
                this.displayAirStats(stats);
            } else if (response.status === 401) {
                auth.logout();
                App.showMessage('Session expirée - Veuillez vous reconnecter', 'error');
            }
        } catch (error) {
            console.error('Error loading stats:', error);
            App.showMessage('Erreur lors du chargement des statistiques', 'error');
        } finally {
            document.getElementById('stats-loading').style.display = 'none';
        }
    },

    // Affichage des statistiques
    displayAirStats: function(stats) {
        const statsDiv = document.getElementById('air-stats');

        if (stats.length === 0) {
            statsDiv.innerHTML = '<div class="loading">Aucune statistique disponible pour la période sélectionnée</div>';
            return;
        }

        statsDiv.innerHTML = stats.map(stat => `
            <div class="stat-card">
                <div class="stat-label">${stat.zone_name}</div>
                <div class="stat-value">${stat.average_quality.toFixed(1)} µg/m³</div>
                <div class="stat-label">${stat.data_points} mesures</div>
                <div class="stat-label">${stat.period || ''}</div>
            </div>
        `).join('');
    },

    // Libellés des indicateurs
    getIndicatorLabel: function(type) {
        const labels = {
            'air_quality_pm25': '🟡 PM2.5',
            'air_quality_pm10': '🟠 PM10',
            'air_quality_no2': '🔴 NO2',
            'co2': '💨 CO2',
            'temperature': '🌡️ Température',
            'humidity': '💧 Humidité',
            'waste_production': '🗑️ Déchets',
            'energy_consumption': '⚡ Énergie',
            'wind_speed': '💨 Vitesse du vent',
            'pressure': '⏱️ Pression atmosphérique'


        };
        return labels[type] || type;
    },

    // Badges de qualité
    getQualityBadge: function(type, value) {
        if (type === 'air_quality_pm25') {
            if (value <= 15) return '<span class="quality-badge quality-good">BON</span>';
            if (value <= 25) return '<span class="quality-badge quality-moderate">MOYEN</span>';
            return '<span class="quality-badge quality-poor">MAUVAIS</span>';
        }
        if (type === 'air_quality_pm10') {
            if (value <= 20) return '<span class="quality-badge quality-good">BON</span>';
            if (value <= 35) return '<span class="quality-badge quality-moderate">MOYEN</span>';
            return '<span class="quality-badge quality-poor">MAUVAIS</span>';
        }
        return '';
    },
    // Ajouter cette fonction à l'objet dashboard
showTab: function(tabName) {
    // Cacher tous les contenus d'onglets
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });

    // Désactiver tous les boutons d'onglets
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Afficher l'onglet sélectionné
    document.getElementById(`tab-${tabName}`).style.display = 'block';
    event.target.classList.add('active');

    // Charger les données si nécessaire
    if (tabName === 'admin') {
        admin.loadUsers();
    }
    },

    // Modifier la fonction showDashboard pour gérer l'admin
    showDashboard: function() {
        document.getElementById('login-section').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
        document.getElementById('user-header').style.display = 'block';
        document.getElementById('user-info').style.display = 'block';

        const email = document.getElementById('email').value || 'admin@ecotrack.com';
        document.getElementById('user-info').innerHTML = `
            <strong>👤 Connecté en tant que:</strong> ${email}
        `;

        // Afficher l'onglet admin si l'utilisateur est admin
        if (App.currentUser && App.currentUser.role === 'admin') {
            document.getElementById('admin-tab').style.display = 'block';
        }

        this.loadZones();
        this.loadIndicators();
    },

};