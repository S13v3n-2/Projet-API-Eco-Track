// Gestion de l'authentification
const auth = {
    // Connexion - MODIFIÉE
    login: async function() {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        if (!email || !password) {
            App.showMessage('Veuillez remplir tous les champs', 'error');
            return;
        }

        try {
            const response = await fetch(`${App.API_BASE}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                App.token = data.access_token;
                localStorage.setItem('ecotrack_token', App.token);

                // NOUVEAU : Récupérer les infos de l'utilisateur connecté
                await this.getCurrentUser();

                dashboard.showDashboard();
                App.showMessage('Connexion réussie!', 'success');
            } else {
                App.showMessage(data.detail || 'Erreur de connexion', 'error');
            }
        } catch (error) {
            App.showMessage('Erreur de connexion: ' + error.message, 'error');
        }
    },

    // NOUVELLE FONCTION : Récupérer l'utilisateur courant
    getCurrentUser: async function() {
        try {
            const response = await App.apiRequest(`${App.API_BASE}/admin/users/me`);
            if (response.ok) {
                App.currentUser = await response.json();
                console.log("👤 Utilisateur connecté:", App.currentUser);
            }
        } catch (error) {
            console.error("Erreur récupération utilisateur:", error);
            // Fallback: essayer une autre route
            await this.getCurrentUserFallback();
        }
    },

    // Fallback si la route /me n'existe pas
    getCurrentUserFallback: async function() {
        try {
            // Récupérer tous les utilisateurs et trouver celui correspondant au token
            const response = await App.apiRequest(`${App.API_BASE}/admin/users/`);
            if (response.ok) {
                const users = await response.json();
                // Ici on suppose que le premier utilisateur est l'admin
                // Dans un vrai système, vous auriez une route /me
                App.currentUser = users[0];
                console.log("👤 Utilisateur (fallback):", App.currentUser);
            }
        } catch (error) {
            console.error("Erreur fallback utilisateur:", error);
        }
    },

    // Inscription
    register: async function() {
        const full_name = document.getElementById('full_name').value;
        const email = document.getElementById('reg_email').value;
        const password = document.getElementById('reg_password').value;

        if (!full_name || !email || !password) {
            App.showMessage('Veuillez remplir tous les champs', 'error');
            return;
        }

        try {
            const response = await fetch(`${App.API_BASE}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, full_name })
            });

            const data = await response.json();

            if (response.ok) {
                App.showMessage('Compte créé avec succès! Vous pouvez maintenant vous connecter.', 'success');
                this.showLogin();
            } else {
                App.showMessage(data.detail || 'Erreur lors de la création du compte', 'error');
            }
        } catch (error) {
            App.showMessage('Erreur lors de la création du compte: ' + error.message, 'error');
        }
    },

    // Déconnexion
    logout: function() {
        localStorage.removeItem('ecotrack_token');
        App.token = null;
        App.currentUser = null;
        document.getElementById('dashboard').style.display = 'none';
        document.getElementById('login-section').style.display = 'block';
        document.getElementById('user-header').style.display = 'none';
        document.getElementById('user-info').style.display = 'none';
        App.showMessage('Déconnexion réussie', 'success');
    },

    // Affichage du formulaire d'inscription
    showRegister: function() {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('register-form').style.display = 'block';
    },

    // Affichage du formulaire de connexion
    showLogin: function() {
        document.getElementById('register-form').style.display = 'none';
        document.getElementById('login-form').style.display = 'block';
    }
};